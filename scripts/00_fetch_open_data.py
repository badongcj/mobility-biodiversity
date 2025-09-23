
# -*- coding: utf-8 -*-

"""
脚本：00_fetch_open_data.py

作用：零账号（Zero-login）拉取小范围（按地名或自定义边界）的起步数据：
- ESA WorldCover 10m（2021 v200）：通过 AWS 公共桶 + COG（无需登录）
- OSM 道路：osmnx 从 Overpass 拉取
- GBIF 物种记录：pygbif 公开 API
输出：
- data/raw/worldcover_*.tif
- data/raw/osm_roads_*.gpkg
- data/raw/gbif_occ_*.parquet
- data/processed/aoi.gpkg 研究区范围

用法示例：
  conda activate mobiodiv
  pip install -r requirements.txt
  python scripts/00_fetch_open_data.py --place "Singapore" --buffer_km 20

注意：
- 该脚本仅为起跑包（小范围）；大范围/全球请转用官方批量下载方案（详见 README_zh）。
"""
from __future__ import annotations
import argparse, os, math, io
from pathlib import Path
import geopandas as gpd
import pandas as pd
import numpy as np
import shapely.geometry as sgeom

import osmnx as ox
from pygbif import occurrences as gbif_occ
from pystac_client import Client as StacClient
import boto3
import botocore
import rasterio
from rasterio import windows
from rasterio.session import AWSSession
from rasterio.enums import Resampling
import rioxarray as rxr

# 本项目的路径配置
from mobiodiv.config import DATA_DIR, RAW_DIR, PROCESSED_DIR, CRS_WGS84

ESA_WORLDCOVER_STAC = "https://services.terrascope.be/stac"  # 官方 STAC 端点（公开）
ESA_WORLDCOVER_BUCKET = "esa-worldcover"                     # AWS 公共桶（无需签名）
ESA_WORLDCOVER_PREFIX = "v200/2021/map"                      # 2021 v200 地图路径
ESA_COLLECTION_HINTS = ["worldcover", "WorldCover", "VITO"]  # 模糊匹配集合名

def geocode_aoi(place: str, buffer_km: float = 0.0) -> gpd.GeoDataFrame:
    """用 osmnx 根据地名获取多边形并可选缓冲（单位 km）"""
    gdf = ox.geocode_to_gdf(place)
    gdf = gdf.to_crs(3857)
    if buffer_km and buffer_km > 0:
        gdf["geometry"] = gdf.geometry.buffer(buffer_km * 1000.0)
    gdf = gdf.to_crs(CRS_WGS84)
    gdf["name"] = place
    return gdf[["name", "geometry"]]

def bbox_from_gdf(gdf: gpd.GeoDataFrame) -> tuple[float,float,float,float]:
    minx, miny, maxx, maxy = gdf.total_bounds
    return (minx, miny, maxx, maxy)

def pick_worldcover_items_by_bbox(bbox):
    """通过 STAC 搜索 WorldCover 2021 v200 COG（按 bbox）"""
    try:
        client = StacClient.open(ESA_WORLDCOVER_STAC)
        # 尝试所有集合，避免名称差异
        items = None
        for coll in client.get_collections():
            name = (coll.id or "").lower()
            if any(h in name for h in [h.lower() for h in ESA_COLLECTION_HINTS]):
                search = client.search(collections=[coll.id], bbox=bbox)
                items = list(search.get_items())
                if items:
                    break
        return items or []
    except Exception as e:
        print("STAC 查询失败，将退回到 AWS 直接列目录：", e)
        return []

def download_worldcover_cogs(items, out_dir: Path, bbox):
    """下载并/或裁剪 COG。若 items 为空，则直接从 AWS 列出并尝试读入重采样裁剪。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    # 配置匿名 AWS 会话（no-sign-request）
    s3 = boto3.client("s3", config=botocore.config.Config(signature_version=botocore.UNSIGNED), region_name="eu-central-1")
    session = AWSSession(botocore_session=botocore.session.get_session())
    minx, miny, maxx, maxy = bbox

    saved = []
    if items:
        # 逐个 COG 拉取并裁剪（保存在 raw 下）
        for it in items:
            href = it.assets["map"].href if "map" in it.assets else list(it.assets.values())[0].href
            # href 可能是 s3://esa-worldcover/... 或 https://...，这里统一改为 vsicurl 读取并裁剪
            try:
                with rasterio.Env(AWSSession(botocore_session=botocore.session.get_session())):
                    with rasterio.open(href) as src:
                        window = windows.from_bounds(minx, miny, maxx, maxy, transform=src.transform, height=src.height, width=src.width)
                        out = src.read(window=window, out_dtype=src.dtypes[0], resampling=Resampling.nearest)
                        profile = src.profile.copy()
                        transform = windows.transform(window, src.transform)
                        profile.update({
                            "height": out.shape[1],
                            "width": out.shape[2],
                            "transform": transform
                        })
                        out_path = out_dir / f"worldcover_clip_{minx:.3f}_{miny:.3f}_{maxx:.3f}_{maxy:.3f}.tif"
                        with rasterio.open(out_path, "w", **profile) as dst:
                            dst.write(out)
                        saved.append(out_path)
            except Exception as e:
                print("读取/裁剪失败：", e)
    else:
        # 直接列 AWS 目录（COG 组织为 3x3 度瓦片），做粗筛后逐瓦片裁剪
        paginator = s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=ESA_WORLDCOVER_BUCKET, Prefix=ESA_WORLDCOVER_PREFIX):
            for obj in page.get("Contents", []):
                key = obj["Key"]
                if not key.lower().endswith(".tif"):
                    continue
                # 直接尝试打开并裁剪（性能较慢，但零账号可用）
                href = f"/vsis3/{ESA_WORLDCOVER_BUCKET}/{key}"
                try:
                    with rasterio.open(href) as src:
                        # 快速判断是否相交（通过坐标系与 bbox）
                        left, bottom, right, top = src.bounds
                        if (right < minx) or (left > maxx) or (top < miny) or (bottom > maxy):
                            continue
                        window = windows.from_bounds(minx, miny, maxx, maxy, transform=src.transform, height=src.height, width=src.width)
                        out = src.read(window=window, out_dtype=src.dtypes[0], resampling=Resampling.nearest)
                        if out.size == 0:
                            continue
                        profile = src.profile.copy()
                        transform = windows.transform(window, src.transform)
                        profile.update({"height": out.shape[1], "width": out.shape[2], "transform": transform})
                        out_path = out_dir / f"worldcover_clip_{minx:.3f}_{miny:.3f}_{maxx:.3f}_{maxy:.3f}.tif"
                        with rasterio.open(out_path, "w", **profile) as dst:
                            dst.write(out)
                        saved.append(out_path)
                        # 找到一个覆盖瓦片即可
                        return saved
                except Exception as e:
                    # 某些瓦片可能读失败，忽略继续
                    continue
    return saved

def fetch_osm_roads(aoi_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """下载研究区道路（机动车网）：返回 GeoDataFrame"""
    poly = aoi_gdf.geometry.unary_union
    G = ox.graph_from_polygon(poly, network_type="drive")
    roads = ox.graph_to_gdfs(G, nodes=False, edges=True)
    roads = roads.to_crs(CRS_WGS84)
    return roads

def fetch_gbif_occurrences(aoi_gdf: gpd.GeoDataFrame, taxon: str = "Aves", limit: int = 2000) -> pd.DataFrame:
    """
    通过 GBIF 公开 API 拉取一定数量的观测记录（示例：鸟类 Aves）
    - 使用 geometry=polygon WKT 限制空间范围
    - 可按需增加年份、质量过滤等
    """
    poly = aoi_gdf.geometry.iloc[0]
    # WKT
    wkt = sgeom.mapping(poly)  # GeoJSON
    # gbif_occ.search 支持 geometry=WKT 字符串（这里简单用 bbox 以提高兼容性）
    minx, miny, maxx, maxy = aoi_gdf.total_bounds
    out = gbif_occ.search(scientificName=taxon, hasCoordinate=True,
                          decimalLatitude=str(miny) + "," + str(maxy),
                          decimalLongitude=str(minx) + "," + str(maxx),
                          limit=limit)
    recs = out.get("results", [])
    if not recs:
        return pd.DataFrame()
    df = pd.DataFrame(recs)
    keep = ["scientificName","decimalLatitude","decimalLongitude","eventDate","basisOfRecord","datasetKey","occurrenceID"]
    df = df[[c for c in keep if c in df.columns]]
    return df

def run(place: str, buffer_km: float = 20.0) -> None:
    """执行零账号开源数据拉取流程。

    该函数将研究区范围、多源栅格和矢量数据写入 ``data`` 目录，
    便于在交互式入口（如 CLI 或 Notebook）中重复调用。
    """

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # 1) 研究区
    aoi = geocode_aoi(place, buffer_km=buffer_km)
    aoi_path = PROCESSED_DIR / "aoi.gpkg"
    aoi.to_file(aoi_path, driver="GPKG")
    print(f"[AOI] 已保存 {aoi_path}")

    # 2) WorldCover（裁剪）
    bbox = bbox_from_gdf(aoi)
    items = pick_worldcover_items_by_bbox(bbox)
    wc_paths = download_worldcover_cogs(items, RAW_DIR, bbox)
    if wc_paths:
        print(f"[WorldCover] 已写入 {wc_paths[0]}")
    else:
        print("[WorldCover] 未能找到覆盖瓦片，请扩大缓冲或检查网络。")

    place_slug = place.replace(" ", "_")

    # 3) OSM 道路
    try:
        roads = fetch_osm_roads(aoi)
        roads_path = RAW_DIR / f"osm_roads_{place_slug}.gpkg"
        roads.to_file(roads_path, driver="GPKG")
        print(f"[OSM] 道路写入 {roads_path}")
    except Exception as e:
        print("[OSM] 拉取失败：", e)

    # 4) GBIF 物种（示例：鸟类 Aves 2000 条）
    try:
        df = fetch_gbif_occurrences(aoi, taxon="Aves", limit=2000)
        gbif_path = RAW_DIR / f"gbif_occ_{place_slug}.parquet"
        if len(df):
            df.to_parquet(gbif_path, index=False)
            print(f"[GBIF] 记录数：{len(df)}，写入 {gbif_path}")
        else:
            print("[GBIF] 未获取到记录，建议增大 limit 或更换 taxon。")
    except Exception as e:
        print("[GBIF] 拉取失败：", e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--place", type=str, required=True, help="地名（例如：Singapore、Beijing、Nairobi）")
    parser.add_argument("--buffer_km", type=float, default=20, help="可选缓冲距离（km），扩大研究区范围")
    args = parser.parse_args()

    run(place=args.place, buffer_km=args.buffer_km)

if __name__ == "__main__":
    main()

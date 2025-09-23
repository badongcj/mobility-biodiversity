# -*- coding: utf-8 -*-
"""OSM 道路数据下载（基于 osmnx）并计算道路密度/长度等指标"""
import geopandas as gpd
import osmnx as ox
from shapely.geometry import box
from pathlib import Path
from ..config import OUTPUTS, CRS_WGS84

def download_osm_roads(polygon: gpd.GeoSeries, network_type: str = "drive"):
    """根据研究区多边形下载 OSM 道路网络
    参数:
      polygon: GeoSeries（单个多边形，WGS84）
      network_type: 'drive'（机动车道），也可用 'walk'、'bike' 等
    返回:
      roads: GeoDataFrame（道路边）
    """
    poly = polygon.values[0]
    G = ox.graph_from_polygon(poly, network_type=network_type, simplify=True)
    edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
    roads = edges.to_crs(CRS_WGS84)
    return roads

def road_density(roads: gpd.GeoDataFrame, area_gdf: gpd.GeoDataFrame, buffer_m: int = 0):
    """计算道路密度（道路总长度 / 面积），可选缓冲
    返回:
      area_gdf 带新字段 'road_km_per_km2'
    """
    if buffer_m > 0:
        area_gdf = area_gdf.copy()
        area_gdf['geometry'] = area_gdf.buffer(buffer_m)
    # 叠加裁剪
    clipped = gpd.overlay(roads[['geometry']], area_gdf[['geometry']], how='intersection')
    clipped['len_km'] = clipped.length / 1000.0
    total_len = clipped['len_km'].sum()
    area_km2 = area_gdf.to_crs(3857).area.sum() / 1e6
    density = total_len / area_km2 if area_km2 > 0 else 0.0
    area_gdf['road_km_per_km2'] = density
    return area_gdf

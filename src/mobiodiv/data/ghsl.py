# -*- coding: utf-8 -*-
"""GHSL（UCDB/SMOD/FUA/POP）读取与城市-城郊-农村分层构建"""
from pathlib import Path
import geopandas as gpd
import rioxarray as rxr
import xarray as xr
import numpy as np
from shapely.geometry import box
from ..config import FILES, OUTPUTS, CRS_WGS84

def build_strata(ucdb_path: Path = FILES['ghsl_ucdb'],
                 smod_path: Path = FILES['ghsl_smod'],
                 out_path: Path = OUTPUTS['strata_gpkg']):
    """基于 UCDB 城市多边形和 SMOD 栅格构建分层（城市-城郊-农村）
    说明：
      - SMOD（Degree of Urbanisation）常见编码：城市(30/31)、城镇/半密集(23/24)、农村(11/12/13)
      - 这里提供一个简单阈值法，你可以按需微调分类规则
    """
    # 读取城市边界（UCDB）
    cities = gpd.read_file(ucdb_path).to_crs(CRS_WGS84)
    # 读取 SMOD 栅格
    smod = rxr.open_rasterio(smod_path, masked=True).squeeze()  # 2D
    smod = smod.rio.reproject(CRS_WGS84)

    records = []
    for _, row in cities.iterrows():
        geom = row.geometry
        # 裁剪栅格到城市外扩一定缓冲（例如 30km）形成 城市-城郊-农村 环
        buffer_km = 30_000  # 30km
        bbox = gpd.GeoSeries([geom.buffer(buffer_km)], crs=CRS_WGS84).total_bounds
        clipped = smod.rio.clip_box(minx=bbox[0], miny=bbox[1], maxx=bbox[2], maxy=bbox[3])

        # 简单分类（示例）
        city_mask = np.isin(clipped.values, [30,31])
        town_mask = np.isin(clipped.values, [23,24])
        rural_mask = np.isin(clipped.values, [11,12,13])

        # 将三类掩膜转为矢量多边形（可选：简化/合并）
        # 为简洁起见，这里不展开栅格→矢量步骤；生产中可用 rasterio.features.shapes 或 rioxarray 的向量化。
        # TODO: 将掩膜矢量化并写入 out_path

    # 占位：写空的 gpkg，避免后续报错
    cities.to_file(out_path, driver='GPKG')
    return out_path

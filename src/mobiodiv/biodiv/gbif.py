# -*- coding: utf-8 -*-
"""GBIF 物种记录下载与栅格聚合（示例）"""
from pathlib import Path
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from ..config import FILES, CRS_WGS84

def load_gbif_occ(csv_path: Path = FILES['gbif_occ']):
    """读取 GBIF 导出的 CSV（请在官网或 API 申请并下载），并转为 GeoDataFrame"""
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=['decimalLatitude', 'decimalLongitude'])
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df['decimalLongitude'], df['decimalLatitude']),
        crs=CRS_WGS84
    )
    return gdf[['species', 'eventDate', 'geometry']]

# -*- coding: utf-8 -*-
"""空气污染（NO2/PM2.5）读取与标准化（占位示例）"""
from pathlib import Path
import rioxarray as rxr
import xarray as xr
import numpy as np
from ..config import FILES, CRS_WGS84

def load_no2(no2_path: Path = FILES['no2']):
    """读取 NO2 格网（例如 TROPOMI 的年度或多年月均合成）"""
    da = rxr.open_rasterio(no2_path).squeeze().rio.reproject(CRS_WGS84)
    return da

def load_pm25(pm25_path: Path = FILES['pm25']):
    da = rxr.open_rasterio(pm25_path).squeeze().rio.reproject(CRS_WGS84)
    return da

def standardize_layers(*arrays):
    """对多层指标做标准化（z-score），便于构建 “干扰指数”"""
    std_layers = []
    for da in arrays:
        mu = float(da.mean().values)
        sigma = float(da.std().values)
        std_layers.append((da - mu) / (sigma + 1e-9))
    return std_layers

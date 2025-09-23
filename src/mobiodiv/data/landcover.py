# -*- coding: utf-8 -*-
"""陆覆/植被（WorldCover/CGLS/Landsat NDVI/Hansen/GEDI）处理与栖息地指标"""
from pathlib import Path
import geopandas as gpd
import rioxarray as rxr
import numpy as np
import pandas as pd
from skimage import measure
from ..config import FILES, CRS_WGS84
import pylandstats as pls

def load_worldcover(path: Path = FILES['worldcover']):
    """读取 WorldCover 10m/100m 重采样栅格，并保持到 WGS84"""
    da = rxr.open_rasterio(path).squeeze().rio.reproject(CRS_WGS84)
    return da

def habitat_mask(da, habitat_codes=(10, 20, 30)):
    """根据陆覆编码创建“栖息地”掩膜（示例：森林/灌丛/草地）"""
    mask = np.isin(da.values, list(habitat_codes))
    return mask

def compute_patch_metrics(mask: np.ndarray, transform, crs=CRS_WGS84):
    """使用 pylandstats 计算景观指标（面积、边界、最大斑块指数等）
    参数:
      mask: 二值掩膜（True 为栖息地）
      transform: 栅格仿射变换（rasterio.transform.Affine）
    返回:
      metrics: dict
    """
    # pylandstats 接受类别栅格，这里把 True/False → 1/0
    import rasterio
    arr = mask.astype(np.uint8)
    profile = {
        'driver': 'GTiff',
        'height': arr.shape[0],
        'width': arr.shape[1],
        'count': 1,
        'dtype': rasterio.uint8,
        'crs': crs,
        'transform': transform
    }
    # 用 pylandstats 计算（注意：真实运行需写入临时文件或构造 Landscape 对象）
    ls = pls.Landscape(arr, res=(abs(transform.a), abs(transform.e)))
    class_metrics = ls.compute_class_metrics_df()
    landscape_metrics = ls.compute_landscape_metrics_df()
    return {
        "class": class_metrics.to_dict(orient="list"),
        "landscape": landscape_metrics.to_dict(orient="list"),
    }

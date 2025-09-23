# -*- coding: utf-8 -*-
"""构建“人类干扰指数”（夜光 + 道路密度 + NO2/PM2.5 的标准化合成）"""
import numpy as np
import xarray as xr

def composite_disturbance(std_viirs: xr.DataArray, std_roads: xr.DataArray, std_no2: xr.DataArray, std_pm25: xr.DataArray, weights=None):
    """将多个标准化层合成为单一干扰指数（加权平均）
    参数:
      std_*: 皆为已 z-score 标准化的栅格
      weights: 权重（默认等权）
    返回:
      xr.DataArray 干扰指数
    """
    stack = xr.concat([std_viirs, std_roads, std_no2, std_pm25], dim='band')
    if weights is None:
        weights = np.ones(stack.sizes['band']) / stack.sizes['band']
    out = (stack * xr.DataArray(weights, dims=['band'])).sum('band')
    return out

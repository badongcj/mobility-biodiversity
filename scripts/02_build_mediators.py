# -*- coding: utf-8 -*-
"""脚本2：构建“中介”数据集（栖息地/连通性 + 干扰指数）"""
from pathlib import Path
from mobiodiv.config import FILES, OUTPUTS
from mobiodiv.data.landcover import load_worldcover, habitat_mask, compute_patch_metrics
from mobiodiv.data.airquality import load_no2, load_pm25, standardize_layers
from mobiodiv.metrics.disturbance import composite_disturbance
import rioxarray as rxr
import xarray as xr
import pandas as pd

if __name__ == "__main__":
    # ===== 示例：读取 WorldCover 并生成栖息地掩膜 =====
    da = load_worldcover()
    mask = habitat_mask(da, habitat_codes=(10,20,30))  # 示例编码：森林/灌丛/草地
    # TODO: 使用真实 transform 与 pylandstats 计算景观/连通性指标

    # ===== 示例：构建干扰指数 =====
    no2 = load_no2()
    pm25 = load_pm25()
    # 这里暂时以自身标准化示意；夜光/道路密度请在对应模块计算后传入
    no2_z, pm25_z = standardize_layers(no2, pm25)
    # 占位合成（缺夜光/道路）
    disturbance = composite_disturbance(no2_z*0, no2_z*0, no2_z, pm25_z)
    disturbance.rio.to_raster(OUTPUTS['mediators_parquet'].with_suffix(".tif"))
    print("已输出干扰指数栅格（示意）。")

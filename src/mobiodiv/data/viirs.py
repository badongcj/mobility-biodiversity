# -*- coding: utf-8 -*-
"""VIIRS 夜间灯光（VNL）下载与栅格处理"""
from pathlib import Path
from . import ghsl
from ..utils.io import download_file
from ..config import FILES

def download_viirs_annual(year: int, out_path: Path = FILES['viirs_vnl']):
    """下载 VIIRS 年度合成（示例：需要你将 BASE_URL 替换为官方年度产品地址）
    提示：不同年份/版本的路径可能不同，请按官方目录结构修改。
    """
    BASE_URL = "https://example/noaa/viirs/VNL_v2/{year}/global_vcmslcfg_c{year}.tif"  # TODO: 替换为真实地址
    url = BASE_URL.format(year=year)
    return download_file(url, out_path)

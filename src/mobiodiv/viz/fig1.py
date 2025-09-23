# -*- coding: utf-8 -*-
"""图1：暴露与研究设计（示例绘图框架）"""
import matplotlib.pyplot as plt
import geopandas as gpd
from ..config import OUTPUTS
from pathlib import Path

def make_fig1(strata_path: Path = OUTPUTS['strata_gpkg'], out_path: Path = None):
    """读取分层 GPKG，绘制 O–D 网络/分层示意/覆盖率等（此处为占位绘图）
    实际项目中：建议将子图拆分为函数，分别负责(a)-(e)子图，再在此组合。
    """
    gdf = gpd.read_file(strata_path)
    fig, ax = plt.subplots(1, 1, figsize=(6, 6), dpi=200)
    gdf.plot(ax=ax, linewidth=0.2, edgecolor='gray', facecolor='none')
    ax.set_title('Fig. 1 占位：研究分层与覆盖（请替换为真实绘图）', fontproperties=None)
    ax.set_axis_off()
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, bbox_inches='tight')
    return fig

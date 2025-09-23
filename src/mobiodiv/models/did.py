# -*- coding: utf-8 -*-
"""差分中的差分（DiD）与面板模型（linearmodels）"""
import pandas as pd
from linearmodels.panel import PanelOLS
import statsmodels.api as sm

def run_did(df: pd.DataFrame, y: str, treat: str, post: str, fe_unit: str, fe_time: str, covars=None):
    """经典二元 DiD：y ~ treat*post + FE(单位, 时间) + 协变量
    参数:
      df: 面板数据（多期多地）
      y: 因变量（多样性指标等）
      treat: 处理组指示（是否受“冲击/开通/政策”等影响）
      post: 冲击后时期指示
      fe_unit: 个体固定效应键（如 city_id 或 rural_catchment_id）
      fe_time: 时间固定效应键（如 year）
      covars: 其他控制变量列表
    返回:
      回归结果对象
    """
    work = df.copy().set_index([fe_unit, fe_time])
    X_terms = [f'{treat}', f'{post}', f'{treat}:{post}']
    if covars:
        X_terms += covars
    X = sm.add_constant(work[X_terms], has_constant='add')
    mod = PanelOLS(work[y], X, entity_effects=True, time_effects=True)
    res = mod.fit(cov_type='clustered', cluster_entity=True)
    return res

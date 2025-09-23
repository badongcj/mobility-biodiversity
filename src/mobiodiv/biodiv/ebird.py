# -*- coding: utf-8 -*-
"""eBird EBD 读取与最简占据模型占位（基于 PyMC 的示例）"""
from pathlib import Path
import pandas as pd
import pymc as pm
import numpy as np
from ..config import FILES

def load_ebd_tsv_gz(path: Path = FILES['ebird_ebd'], max_rows: int = 100000):
    """读取 eBird EBD（制表符分隔、gzip 压缩），仅载入必要列
    注意：EBD 体量很大，请先用官方过滤器导出区域/时间窗口，再读取。
    """
    usecols = [
        'SAMPLING.EVENT.IDENTIFIER','COMMON.NAME','SCIENTIFIC.NAME','OBSERVATION.COUNT',
        'LATITUDE','LONGITUDE','OBSERVATION.DATE','EFFORT.DISTANCE.KM','DURATION.MINUTES',
        'ALL.OBSERVATIONS.REPORTED'
    ]
    df = pd.read_csv(path, sep='\t', compression='gzip', usecols=usecols, nrows=max_rows)
    return df

def toy_occupancy_model(y, effort):
    """极简占据-检测模型（示意）：psi 为占据概率，p 为检测概率
    y: 二值观测（1=记录到该物种，0=未记录到）
    effort: 观测努力（如时长/距离，已标准化）
    """
    with pm.Model() as model:
        alpha_psi = pm.Normal('alpha_psi', 0, 1.0)
        alpha_p = pm.Normal('alpha_p', 0, 1.0)
        beta_p_eff = pm.Normal('beta_p_eff', 0, 1.0)

        psi = pm.Deterministic('psi', pm.math.sigmoid(alpha_psi))
        logit_p = alpha_p + beta_p_eff * effort
        p = pm.Deterministic('p', pm.math.sigmoid(logit_p))

        theta = psi * p  # 简化：非层级、非时间/空间结构，仅示意
        pm.Bernoulli('y', p=theta, observed=y)

        idata = pm.sample(1000, tune=1000, target_accept=0.9, chains=2, progressbar=False)
    return idata

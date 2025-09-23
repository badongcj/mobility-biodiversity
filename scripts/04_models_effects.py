# -*- coding: utf-8 -*-
"""脚本4：面板与中介估计（DiD + 线性中介占位）"""
import pandas as pd
from mobiodiv.models.did import run_did
from mobiodiv.models.mediation import paramed_linear

if __name__ == "__main__":
    # 生成一份模拟数据演示 DiD（真实项目请读取处理后的面板）
    import numpy as np
    n_units, n_time = 50, 6
    idx = pd.MultiIndex.from_product([range(n_units), range(n_time)], names=['unit','year'])
    df = pd.DataFrame(index=idx).reset_index()
    df['treat'] = (df['unit'] < n_units//2).astype(int)
    df['post'] = (df['year'] >= 3).astype(int)
    # 真值：处理效应 0.2
    rng = np.random.default_rng(42)
    df['m'] = 0.5*df['treat'] + rng.normal(0,1, size=len(df))
    df['y'] = 0.2*df['treat']*df['post'] + 0.3*df['m'] + rng.normal(0,1, size=len(df))

    did_res = run_did(df, y='y', treat='treat', post='post', fe_unit='unit', fe_time='year')
    print(did_res.summary)

    med = paramed_linear(y=df['y'], x=df['treat'], m=df['m'])
    print("中介分解：", {k: round(v,4) if isinstance(v, (int,float)) else '...' for k,v in med.items() if k.endswith('effect')})

# -*- coding: utf-8 -*-
"""简化的中介分解（参数化法）与 PyMC 层级模型占位"""
import pandas as pd
import statsmodels.api as sm

def paramed_linear(y, x, m, covars=None):
    """最简单的线性中介分解（Baron–Kenny 思路，仅作占位）
    路径: x -> m, y ~ x + m (+ covars)
    返回: 总效应、直接效应、间接效应（线性近似）
    """
    covars = covars or []
    # x->m
    Xm = sm.add_constant(pd.concat([x] + [covars], axis=1), has_constant='add')
    mhat = sm.OLS(m, Xm).fit()
    a = mhat.params[x.name]
    # y ~ x + m
    Xy = sm.add_constant(pd.concat([x, m] + [covars], axis=1), has_constant='add')
    yhat = sm.OLS(y, Xy).fit()
    b = yhat.params[m.name]
    c_prime = yhat.params[x.name]
    ab = a * b
    # 总效应（不含 m）
    Xc = sm.add_constant(pd.concat([x] + [covars], axis=1), has_constant='add')
    chat = sm.OLS(y, Xc).fit()
    c_total = chat.params[x.name]
    return {
        "total_effect": c_total,
        "direct_effect": c_prime,
        "indirect_effect": ab,
        "models": {"x_to_m": mhat, "y_on_xm": yhat}
    }

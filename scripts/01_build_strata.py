# -*- coding: utf-8 -*-
"""脚本1：生成城市-城郊-农村分层（用于图1）"""
from pathlib import Path
from mobiodiv.config import OUTPUTS
from mobiodiv.data.ghsl import build_strata

if __name__ == "__main__":
    out = build_strata()
    print(f"分层矢量已写入: {out}")

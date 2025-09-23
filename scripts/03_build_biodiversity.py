# -*- coding: utf-8 -*-
"""脚本3：生物多样性数据处理（eBird/GBIF 占位）"""
from mobiodiv.biodiv.gbif import load_gbif_occ
from mobiodiv.biodiv.ebird import load_ebd_tsv_gz
from mobiodiv.config import OUTPUTS

if __name__ == "__main__":
    try:
        gdf = load_gbif_occ()
        print(f"GBIF 记录数：{len(gdf)}")
    except Exception as e:
        print("GBIF 未就绪：", e)

    try:
        ebd = load_ebd_tsv_gz()
        print(f"EBD 记录预览：{ebd.head(3)}")
    except Exception as e:
        print("EBD 未就绪：", e)

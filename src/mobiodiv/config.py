# -*- coding: utf-8 -*-
"""项目级配置（路径、坐标系、文件名约定等）"""
from pathlib import Path

# 工程根目录（可按需修改）
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"

OUT_DIR = PROJECT_ROOT / "outputs"
FIG_DIR = OUT_DIR / "figures"
TAB_DIR = OUT_DIR / "tables"

# 常用坐标参考
CRS_WGS84 = "EPSG:4326"

# 研究区域/城市清单（示例；可替换为你的列表或全局）
CITY_LIST = [
    # 结构：{name, country, ghsl_ucdb_id}
    {"name": "Beijing", "country": "CHN", "ucdb_id": None},
    {"name": "Nairobi", "country": "KEN", "ucdb_id": None},
]

# 文件名约定（仅示例，占位）
FILES = {
    "ghsl_ucdb": RAW_DIR / "ghsl_ucdb.gpkg",
    "ghsl_smod": RAW_DIR / "ghsl_smod.tif",
    "ghs_pop": RAW_DIR / "ghs_pop.tif",
    "worldcover": RAW_DIR / "worldcover_2021.tif",
    "cgls_lc100": RAW_DIR / "cgls_lc100_2015_2019.tif",
    "landsat_ndvi": RAW_DIR / "landsat_ndvi_annual.tif",
    "hansen_gfc": RAW_DIR / "hansen_gfc.tif",
    "gedi": RAW_DIR / "gedi_l4a.gpkg",
    "viirs_vnl": RAW_DIR / "viirs_annual_v2_2021.tif",
    "osm_roads": RAW_DIR / "osm_roads.gpkg",
    "no2": RAW_DIR / "tropomi_no2.tif",
    "pm25": RAW_DIR / "global_pm25.tif",
    "ipums_mobility": RAW_DIR / "ipums_od.csv",
    "idmc_disasters": RAW_DIR / "idmc_events.csv",
    "emdat": RAW_DIR / "emdat_events.csv",
    "gtfs": RAW_DIR / "gtfs_feeds.zip",
    "ebird_ebd": RAW_DIR / "ebd_region.txt.gz",
    "gbif_occ": RAW_DIR / "gbif_occ.csv",
}

# 输出文件（示例）
OUTPUTS = {
    "strata_gpkg": INTERIM_DIR / "strata.gpkg",
    "mediators_parquet": PROCESSED_DIR / "mediators.parquet",
    "biodiv_parquet": PROCESSED_DIR / "biodiversity.parquet",
    "effects_parquet": PROCESSED_DIR / "effects.parquet",
}

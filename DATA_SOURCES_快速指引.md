# 开源数据“零账号”与“需注册”清单（快速下载指引）

## 无需注册（Zero-login）
- **GHSL（城市/分级/人口）**：JRC 官方下载页与 FTP（按产品/年份/分辨率/瓦片提供）
  - 入口页（含“按瓦片下载”说明）：https://human-settlement.emergency.copernicus.eu/download.php
  - 公开 FTP 根目录（示例，人口 GHS-POP R2023A）：https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/
- **ESA WorldCover 10 m（2021 v200）**：AWS 开放桶（COG，支持 `--no-sign-request`）
  - Registry 说明：`s3://esa-worldcover`（可直接列桶/读取）; STAC 端点：https://services.terrascope.be/stac
- **OSM 道路**：Overpass API 或 Geofabrik PBF，无需注册
- **GBIF 物种出现记录**：开放 API（`pygbif`），匿名可查小批量结果

## 需免费注册（推荐补齐“干扰/夜光/NO₂/PM₂.₅”等）
- **VIIRS 夜光（EOG Annual VNL v2/v2.1）**：EOG 官网注册后下载
- **TROPOMI NO₂（年均 L3 栅格）**：NASA GES DISC / S5P PAL（Earthdata 免费账号）
- **ACAG 全球 PM₂.₅（V5/V6）**：华盛顿大学 ACAG 官网直接下载

> 详细链接请见聊天记录中的引用；脚手架 README 也会逐步补充。

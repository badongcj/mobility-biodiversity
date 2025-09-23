# 移动性-生物多样性（Python 全流程脚手架）

> 目标：用 **Python（含中文注释）** 复现《结果》所需 5 幅图（每幅多子图），并给出可扩展的数据处理与建模代码。

## 图件与数据（一览）

- **图1（暴露与研究设计）**：城市—城郊—农村分层、O–D 流（迁移/流动）网络、样本覆盖、平行趋势与安慰剂检验  
  **数据**：  
  - 城市与分层：**GHSL GHS-UCDB / SMOD / FUA**；人口栅格：**GHS-POP 或 WorldPop**  
  - 移动性：**IPUMS 国际人口普查（前居住地）**；事件冲击：**IDMC/EM-DAT**（灾害致迁移）、**Transit 开通**（GTFS）  
- **图2（流入地：城郊/城市的中介机制）**：栖息地数量与构型（连通性等）、人类干扰（夜光、道路/交通、NO₂/PM₂.₅）对多样性的中介作用  
  **数据**：陆覆（WorldCover/CGLS）、植被指数（Landsat/HLS NDVI）、森林变化（Hansen）、树冠/结构（GEDI，可选）；  
  夜光（VIIRS）、道路（OSM）、NO₂（Sentinel-5P）、PM₂.₅（全球产品）；  
  生物多样性（eBird、GBIF、Wildlife Insights）
- **图3（流出地：农村“外出—撂荒/集约化”分化）**：田块边界/树篱、道路增长、夜光增幅阈值对多样性的影响与时滞  
- **图4（系统分解与均质化）**：起点（农村）+ 终点（城市）净效应分解；β 多样性（周转/嵌套）、功能/系统发育多样性  
- **图5（政策情景）**：**成对**（农村+城市）干预（连通绿蓝网络 + 干扰削减）下的可恢复多样性与成本粗评

> 注：本脚手架只给出 **开源数据名称与处理接口**；部分数据（如 eBird EBD、IPUMS 提取）需注册或线下下载后放入 `data/raw/`。

## 环境安装

```bash
conda create -n mobiodiv python=3.11 -y
conda activate mobiodiv

# 基础科学计算 + 地理空间 + 因果/面板 + 绘图
 pip install -r requirements.txt
```

## 命令行入口（可选）

安装依赖后，可通过 `python -m mobiodiv` 调用集成入口，例如：

```bash
# 查看脚本列表
python -m mobiodiv list-scripts

# 直接执行开源数据拉取脚本
python -m mobiodiv fetch-open-data --place "Singapore" --buffer-km 20
```

## 快速开始（建议顺序）

1. **放数据**：将下载的原始数据放入 `data/raw/`（文件名可在 `src/mobiodiv/config.py` 中配置）。
2. **生成分层**：运行 `python scripts/01_build_strata.py`（城市-城郊-农村掩膜 + 人口权重）。
3. **处理中介**：`python scripts/02_build_mediators.py`（栖息地/连通性、干扰指数）。
4. **生物数据**：`python scripts/03_build_biodiversity.py`（eBird/GBIF 读取、占据模型/校正、群落矩阵）。
5. **建模估计**：`python scripts/04_models_effects.py`（DiD、分解/中介、阈值/时滞）。
6. **情景模拟**：`python scripts/05_counterfactuals.py`（走廊与干扰削减）。
7. **出图**：`python scripts/06_make_figures.py`（一次性绘制图1–图5）。

## 重要说明

- **纯 Python**：本项目尽量使用 Python 生态（`geopandas/rioxarray/rasterio/pylandstats/linearmodels/pymc` 等）。
- **复现性**：所有中间结果写入 `data/interim/`，分析就绪数据写入 `data/processed/`，图片和表格写入 `outputs/`。
- **占据模型**：Python 中可用 `pymc` 实现（已给出模板）；若你更熟悉 R，可后续用 `rpy2` 接 R 包替换。
- **注释**：全部关键代码段提供中文注释与“替换为你路径”的 TODO 提示。

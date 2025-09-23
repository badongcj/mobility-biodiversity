"""项目命令行入口（Typer 应用）。

提供对 ``scripts`` 目录下常用脚本的统一封装，
便于通过 ``python -m mobiodiv`` 在命令行中执行。
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Dict

import typer
from rich.console import Console


app = typer.Typer(help="MobioDiv 数据处理与建模脚手架的命令行入口。")
console = Console()


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"
_LOADED_SCRIPTS: Dict[str, ModuleType] = {}


def _load_script_module(script_filename: str) -> ModuleType:
    """按需载入 ``scripts`` 目录下的脚本模块。"""

    script_path = SCRIPTS_DIR / script_filename
    if not script_path.exists():
        raise typer.BadParameter(f"未找到脚本：{script_filename}")

    module_name = f"_mobiodiv_script_{script_path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载脚本 {script_filename}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[assignment]
    return module


def _get_script_module(script_filename: str) -> ModuleType:
    """获取（并缓存）脚本模块。"""

    if script_filename not in _LOADED_SCRIPTS:
        _LOADED_SCRIPTS[script_filename] = _load_script_module(script_filename)
    return _LOADED_SCRIPTS[script_filename]


@app.command("fetch-open-data")
def fetch_open_data(
    place: str = typer.Argument(..., help="地名（例如：Singapore、Beijing、Nairobi）"),
    buffer_km: float = typer.Option(20.0, "--buffer-km", "-b", help="缓冲距离（km）"),
) -> None:
    """零账号地理开源数据快速拉取。"""

    module = _get_script_module("00_fetch_open_data.py")
    if not hasattr(module, "run"):
        console.print("脚本缺少 run() 函数，无法通过入口调用。")
        raise typer.Exit(code=1)

    module.run(place=place, buffer_km=buffer_km)  # type: ignore[attr-defined]


@app.command("list-scripts")
def list_scripts() -> None:
    """列出 ``scripts`` 目录下可执行的脚本。"""

    scripts = sorted(path.name for path in SCRIPTS_DIR.glob("*.py"))
    if not scripts:
        console.print("[yellow]尚未找到任何脚本。[/yellow]")
        return

    console.print("可用脚本：")
    for script in scripts:
        console.print(f"  - {script}")


def main() -> None:
    """Typer 应用入口。"""

    app()


if __name__ == "__main__":
    main()

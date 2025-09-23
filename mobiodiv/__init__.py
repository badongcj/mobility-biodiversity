"""轻量包装，允许直接 ``import mobiodiv``。"""

from __future__ import annotations

from pathlib import Path


_PKG_DIR = Path(__file__).resolve().parent.parent / "src" / "mobiodiv"
__path__ = [str(_PKG_DIR)]

_init_file = _PKG_DIR / "__init__.py"
if _init_file.exists():
    exec(_init_file.read_text(encoding="utf-8"), globals())

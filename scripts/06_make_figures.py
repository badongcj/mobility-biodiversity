# -*- coding: utf-8 -*-
"""脚本6：统一出图（图1–图5）"""
from pathlib import Path
from mobiodiv.viz.fig1 import make_fig1
from mobiodiv.viz.fig2 import make_fig2
from mobiodiv.viz.fig3 import make_fig3
from mobiodiv.viz.fig4 import make_fig4
from mobiodiv.viz.fig5 import make_fig5
from mobiodiv.config import FIG_DIR

if __name__ == "__main__":
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    make_fig1(out_path=FIG_DIR/'fig1.png')
    make_fig2().savefig(FIG_DIR/'fig2.png', bbox_inches='tight', dpi=200)
    make_fig3().savefig(FIG_DIR/'fig3.png', bbox_inches='tight', dpi=200)
    make_fig4().savefig(FIG_DIR/'fig4.png', bbox_inches='tight', dpi=200)
    make_fig5().savefig(FIG_DIR/'fig5.png', bbox_inches='tight', dpi=200)
    print(f"图件已写入：{FIG_DIR}")

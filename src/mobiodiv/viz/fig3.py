# -*- coding: utf-8 -*-
"""图3：流出地（农村）分化（示例）"""
import matplotlib.pyplot as plt

def make_fig3():
    fig = plt.figure(figsize=(8, 6), dpi=200)
    ax = fig.add_subplot(111)
    ax.text(0.5, 0.5, 'Fig. 3 占位：农村类型分化', ha='center', va='center')
    ax.set_axis_off()
    return fig

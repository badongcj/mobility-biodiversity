# -*- coding: utf-8 -*-
"""图5：政策情景（示例）"""
import matplotlib.pyplot as plt

def make_fig5():
    fig = plt.figure(figsize=(8, 6), dpi=200)
    ax = fig.add_subplot(111)
    ax.text(0.5, 0.5, 'Fig. 5 占位：政策情景', ha='center', va='center')
    ax.set_axis_off()
    return fig

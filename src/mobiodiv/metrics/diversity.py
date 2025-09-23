# -*- coding: utf-8 -*-
"""多样性指标：α、β（周转/嵌套）、功能/系统发育（基于 scikit-bio 的示例）"""
import numpy as np
import pandas as pd
from skbio.diversity import alpha_diversity, beta_diversity
from skbio.tree import TreeNode
from skbio import DistanceMatrix

def compute_alpha(count_matrix: np.ndarray, metric='shannon'):
    """alpha 多样性（对每个样方/分层单元）"""
    return alpha_diversity(metric=metric, counts=count_matrix, ids=[f'site_{i}' for i in range(count_matrix.shape[0])])

def compute_beta(count_matrix: np.ndarray, metric='braycurtis'):
    """beta 多样性（场地两两之间），返回距离矩阵"""
    dm = beta_diversity(metric=metric, counts=count_matrix, ids=[f'site_{i}' for i in range(count_matrix.shape[0])])
    return dm

def phylogenetic_diversity(count_matrix: np.ndarray, tree_newick: str):
    """系统发育多样性（Faith's PD 等，可按需扩展）
    注意：需要物种-树端点的一致性与树校正。
    """
    tree = TreeNode.read([tree_newick])
    # TODO: 实现 PD 计算逻辑（此处留空，建议后续补充或使用现成函数）
    return None

# -*- coding: utf-8 -*-
"""IO 工具函数（下载、解压、缓存等）"""
from pathlib import Path
import requests
from tqdm import tqdm
import zipfile
import tarfile

def download_file(url: str, out_path: Path, chunk: int = 1<<20):
    """下载大文件（支持断点续传）。需要你提供合法的 URL。
    参数:
      url: 下载地址
      out_path: 输出路径
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    headers = {}
    pos = 0
    if out_path.exists():
        pos = out_path.stat().st_size
        headers['Range'] = f'bytes={pos}-'
    with requests.get(url, stream=True, headers=headers, timeout=60) as r:
        r.raise_for_status()
        mode = 'ab' if pos>0 else 'wb'
        total = int(r.headers.get('Content-Length', 0)) + pos
        with open(out_path, mode) as f, tqdm(total=total, initial=pos, unit='B', unit_scale=True, desc=out_path.name) as pbar:
            for chunk_bytes in r.iter_content(chunk_size=chunk):
                if chunk_bytes:
                    f.write(chunk_bytes)
                    pbar.update(len(chunk_bytes))
    return out_path

def extract_any(archive_path: Path, out_dir: Path):
    """解压 zip/tar.gz 等常见归档"""
    out_dir.mkdir(parents=True, exist_ok=True)
    if archive_path.suffix == '.zip':
        with zipfile.ZipFile(archive_path, 'r') as zf:
            zf.extractall(out_dir)
    elif archive_path.suffixes[-2:] == ['.tar', '.gz'] or archive_path.suffix == '.tgz':
        with tarfile.open(archive_path, 'r:gz') as tf:
            tf.extractall(out_dir)
    else:
        raise ValueError(f"不支持的压缩格式: {archive_path}")
    return out_dir

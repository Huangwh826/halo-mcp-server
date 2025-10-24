"""Version management utilities."""

import os
from pathlib import Path


def get_version() -> str:
    """
    从 version.txt 文件读取版本号

    Returns:
        str: 版本号字符串，如 "0.1.2"
    """
    # 获取项目根目录
    # 当前文件: src/halo_mcp_server/_version.py
    # 根目录: 向上两级
    current_file = Path(__file__)
    root_dir = current_file.parent.parent.parent
    version_file = root_dir / "version.txt"

    try:
        if version_file.exists():
            version = version_file.read_text(encoding="utf-8").strip()
            return version
        else:
            # 如果找不到 version.txt，返回默认版本
            return "0.0.0"
    except Exception as e:
        # 如果读取失败，返回默认版本
        print(f"Warning: Failed to read version from {version_file}: {e}")
        return "0.0.0"


# 模块级别的版本号，方便直接导入
__version__ = get_version()

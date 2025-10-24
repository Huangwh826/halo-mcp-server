#!/usr/bin/env python3
"""版本号管理工具"""

import sys
from pathlib import Path


def get_current_version() -> str:
    """获取当前版本号"""
    version_file = Path(__file__).parent / "version.txt"
    return version_file.read_text(encoding="utf-8").strip()


def update_version(new_version: str) -> None:
    """更新版本号"""
    version_file = Path(__file__).parent / "version.txt"
    version_file.write_text(new_version + "\n", encoding="utf-8")
    print(f"✓ 版本号已更新: {new_version}")


def bump_version(part: str = "patch") -> str:
    """
    自动升级版本号
    
    Args:
        part: 要升级的部分 - "major", "minor", 或 "patch"
    
    Returns:
        新版本号
    """
    current = get_current_version()
    major, minor, patch = map(int, current.split("."))
    
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid part: {part}. Must be 'major', 'minor', or 'patch'")
    
    new_version = f"{major}.{minor}.{patch}"
    update_version(new_version)
    return new_version


def main():
    """主函数"""
    if len(sys.argv) == 1:
        # 显示当前版本
        current = get_current_version()
        print(f"当前版本: {current}")
        print("\n用法:")
        print("  python update_version.py              # 显示当前版本")
        print("  python update_version.py 0.2.0        # 设置指定版本")
        print("  python update_version.py patch        # 升级修订号 (0.1.0 → 0.1.1)")
        print("  python update_version.py minor        # 升级次版本号 (0.1.0 → 0.2.0)")
        print("  python update_version.py major        # 升级主版本号 (0.1.0 → 1.0.0)")
        return
    
    arg = sys.argv[1]
    
    if arg in ["major", "minor", "patch"]:
        # 自动升级
        old_version = get_current_version()
        new_version = bump_version(arg)
        print(f"✓ 版本号已从 {old_version} 升级到 {new_version}")
    else:
        # 手动设置
        old_version = get_current_version()
        update_version(arg)
        print(f"✓ 版本号已从 {old_version} 设置为 {arg}")
    
    new_version = get_current_version()
    print("\n📝 后续步骤:")
    print("1. 检查 version.txt 文件")
    print("2. 运行: pip install -e . (测试安装)")
    print(f"3. 提交代码: git add version.txt && git commit -m 'Bump version to {new_version}'")
    print(f"4. 创建标签: git tag -a v{new_version} -m 'Release version {new_version}'")


if __name__ == "__main__":
    main()
#!/bin/bash
# Halo MCP Server 发布脚本 (Linux/macOS)
# 用于打包并发布到 PyPI

set -e  # 遇到错误立即退出

echo "============================================"
echo "Halo MCP Server - PyPI 发布脚本"
echo "============================================"
echo ""

# 检查是否在虚拟环境中
if [ -z "$VIRTUAL_ENV" ]; then
    echo "[警告] 未检测到虚拟环境，建议在虚拟环境中执行"
    echo ""
    read -p "是否继续? (y/n): " continue
    if [ "$continue" != "y" ]; then
        echo "已取消"
        exit 1
    fi
fi

echo "[1/7] 清理旧的构建文件..."
rm -rf dist build src/*.egg-info
echo "✓ 清理完成"
echo ""

echo "[2/7] 安装/更新构建工具..."
python -m pip install --upgrade pip
python -m pip install --upgrade build twine setuptools wheel
echo "✓ 构建工具安装完成"
echo ""

echo "[3/7] 运行代码检查..."
pip install ruff black isort mypy 2>/dev/null || true
echo "- 代码格式检查 (Black)..."
if ! python -m black --check src/; then
    echo "[警告] 代码格式不符合规范，建议运行: black src/"
    read -p "是否继续? (y/n): " continue
    if [ "$continue" != "y" ]; then
        exit 1
    fi
fi
echo "✓ 代码检查通过"
echo ""

echo "[4/7] 构建 Python 包..."
python -m build
echo "✓ 构建成功"
echo ""

echo "[5/7] 检查构建的包..."
python -m twine check dist/*
echo "✓ 包检查通过"
echo ""

echo "============================================"
echo "构建完成！"
echo ""
echo "生成的文件:"
ls -lh dist/
echo ""
echo "============================================"
echo ""

echo "[6/7] 选择发布目标"
echo "  1. TestPyPI (测试环境，推荐先测试)"
echo "  2. PyPI (正式环境)"
echo "  3. 跳过上传，仅构建"
echo ""
read -p "请选择 (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "[7/7] 上传到 TestPyPI..."
        echo ""
        echo "请确保已设置 TestPyPI Token:"
        echo "  https://test.pypi.org/manage/account/token/"
        echo ""
        python -m twine upload --repository testpypi dist/*
        echo ""
        echo "✓ 成功上传到 TestPyPI！"
        echo ""
        echo "安装测试:"
        echo "  pip install --index-url https://test.pypi.org/simple/ halo-mcp-server"
        echo ""
        ;;
    2)
        echo ""
        echo "[7/7] 上传到 PyPI..."
        echo ""
        echo "⚠️  警告：即将发布到正式 PyPI"
        echo ""
        echo "请确保:"
        echo "  1. 已在 TestPyPI 测试成功"
        echo "  2. 版本号已更新 (当前: pyproject.toml)"
        echo "  3. 已设置 PyPI Token: https://pypi.org/manage/account/token/"
        echo ""
        read -p "确认发布到正式 PyPI? (yes/no): " confirm
        if [ "$confirm" != "yes" ]; then
            echo "已取消"
            exit 1
        fi
        echo ""
        python -m twine upload dist/*
        echo ""
        echo "✓ 成功发布到 PyPI！"
        echo ""
        echo "用户现在可以通过以下命令安装:"
        echo "  pip install halo-mcp-server"
        echo ""
        echo "查看项目页面:"
        echo "  https://pypi.org/project/halo-mcp-server/"
        echo ""
        ;;
    3)
        echo ""
        echo "✓ 构建完成，已跳过上传"
        echo ""
        echo "如需手动上传，使用:"
        echo "  # 测试环境"
        echo "  python -m twine upload --repository testpypi dist/*"
        echo ""
        echo "  # 正式环境"
        echo "  python -m twine upload dist/*"
        echo ""
        ;;
    *)
        echo "无效的选择"
        exit 1
        ;;
esac

echo "============================================"
echo "完成！"
echo "============================================"

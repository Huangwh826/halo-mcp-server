# 📝 版本号管理指南

## 🎯 概述

本项目采用 **统一版本号管理方案**，通过 `version.txt` 文件作为唱一的版本号来源，确保所有使用场景中的版本号保持一致。

## 📚 版本号来源

### 单一来源 (Single Source of Truth)

```
version.txt  ← 唯一的版本号来源
     │
     ├──→ pyproject.toml (通过 tool.setuptools.dynamic 读取)
     ├──→ __init__.py (通过 _version.py 读取)
     ├──→ PyPI 包 (打包时读取)
     ├──→ pip show 输出 (安装后显示)
     └──→ README.md 徽章 (使用 PyPI 动态徽章)
```

### 版本号使用位置

| 位置 | 文件 | 读取方式 | 自动更新 |
|------|------|----------|----------|
| **主文件** | `version.txt` | - | 手动/脚本 |
| **构建配置** | `pyproject.toml` | `tool.setuptools.dynamic` | ✅ 自动 |
| **Python 模块** | `_version.py` | 读取 `version.txt` | ✅ 自动 |
| **包入口** | `__init__.py` | 导入 `_version.py` | ✅ 自动 |
| **PyPI 包** | 打包结果 | setuptools 读取 | ✅ 自动 |
| **安装信息** | `pip show` | 安装元数据 | ✅ 自动 |
| **README 徽章** | `README.md` | PyPI 动态徽章 | ✅ 自动 |

## 🔧 使用方法

### 1️⃣ 查看当前版本

```bash
# 方法 1: 使用版本管理脚本
python update_version.py

# 方法 2: 直接查看文件
cat version.txt
# Windows:
type version.txt

# 方法 3: 查看已安装的版本
python -c "import halo_mcp_server; print(halo_mcp_server.__version__)"
```

### 2️⃣ 更新版本号

#### 方法 A: 使用版本管理脚本 (推荐)

```bash
# 自动升级修订号 (0.1.2 → 0.1.3)
python update_version.py patch

# 自动升级次版本号 (0.1.2 → 0.2.0)
python update_version.py minor

# 自动升级主版本号 (0.1.2 → 1.0.0)
python update_version.py major

# 手动设置指定版本
python update_version.py 0.3.0
```

**脚本输出示例**：
```
✓ 版本号已从 0.1.2 升级到 0.1.3

📝 后续步骤:
1. 检查 version.txt 文件
2. 运行: pip install -e . (测试安装)
3. 提交代码: git add version.txt && git commit -m 'Bump version to 0.1.3'
4. 创建标签: git tag -a v0.1.3 -m 'Release version 0.1.3'
```

#### 方法 B: 直接编辑文件

```bash
# Linux/macOS
echo "0.2.0" > version.txt

# Windows PowerShell
Set-Content version.txt "0.2.0"

# Windows CMD
echo 0.2.0 > version.txt
```

### 3️⃣ 验证版本号

```bash
# 安装开发版本
pip install -e .

# 验证版本号
python -c "import halo_mcp_server; print(halo_mcp_server.__version__)"

# 查看包信息
pip show halo-mcp-server
```

## 📦 发布流程

### 完整发布步骤

```bash
# 1. 更新版本号
python update_version.py minor  # 或 patch/major

# 2. 测试安装
pip install -e .
python -c "import halo_mcp_server; print(halo_mcp_server.__version__)"

# 3. 提交更改
VERSION=$(cat version.txt)
git add version.txt
git commit -m "Bump version to $VERSION"

# 4. 创建 Git 标签
git tag -a v$VERSION -m "Release version $VERSION"

# 5. 推送到远程
git push origin main
git push origin v$VERSION

# 6. 构建发布包
python -m build

# 7. 检查构建结果
python -m twine check dist/*

# 8. 上传到 PyPI (正式环境)
python -m twine upload dist/*

# 或者先上传到测试环境
python -m twine upload --repository testpypi dist/*
```

### Windows PowerShell 版本

```powershell
# 1. 更新版本号
python update_version.py minor

# 2. 测试安装
pip install -e .
python -c "import halo_mcp_server; print(halo_mcp_server.__version__)"

# 3. 提交更改
$VERSION = Get-Content version.txt
git add version.txt
git commit -m "Bump version to $VERSION"

# 4. 创建 Git 标签
git tag -a v$VERSION -m "Release version $VERSION"

# 5. 推送到远程
git push origin main
git push origin v$VERSION

# 6. 构建发布包
python -m build

# 7. 检查构建结果
python -m twine check dist/*

# 8. 上传到 PyPI
python -m twine upload dist/*
```

## 📁 文件说明

### version.txt

**位置**：`d:\Project\halo-mcp-server\version.txt`

**格式**：
```
0.1.2
```

**规则**：
- 单行纯文本
- 遵循语义化版本号 (Semantic Versioning): `MAJOR.MINOR.PATCH`
- 使用 LF 换行符 (通过 `.gitattributes` 配置)

### _version.py

**位置**：`src/halo_mcp_server/_version.py`

**功能**：
- 提供 `get_version()` 函数读取 `version.txt`
- 导出 `__version__` 变量供包使用
- 处理文件不存在的情况（返回 "0.0.0"）

**示例**：
```python
from halo_mcp_server._version import __version__
print(__version__)  # 输出: 0.1.2
```

### __init__.py

**位置**：`src/halo_mcp_server/__init__.py`

**修改**：
```python
# 从直接定义
__version__ = "0.1.2"

# 改为从 _version.py 导入
from halo_mcp_server._version import __version__
```

### pyproject.toml

**位置**：`d:\Project\halo-mcp-server\pyproject.toml`

**关键配置**：
```toml
[project]
name = "halo-mcp-server"
dynamic = ["version"]  # 声明版本号为动态
# version = "0.1.2"  # 删除静态版本号

[tool.setuptools.dynamic]
version = {file = "version.txt"}  # 指定从 version.txt 读取
```

### update_version.py

**位置**：`d:\Project\halo-mcp-server\update_version.py`

**功能**：
- 查看当前版本：`python update_version.py`
- 自动升级：`python update_version.py patch|minor|major`
- 手动设置：`python update_version.py 0.2.0`
- 显示后续步骤提示

### MANIFEST.in

**位置**：`d:\Project\halo-mcp-server\MANIFEST.in`

**增加**：
```
include version.txt  # 确保 version.txt 被打包
```

### .gitattributes

**位置**：`d:\Project\halo-mcp-server\.gitattributes`

**配置**：
```
# version.txt 应该使用 LF 换行符
version.txt text eol=lf
```

## 📊 版本号规则

### 语义化版本号 (Semantic Versioning)

格式：`MAJOR.MINOR.PATCH`

- **MAJOR** (主版本号)：不兼容的 API 修改
  - 示例：`0.1.2 → 1.0.0`
  - 命令：`python update_version.py major`

- **MINOR** (次版本号)：向下兼容的功能性新增
  - 示例：`0.1.2 → 0.2.0`
  - 命令：`python update_version.py minor`

- **PATCH** (修订号)：向下兼容的问题修正
  - 示例：`0.1.2 → 0.1.3`
  - 命令：`python update_version.py patch`

### 版本号升级场景

| 场景 | 版本类型 | 示例 |
|------|----------|------|
| 修复 Bug | PATCH | 0.1.2 → 0.1.3 |
| 性能优化 | PATCH | 0.1.2 → 0.1.3 |
| 文档更新 | PATCH | 0.1.2 → 0.1.3 |
| 新增功能 | MINOR | 0.1.2 → 0.2.0 |
| 新增 API | MINOR | 0.1.2 → 0.2.0 |
| 增强现有功能 | MINOR | 0.1.2 → 0.2.0 |
| 不兼容修改 | MAJOR | 0.1.2 → 1.0.0 |
| API 破坏性变更 | MAJOR | 0.1.2 → 1.0.0 |
| 重大重构 | MAJOR | 0.1.2 → 1.0.0 |

## ✅ 验证清单

在更新版本号后，请验证以下项：

- [ ] `version.txt` 内容正确
- [ ] `python update_version.py` 显示正确的版本
- [ ] `pip install -e .` 安装成功
- [ ] `python -c "import halo_mcp_server; print(halo_mcp_server.__version__)"` 输出正确
- [ ] `pip show halo-mcp-server` 显示正确的版本
- [ ] `python -m build` 构建成功
- [ ] 构建的包文件名包含正确的版本号
- [ ] Git 标签与版本号一致

## 🐞 故障排除

### 问题 1：版本号不一致

**症状**：`pip show` 显示的版本与 `version.txt` 不同

**解决**：
```bash
# 重新安装
pip uninstall halo-mcp-server -y
pip install -e .
```

### 问题 2：打包时找不到 version.txt

**症状**：构建失败，提示找不到 version.txt

**解决**：
1. 检查 `MANIFEST.in` 是否包含 `include version.txt`
2. 检查 `version.txt` 是否在项目根目录
3. 清理构建缓存：`rm -rf dist/ build/ *.egg-info`

### 问题 3：ImportError

**症状**：`ImportError: cannot import name '__version__' from 'halo_mcp_server'`

**解决**：
1. 检查 `_version.py` 是否存在
2. 检查 `__init__.py` 是否正确导入
3. 重新安装：`pip install -e .`

### 问题 4：Git 换行符问题

**症状**：version.txt 在不同系统上换行符不一致

**解决**：
1. 确保 `.gitattributes` 包含 `version.txt text eol=lf`
2. 重新规范化文件：
   ```bash
   git rm --cached version.txt
   git add version.txt
   git commit -m "Normalize version.txt line endings"
   ```

## 💡 最佳实践

1. **始终使用脚本**：使用 `update_version.py` 而不是手动编辑
2. **发布前测试**：在每次发布前运行 `pip install -e .` 验证
3. **Git 标签**：每次发布都创建对应的 Git 标签
4. **保持一致**：Git 标签名应与版本号一致 (`v0.1.2`)
5. **语义化版本**：遵循 Semantic Versioning 规范
6. **变更日志**：在 CHANGELOG.md 中记录每次版本更新

## 🔗 相关链接

- [Semantic Versioning 2.0.0](https://semver.org/lang/zh-CN/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [setuptools Documentation](https://setuptools.pypa.io/)
- [Git Tagging](https://git-scm.com/book/zh/v2/Git-%E5%9F%BA%E7%A1%80-%E6%89%93%E6%A0%87%E7%AD%BE)

---

**最后更新**：2025-10-24
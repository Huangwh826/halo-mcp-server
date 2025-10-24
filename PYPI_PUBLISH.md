# 🚀 PyPI 发布完整指南

本文档详细说明如何将 Halo MCP Server 发布到 PyPI。

> 💡 **快速发布**:如果你只想快速发布,直接跳到 [自动化发布脚本](#自动化发布脚本) 部分  
> 📚 **首次发布**:建议完整阅读本文档,了解完整的发布流程

---

## 📋 目录

- [快速开始](#快速开始)
  - [自动化发布脚本](#自动化发布脚本)
  - [5分钟快速发布](#5分钟快速发布)
- [前置准备](#前置准备)
  - [注册 PyPI 账号](#1-注册-pypi-账号)
  - [生成 API Token](#2-生成-api-token)
  - [配置认证信息](#3-配置认证信息)
  - [安装发布工具](#4-安装发布工具)
- [版本号管理](#版本号管理)
- [手动发布流程](#手动发布流程)
- [发布检查清单](#发布检查清单)
- [故障排除](#故障排除)
- [高级配置](#高级配置)
- [参考资源](#参考资源)

---

## 快速开始

### 自动化发布脚本

项目提供了自动化发布脚本,可一键完成从构建到发布的全部流程。

#### Windows

```powershell
# 1. 激活虚拟环境（如果使用）
.\venv\Scripts\activate

# 2. 运行发布脚本
.\publish.bat
```

#### Linux/macOS

```bash
# 1. 激活虚拟环境（如果使用）
source venv/bin/activate

# 2. 添加执行权限（首次运行）
chmod +x publish.sh

# 3. 运行发布脚本
./publish.sh
```

#### 脚本功能特性

发布脚本会自动完成以下步骤:

```
[1/7] ✅ 清理旧的构建文件
[2/7] ✅ 安装/更新构建工具（build, twine, setuptools, wheel）
[3/7] ✅ 运行代码格式检查（Black）
[4/7] ✅ 构建 Python 包（wheel + tar.gz）
[5/7] ✅ 检查包的完整性（twine check）
[6/7] ✅ 交互式选择发布目标（TestPyPI / PyPI / 仅构建）
[7/7] ✅ 上传到选定的目标仓库
```

**优势**:
- ✅ 自动化流程,减少人为错误
- ✅ 内置检查和验证步骤
- ✅ 支持 TestPyPI 测试环境
- ✅ 跨平台支持（Windows / Linux / macOS）

---

### 5分钟快速发布

**适合人群**:已完成前置准备,需要快速发布新版本

#### 步骤 1: 更新版本号

```bash
# 使用版本管理脚本（推荐）
python update_version.py patch   # 0.1.3 → 0.1.4 (Bug修复)
python update_version.py minor   # 0.1.3 → 0.2.0 (新功能)
python update_version.py major   # 0.1.3 → 1.0.0 (重大更新)

# 或手动设置版本号
python update_version.py 0.2.0
```

> 📝 项目使用 `version.txt` 统一管理版本号,详见 [版本号管理](#版本号管理)

#### 步骤 2: 运行发布脚本

```bash
# Windows
.\publish.bat

# Linux/macOS
./publish.sh
```

#### 步骤 3: 选择发布目标

脚本会提示选择:
```
[6/7] 选择发布目标
  1. TestPyPI (测试环境,推荐先测试)
  2. PyPI (正式环境)
  3. 跳过上传,仅构建
```

**推荐流程**:
1. 首次发布 → 选择 **1 (TestPyPI)** 测试
2. 测试成功 → 再次运行脚本,选择 **2 (PyPI)** 正式发布

#### 步骤 4: 输入认证信息

```
Username: __token__
Password: [粘贴你的 PyPI Token]
```

> 💡 **提示**:如果已配置 `.pypirc` 文件,会自动使用,无需手动输入

#### 步骤 5: 验证发布

```bash
# 查看 PyPI 页面
https://pypi.org/project/halo-mcp-server/

# 测试安装
pip install halo-mcp-server --upgrade

# 验证版本
pip show halo-mcp-server
```

✅ **完成!** 新版本已成功发布到 PyPI

---

## 前置准备

> ⚠️ **首次发布必读**:在使用发布脚本之前,需要先完成以下准备工作

### 1. 注册 PyPI 账号

#### TestPyPI（测试环境）
1. 访问:https://test.pypi.org/account/register/
2. 注册账号并验证邮箱
3. 用于测试发布流程,不影响正式环境

#### PyPI（正式环境）
1. 访问:https://pypi.org/account/register/
2. 注册账号并验证邮箱
3. 正式发布的目标仓库

### 2. 生成 API Token

#### TestPyPI Token

1. 登录 TestPyPI:https://test.pypi.org/
2. 进入 **Account Settings** → **API tokens**
3. 点击 **"Add API token"**
4. 设置名称:`halo-mcp-server`
5. 范围:选择 **"Entire account"** 或特定项目
6. **复制并保存 Token**（仅显示一次,格式:`pypi-AgENdGVzdC5weXBpLm9yZw...`）

#### PyPI Token

1. 登录 PyPI:https://pypi.org/
2. 进入 **Account Settings** → **API tokens**
3. 点击 **"Add API token"**
4. 设置名称:`halo-mcp-server`
5. 范围:选择 **"Entire account"** 或特定项目
6. **复制并保存 Token**（仅显示一次,格式:`pypi-AgEIcHlwaS5vcmcC...`）

⚠️ **重要提示**:
- Token 仅显示一次,请妥善保存
- 建议使用密码管理器存储
- 如丢失需重新生成

### 3. 配置认证信息

#### 方法一:使用 .pypirc 文件（推荐）

**文件位置**:
- **Windows**: `%USERPROFILE%\.pypirc`
- **Linux/macOS**: `~/.pypirc`

**文件内容**:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC...  # 你的 PyPI Token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgENdGVzdC5weXBpLm9yZw...  # 你的 TestPyPI Token
```

**⚠️ 安全提示**:
- 文件权限设置为仅用户可读:`chmod 600 ~/.pypirc` (Linux/macOS)
- 不要提交此文件到 Git（`.pypirc` 已在 `.gitignore` 中）
- 定期更换 Token,提高安全性

#### 方法二:环境变量

```bash
# Windows (PowerShell)
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-AgEIcHlwaS5vcmcC..."

# Linux/macOS
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="pypi-AgEIcHlwaS5vcmcC..."
```

### 4. 安装发布工具

```bash
pip install --upgrade build twine setuptools wheel
```

**工具说明**:
- **build** - 构建现代 Python 包
- **twine** - 安全上传包到 PyPI
- **setuptools** - 打包工具
- **wheel** - 创建 wheel 格式分发包

> 💡 **提示**:发布脚本会自动安装这些工具,无需手动执行

---

## 版本号管理

Halo MCP Server 采用 **统一版本号管理方案**,通过 `version.txt` 作为唯一的版本号来源。

### 版本号来源架构

```
version.txt  ← 📌 唯一的版本号来源 (Single Source of Truth)
     │
     ├──→ pyproject.toml (通过 tool.setuptools.dynamic 动态读取)
     ├──→ __init__.py (通过 _version.py 读取)
     ├──→ PyPI 包 (打包时自动读取)
     └──→ pip show 输出 (安装后显示)
```

### 更新版本号

#### 使用版本管理脚本（推荐）

```bash
# 查看当前版本
python update_version.py

# 自动升级修订号 (0.1.3 → 0.1.4)
python update_version.py patch

# 自动升级次版本号 (0.1.3 → 0.2.0)
python update_version.py minor

# 自动升级主版本号 (0.1.3 → 1.0.0)
python update_version.py major

# 手动设置指定版本
python update_version.py 0.3.0
```

#### 脚本输出示例

```
✓ 版本号已从 0.1.3 升级到 0.1.4

📝 后续步骤:
1. 检查 version.txt 文件
2. 运行: pip install -e . (测试安装)
3. 提交代码: git add version.txt && git commit -m 'Bump version to 0.1.4'
4. 创建标签: git tag -a v0.1.4 -m 'Release version 0.1.4'
```

### 版本号规范（Semantic Versioning）

格式:`MAJOR.MINOR.PATCH`

| 版本类型 | 说明 | 场景示例 | 命令 |
|---------|------|---------|------|
| **PATCH** | 修订号 +1 | Bug修复、性能优化、文档更新 | `python update_version.py patch` |
| **MINOR** | 次版本号 +1 | 新增功能、增强现有功能 | `python update_version.py minor` |
| **MAJOR** | 主版本号 +1 | 不兼容的 API 修改、重大重构 | `python update_version.py major` |

**示例**:
- `0.1.3 → 0.1.4` - 修复了文章创建的Bug
- `0.1.4 → 0.2.0` - 新增附件管理功能
- `0.2.0 → 1.0.0` - 重构 API,不兼容旧版本

### 验证版本号

```bash
# 查看 version.txt
cat version.txt   # Linux/macOS
type version.txt  # Windows

# 测试安装并验证
pip install -e .
python -c "import halo_mcp_server; print(halo_mcp_server.__version__)"

# 查看包信息
pip show halo-mcp-server
```

> 📚 **详细文档**:查看 [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md) 了解版本管理的完整说明

---

## 手动发布流程

如果你想手动控制每一步,可以按照以下流程操作。

### 步骤 1: 更新版本号

```bash
# 使用版本管理脚本
python update_version.py minor  # 或 patch/major

# 验证版本号
cat version.txt  # Linux/macOS
type version.txt  # Windows
```

### 步骤 2: 更新文档

确保以下内容是最新的:
- [ ] `version.txt` 版本号正确
- [ ] `README.md` 功能特性描述准确
- [ ] 更新日志（如果有 `CHANGELOG.md`）
- [ ] 示例代码可用

### 步骤 3: 清理旧的构建文件

```bash
# Windows
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist src\halo_mcp_server.egg-info rmdir /s /q src\halo_mcp_server.egg-info

# Linux/macOS
rm -rf dist build src/*.egg-info
```

### 步骤 4: 运行测试（可选但推荐）

```bash
# 运行单元测试
pytest tests/ -v --cov=halo_mcp_server

# 代码格式检查
black --check src/
isort --check-only src/

# 类型检查
mypy src/

# 代码质量检查
ruff check src/
```

### 步骤 5: 构建包

```bash
python -m build
```

这会在 `dist/` 目录生成两个文件:
- `halo_mcp_server-0.1.3-py3-none-any.whl` (wheel 包)
- `halo_mcp_server-0.1.3.tar.gz` (源码包)

### 步骤 6: 检查构建的包

```bash
python -m twine check dist/*
```

**预期输出**:
```
Checking dist/halo_mcp_server-0.1.3-py3-none-any.whl: PASSED
Checking dist/halo_mcp_server-0.1.3.tar.gz: PASSED
```

### 步骤 7: 上传到 TestPyPI（推荐先测试）

```bash
python -m twine upload --repository testpypi dist/*
```

**输入凭据**（如果未配置 .pypirc）:
- Username: `__token__`（注意是两个下划线）
- Password: `pypi-AgENdGVzdC5weXBpLm9yZw...`（你的 TestPyPI Token）

**成功标志**:
```
Uploading distributions to https://test.pypi.org/legacy/
Uploading halo_mcp_server-0.1.3-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 49.1/49.1 kB
Uploading halo_mcp_server-0.1.3.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 116.6/116.6 kB

View at:
https://test.pypi.org/project/halo-mcp-server/0.1.3/
```

### 步骤 8: 测试安装

```bash
# 创建新的虚拟环境进行测试
python -m venv test_env

# Windows
.\test_env\Scripts\activate
# Linux/macOS
source test_env/bin/activate

# 从 TestPyPI 安装
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ halo-mcp-server

# 验证安装
python -c "import halo_mcp_server; print(halo_mcp_server.__version__)"

# 测试基本功能
python -m halo_mcp_server --help

# 退出测试环境
deactivate
```

**预期输出**:
```
Successfully installed halo-mcp-server-0.1.3
0.1.3
```

### 步骤 9: 上传到正式 PyPI

**⚠️ 重要提示**:
- 确保在 TestPyPI 测试成功
- PyPI 不允许重复上传相同版本
- 发布后无法撤销,只能上传新版本

```bash
python -m twine upload dist/*
```

**输入凭据**（如果未配置 .pypirc）:
- Username: `__token__`
- Password: `pypi-AgEIcHlwaS5vcmcC...`（你的 PyPI Token）

**成功标志**:
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading halo_mcp_server-0.1.3-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 49.1/49.1 kB
Uploading halo_mcp_server-0.1.3.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 116.6/116.6 kB

View at:
https://pypi.org/project/halo-mcp-server/0.1.3/
```

### 步骤 10: 验证发布

1. **查看 PyPI 页面:**
   ```
   https://pypi.org/project/halo-mcp-server/
   ```

2. **测试安装:**
   ```bash
   pip install halo-mcp-server --upgrade
   ```

3. **验证版本:**
   ```bash
   pip show halo-mcp-server
   python -c "import halo_mcp_server; print(halo_mcp_server.__version__)"
   ```

### 步骤 11: 创建 Git 标签

```bash
# 获取版本号
VERSION=$(cat version.txt)  # Linux/macOS
# Windows PowerShell: $VERSION = Get-Content version.txt

# 提交版本更新
git add version.txt
git commit -m "Bump version to $VERSION"

# 创建标签
git tag -a v$VERSION -m "Release version $VERSION"

# 推送到远程
git push origin main
git push origin v$VERSION
```

### 步骤 12: 在 GitHub 创建 Release（可选）

1. 访问:https://github.com/Huangwh826/halo-mcp-server/releases/new
2. 选择标签:`v0.1.3`
3. 填写发布标题和说明
4. 附加构建文件（可选）
5. 点击 **"Publish release"**

---

## 发布检查清单

发布前请检查以下事项,确保发布顺利:

### ✅ 代码质量

- [ ] 所有单元测试通过（`pytest tests/ -v`）
- [ ] 代码格式符合规范（`black --check src/`）
- [ ] 导入顺序正确（`isort --check-only src/`）
- [ ] 类型检查通过（`mypy src/`）
- [ ] 无明显的代码质量问题（`ruff check src/`）

### ✅ 文档

- [ ] `README.md` 内容完整且准确
- [ ] 版本号已更新（`version.txt`）
- [ ] 安装说明正确
- [ ] 示例代码可用
- [ ] `LICENSE` 文件存在
- [ ] 更新日志已更新（如果有）

### ✅ 配置文件

- [ ] `pyproject.toml` 配置正确
- [ ] 依赖项版本合理
- [ ] 分类器（classifiers）准确
- [ ] 项目 URL 正确
- [ ] `version.txt` 版本号正确

### ✅ 包内容

- [ ] 所有必要文件都包含在包中
- [ ] `MANIFEST.in` 配置正确（包含 `version.txt`）
- [ ] 没有包含敏感信息（Token、密码等）
- [ ] 测试文件和示例文件已排除（或适当包含）

### ✅ 版本管理

- [ ] 版本号遵循语义化版本规范（Semantic Versioning）
- [ ] 版本号在 PyPI 上尚未使用
- [ ] `version.txt` 文件格式正确（单行,无多余空格）
- [ ] Git 标签准备创建（`v0.1.3`）

### ✅ 测试

- [ ] 在 TestPyPI 测试成功
- [ ] 测试安装包可正常使用
- [ ] 依赖项能正确安装
- [ ] 基本功能验证通过

### ✅ 发布准备

- [ ] PyPI Token 已配置（`.pypirc` 或环境变量）
- [ ] 已清理旧的构建文件
- [ ] 构建包已通过 `twine check`
- [ ] 准备好发布说明

---

## 故障排除

### 问题 1: 版本号已存在

**错误信息:**
```
HTTPError: 400 Bad Request from https://upload.pypi.org/legacy/
File already exists.
```

**原因**:PyPI 不允许重复上传相同版本号的包

**解决方案:**
```bash
# 更新版本号
python update_version.py patch  # 或 minor/major

# 重新构建
rm -rf dist build src/*.egg-info
python -m build

# 重新上传
python -m twine upload dist/*
```

### 问题 2: 认证失败

**错误信息:**
```
HTTPError: 403 Forbidden from https://upload.pypi.org/legacy/
Invalid or non-existent authentication information.
```

**可能原因**:
- Token 错误或过期
- 用户名不是 `__token__`
- `.pypirc` 文件格式错误

**解决方案:**

1. **检查 Token 格式**:
   ```bash
   # 正确格式
   Username: __token__  # 两个下划线
   Password: pypi-AgEIcHlwaS5vcmcC...  # 完整 Token
   ```

2. **重新生成 Token**:
   - PyPI: https://pypi.org/manage/account/token/
   - TestPyPI: https://test.pypi.org/manage/account/token/

3. **检查 .pypirc 文件**:
   ```ini
   [pypi]
   username = __token__
   password = pypi-AgEI...  # 确保 Token 正确
   ```

4. **测试网络连接**:
   ```bash
   curl https://upload.pypi.org/
   ```

### 问题 3: 包检查失败

**错误信息:**
```
warning: check: missing required meta-data: url
```

**解决方案:**

1. **检查 `pyproject.toml` 必需字段**:
   ```toml
   [project]
   name = "halo-mcp-server"
   dynamic = ["version"]
   description = "MCP for Halo blog system - AI-powered content management"
   readme = "README.md"
   requires-python = ">=3.10"
   license = {text = "MIT"}
   
   [project.urls]
   Homepage = "https://github.com/Huangwh826/halo-mcp-server"
   ```

2. **重新构建**:
   ```bash
   rm -rf dist build src/*.egg-info
   python -m build
   python -m twine check dist/*
   ```

### 问题 4: 依赖项问题

**错误信息:**
```
error: Could not find suitable distribution for Requirement.parse('xxx')
```

**解决方案:**

1. **检查依赖项版本**:
   ```toml
   dependencies = [
       "mcp>=0.9.0",  # 确保版本约束合理
       "httpx>=0.25.0",
   ]
   ```

2. **验证依赖项存在**:
   ```bash
   pip search mcp  # 检查包是否在 PyPI 上
   ```

3. **从 TestPyPI 安装时指定主 PyPI**:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ \
               --extra-index-url https://pypi.org/simple/ \
               halo-mcp-server
   ```

### 问题 5: 模块导入错误

**错误信息:**
```
ModuleNotFoundError: No module named 'halo_mcp_server'
```

**解决方案:**

1. **重新安装包**:
   ```bash
   pip uninstall halo-mcp-server -y
   pip install -e .
   ```

2. **检查包结构**:
   ```bash
   python -m build
   tar -tzf dist/halo_mcp_server-*.tar.gz | grep __init__.py
   ```

3. **验证 setuptools 配置**:
   ```toml
   [tool.setuptools.packages.find]
   where = ["src"]
   ```

### 问题 6: version.txt 未找到

**错误信息:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'version.txt'
```

**解决方案:**

1. **确保 `version.txt` 在项目根目录**:
   ```bash
   ls version.txt  # 应该存在
   cat version.txt  # 应该包含版本号,如 0.1.3
   ```

2. **检查 `MANIFEST.in`**:
   ```
   include version.txt
   ```

3. **重新构建**:
   ```bash
   rm -rf dist build src/*.egg-info
   python -m build
   ```

### 问题 7: wheel 构建失败

**错误信息:**
```
error: invalid command 'bdist_wheel'
```

**解决方案:**
```bash
pip install --upgrade wheel setuptools
python -m build
```

### 问题 8: Twine 上传超时

**错误信息:**
```
ConnectionError: HTTPSConnectionPool(host='upload.pypi.org', port=443)
```

**解决方案:**

1. **检查网络连接**
2. **使用代理（如果需要）**:
   ```bash
   export https_proxy=http://proxy.example.com:8080
   python -m twine upload dist/*
   ```
3. **增加超时时间**:
   ```bash
   python -m twine upload --timeout 300 dist/*
   ```

---

## 高级配置

### 自动化版本号管理

使用 `update_version.py` 脚本实现自动化版本管理:

```bash
# 查看当前版本
python update_version.py

# 自动升级
python update_version.py patch   # 修订号 +1 (0.1.3 → 0.1.4)
python update_version.py minor   # 次版本号 +1 (0.1.3 → 0.2.0)
python update_version.py major   # 主版本号 +1 (0.1.3 → 1.0.0)

# 手动设置
python update_version.py 1.0.0
```

### 签名发布

使用 GPG 签名发布包（可选,增强安全性）:

```bash
# 生成 GPG 密钥（如果没有）
gpg --gen-key

# 签名并上传
python -m twine upload --sign dist/*
```

### CI/CD 自动发布

#### GitHub Actions 示例

创建 `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
        run: python -m twine upload dist/*
```

**配置步骤**:
1. 在 GitHub 仓库设置中添加 Secret: `PYPI_TOKEN`
2. 值为你的 PyPI Token
3. 创建 Release 时会自动触发发布

---

## 参考资源

- **PyPI 官方文档:** https://packaging.python.org/
- **Twine 文档:** https://twine.readthedocs.io/
- **PEP 440（版本号规范）:** https://peps.python.org/pep-0440/
- **PEP 621（pyproject.toml）:** https://peps.python.org/pep-0621/
- **语义化版本:** https://semver.org/lang/zh-CN/
- **版本管理详细文档:** [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md)

---

## 快速命令参考

```bash
# 清理
rm -rf dist build src/*.egg-info

# 构建
python -m build

# 检查
python -m twine check dist/*

# 上传到 TestPyPI
python -m twine upload --repository testpypi dist/*

# 上传到 PyPI
python -m twine upload dist/*

# 从 TestPyPI 安装测试
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ halo-mcp-server

# 从 PyPI 安装
pip install halo-mcp-server
```

---

## 联系支持

如果遇到其他问题,可以:

1. 查看 PyPI 帮助文档:https://pypi.org/help/
2. 提交 Issue:https://github.com/Huangwh826/halo-mcp-server/issues
3. 查看项目 README:https://github.com/Huangwh826/halo-mcp-server

---

**祝发布顺利!** 🚀

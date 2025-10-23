# PyPI 发布指南

本文档详细说明如何将 Halo MCP Server 发布到 PyPI。

## 📋 目录

- [前置准备](#前置准备)
- [快速发布](#快速发布)
- [手动发布流程](#手动发布流程)
- [发布检查清单](#发布检查清单)
- [故障排除](#故障排除)

---

## 前置准备

### 1. 注册 PyPI 账号

#### TestPyPI（测试环境）
1. 访问：https://test.pypi.org/account/register/
2. 注册账号并验证邮箱

#### PyPI（正式环境）
1. 访问：https://pypi.org/account/register/
2. 注册账号并验证邮箱

### 2. 生成 API Token

#### TestPyPI Token
1. 登录 TestPyPI：https://test.pypi.org/
2. 进入 Account Settings → API tokens
3. 点击 "Add API token"
4. 设置名称：`halo-mcp-server`
5. 范围：选择 "Entire account" 或特定项目
6. **复制并保存 Token**（仅显示一次）

#### PyPI Token
1. 登录 PyPI：https://pypi.org/
2. 进入 Account Settings → API tokens
3. 点击 "Add API token"
4. 设置名称：`halo-mcp-server`
5. 范围：选择 "Entire account" 或特定项目
6. **复制并保存 Token**（仅显示一次）

### 3. 配置认证信息

#### 方法一：使用 .pypirc 文件（推荐）

**Windows 位置：** `%USERPROFILE%\.pypirc`
**Linux/macOS 位置：** `~/.pypirc`

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

**⚠️ 安全提示：**
- 文件权限设置为仅用户可读：`chmod 600 ~/.pypirc` (Linux/macOS)
- 不要提交此文件到 Git
- `.pypirc` 已在 `.gitignore` 中

#### 方法二：环境变量

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

---

## 快速发布

我们提供了自动化发布脚本，简化发布流程。

### Windows

```powershell
# 1. 激活虚拟环境（如果使用）
.\venv\Scripts\activate

# 2. 运行发布脚本
.\publish.bat
```

### Linux/macOS

```bash
# 1. 激活虚拟环境（如果使用）
source venv/bin/activate

# 2. 添加执行权限
chmod +x publish.sh

# 3. 运行发布脚本
./publish.sh
```

### 脚本功能

发布脚本会自动完成以下步骤：

1. ✅ 清理旧的构建文件
2. ✅ 安装/更新构建工具
3. ✅ 运行代码格式检查
4. ✅ 构建 Python 包
5. ✅ 检查包的完整性
6. ✅ 交互式选择发布目标
7. ✅ 上传到 PyPI/TestPyPI

---

## 手动发布流程

如果你想手动控制每一步，可以按照以下流程操作。

### 步骤 1: 更新版本号

编辑 `pyproject.toml`：

```toml
[project]
name = "halo-mcp-server"
version = "0.1.2"  # ← 修改这里
```

**版本号规范（Semantic Versioning）：**
- **主版本号**：不兼容的 API 修改（1.0.0 → 2.0.0）
- **次版本号**：向下兼容的功能性新增（0.1.0 → 0.2.0）
- **修订号**：向下兼容的问题修正（0.1.0 → 0.1.2）

### 步骤 2: 更新 README 和文档

确保以下内容是最新的：
- [ ] `README.md` 中的版本号徽章
- [ ] 更新日志（如果有 `CHANGELOG.md`）
- [ ] 功能特性列表
- [ ] 安装说明

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

这会在 `dist/` 目录生成两个文件：
- `halo_mcp_server-0.1.2-py3-none-any.whl` (wheel 包)
- `halo_mcp_server-0.1.2.tar.gz` (源码包)

### 步骤 6: 检查构建的包

```bash
python -m twine check dist/*
```

应该看到：
```
Checking dist/halo_mcp_server-0.1.2-py3-none-any.whl: PASSED
Checking dist/halo_mcp_server-0.1.2.tar.gz: PASSED
```

### 步骤 7: 上传到 TestPyPI（推荐先测试）

```bash
python -m twine upload --repository testpypi dist/*
```

输入用户名和密码（或使用 Token）：
- Username: `__token__`
- Password: `pypi-AgENdGVzdC5weXBpLm9yZw...`（你的 TestPyPI Token）

### 步骤 8: 测试安装

```bash
# 从 TestPyPI 安装
pip install --index-url https://test.pypi.org/simple/ halo-mcp-server

# 测试基本功能
python -c "import halo_mcp_server; print(halo_mcp_server.__version__)"
```

### 步骤 9: 上传到正式 PyPI

确认 TestPyPI 测试成功后：

```bash
python -m twine upload dist/*
```

输入用户名和密码（或使用 Token）：
- Username: `__token__`
- Password: `pypi-AgEIcHlwaS5vcmcC...`（你的 PyPI Token）

### 步骤 10: 验证发布

1. **查看 PyPI 页面：**
   - https://pypi.org/project/halo-mcp-server/

2. **测试安装：**
   ```bash
   pip install halo-mcp-server
   ```

3. **验证版本：**
   ```bash
   pip show halo-mcp-server
   ```

---

## 发布检查清单

发布前请检查以下事项：

### 代码质量
- [ ] 所有单元测试通过
- [ ] 代码格式符合规范（Black, isort）
- [ ] 类型检查通过（mypy）
- [ ] 无明显的代码质量问题（ruff）

### 文档
- [ ] README.md 内容完整且准确
- [ ] 版本号已更新
- [ ] 安装说明正确
- [ ] 示例代码可用
- [ ] LICENSE 文件存在

### 配置文件
- [ ] `pyproject.toml` 配置正确
- [ ] 依赖项版本合理
- [ ] 分类器（classifiers）准确
- [ ] 项目 URL 正确

### 包内容
- [ ] 所有必要文件都包含在包中
- [ ] `MANIFEST.in` 配置正确
- [ ] 没有包含敏感信息（Token、密码等）
- [ ] 测试文件和示例文件已排除

### 版本管理
- [ ] 版本号遵循语义化版本规范
- [ ] 版本号在 PyPI 上尚未使用
- [ ] Git 标签已创建（可选）

### 测试
- [ ] 在 TestPyPI 测试成功
- [ ] 测试安装包可正常使用
- [ ] 依赖项能正确安装

---

## 故障排除

### 问题 1: 版本号已存在

**错误信息：**
```
HTTPError: 400 Bad Request from https://upload.pypi.org/legacy/
File already exists.
```

**解决方案：**
1. PyPI 不允许重复上传相同版本
2. 更新 `pyproject.toml` 中的版本号
3. 重新构建并上传

### 问题 2: 认证失败

**错误信息：**
```
HTTPError: 403 Forbidden from https://upload.pypi.org/legacy/
Invalid or non-existent authentication information.
```

**解决方案：**
1. 确认 Token 正确且未过期
2. 检查 `.pypirc` 文件格式
3. 确保用户名是 `__token__`（两个下划线）
4. 重新生成 Token

### 问题 3: 包检查失败

**错误信息：**
```
warning: check: missing required meta-data: url
```

**解决方案：**
1. 检查 `pyproject.toml` 配置完整性
2. 确保包含必要的元数据（name, version, description 等）
3. 运行 `python -m build` 重新构建

### 问题 4: 依赖项问题

**错误信息：**
```
error: Could not find suitable distribution for Requirement.parse('xxx')
```

**解决方案：**
1. 检查 `pyproject.toml` 中的依赖项版本
2. 确保依赖项在 PyPI 上存在
3. 更新依赖项版本约束

### 问题 5: 文件缺失

**错误信息：**
```
warning: sdist: standard file not found: should have one of README, README.rst, README.txt, README.md
```

**解决方案：**
1. 确保 `README.md` 存在于项目根目录
2. 检查 `MANIFEST.in` 配置
3. 重新构建包

### 问题 6: wheel 构建失败

**错误信息：**
```
error: invalid command 'bdist_wheel'
```

**解决方案：**
```bash
pip install --upgrade wheel setuptools
```

---

## 高级配置

### 自动化版本号管理

使用 `bump2version` 自动管理版本号：

```bash
pip install bump2version

# 修订号 +1 (0.1.0 → 0.1.2)
bump2version patch

# 次版本号 +1 (0.1.0 → 0.2.0)
bump2version minor

# 主版本号 +1 (0.1.0 → 1.0.0)
bump2version major
```

### 签名发布

使用 GPG 签名发布包（可选）：

```bash
# 生成 GPG 密钥（如果没有）
gpg --gen-key

# 签名并上传
python -m twine upload --sign dist/*
```

### CI/CD 自动发布

参考 `.github/workflows/publish.yml`（如果使用 GitHub Actions）：

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

---

## 参考资源

- **PyPI 官方文档：** https://packaging.python.org/
- **Twine 文档：** https://twine.readthedocs.io/
- **PEP 440（版本号规范）：** https://peps.python.org/pep-0440/
- **PEP 621（pyproject.toml）：** https://peps.python.org/pep-0621/
- **语义化版本：** https://semver.org/lang/zh-CN/

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
pip install --index-url https://test.pypi.org/simple/ halo-mcp-server

# 从 PyPI 安装
pip install halo-mcp-server
```

---

## 联系支持

如果遇到其他问题，可以：

1. 查看 PyPI 帮助文档：https://pypi.org/help/
2. 提交 Issue：https://github.com/Huangwh826/halo-mcp-server/issues
3. 联系维护者

---

**祝发布顺利！** 🚀

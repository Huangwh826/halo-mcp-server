# 🚀 快速发布到 PyPI

恭喜！你的包已经成功构建。现在按照以下步骤发布到 PyPI。

## ✅ 构建完成

已生成以下文件：
```
dist/
├── halo_mcp_server-0.1.2-py3-none-any.whl  (Wheel 包)
└── halo_mcp_server-0.1.2.tar.gz            (源码包)
```

✓ 包检查通过！

---

## 📤 发布步骤

### 步骤 1: 获取 PyPI Token

#### 方法 A: TestPyPI（推荐先测试）

1. 注册账号：https://test.pypi.org/account/register/
2. 登录后进入：https://test.pypi.org/manage/account/token/
3. 点击 "Add API token"
   - Token name: `halo-mcp-server`
   - Scope: "Entire account" 或指定项目
4. 复制生成的 Token（格式：`pypi-AgENdGVzdC5weXBpLm9yZw...`）

#### 方法 B: 正式 PyPI

1. 注册账号：https://pypi.org/account/register/
2. 登录后进入：https://pypi.org/manage/account/token/
3. 点击 "Add API token"
   - Token name: `halo-mcp-server`
   - Scope: "Entire account" 或指定项目
4. 复制生成的 Token（格式：`pypi-AgEIcHlwaS5vcmcC...`）

---

### 步骤 2: 上传到 TestPyPI（强烈推荐先测试）

```powershell
# 在项目目录运行
cd d:\Project\halo-mcp-server

# 上传到 TestPyPI
python -m twine upload --repository testpypi dist/*
```

**输入凭据：**
- Username: `__token__`（注意是两个下划线）
- Password: 粘贴你的 TestPyPI Token

**成功标志：**
```
Uploading distributions to https://test.pypi.org/legacy/
Uploading halo_mcp_server-0.1.2-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 49.1/49.1 kB
Uploading halo_mcp_server-0.1.2.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 116.6/116.6 kB

View at:
https://test.pypi.org/project/halo-mcp-server/0.1.2/
```

---

### 步骤 3: 测试安装

```powershell
# 创建新的虚拟环境进行测试
python -m venv test_env
.\test_env\Scripts\activate

# 从 TestPyPI 安装
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ halo-mcp-server

# 验证安装
python -c "import halo_mcp_server; print(halo_mcp_server.__version__)"

# 退出测试环境
deactivate
```

**预期输出：**
```
Successfully installed halo-mcp-server-0.1.2
0.1.2
```

---

### 步骤 4: 发布到正式 PyPI

**⚠️ 重要提示：**
- 确保在 TestPyPI 测试成功
- PyPI 不允许重复上传相同版本
- 发布后无法撤销，只能上传新版本

```powershell
# 上传到正式 PyPI
python -m twine upload dist/*
```

**输入凭据：**
- Username: `__token__`
- Password: 粘贴你的 PyPI Token

**成功标志：**
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading halo_mcp_server-0.1.2-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 49.1/49.1 kB
Uploading halo_mcp_server-0.1.2.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 116.6/116.6 kB

View at:
https://pypi.org/project/halo-mcp-server/0.1.2/
```

---

### 步骤 5: 验证正式发布

```powershell
# 用户安装测试
pip install halo-mcp-server

# 查看包信息
pip show halo-mcp-server

# 运行测试
python -m halo-mcp-server --help
```

访问项目页面：
- **PyPI**: https://pypi.org/project/halo-mcp-server/
- **GitHub**: https://github.com/Huangwh826/halo-mcp-server

---

## 🎉 发布完成后

### 1. 更新 README 徽章

在 README.md 中添加：
```markdown
[![PyPI version](https://badge.fury.io/py/halo-mcp-server.svg)](https://pypi.org/project/halo-mcp-server/)
[![Downloads](https://pepy.tech/badge/halo-mcp-server)](https://pepy.tech/project/halo-mcp-server)
```

### 2. 创建 Git 标签

```bash
git tag -a v0.1.2 -m "Release version 0.1.2"
git push origin v0.1.2
```

### 3. 在 GitHub 创建 Release

1. 访问：https://github.com/Huangwh826/halo-mcp-server/releases/new
2. 选择标签：`v0.1.2`
3. 填写发布说明
4. 发布

### 4. 宣传推广

- 在 Halo 社区分享
- 发布博客文章
- 社交媒体宣传

---

## 🔧 使用自动化脚本

为了简化流程，我们提供了自动化脚本：

### Windows
```powershell
.\publish.bat
```

### Linux/macOS
```bash
chmod +x publish.sh
./publish.sh
```

脚本会自动完成：
1. ✅ 清理旧文件
2. ✅ 安装工具
3. ✅ 代码检查
4. ✅ 构建包
5. ✅ 检查包
6. ✅ 交互式上传

---

## 📝 常见问题

### Q1: 版本号已存在怎么办？

更新 `pyproject.toml` 中的版本号：
```toml
version = "0.1.2"  # 增加版本号
```

然后重新构建和上传。

### Q2: 认证失败

确保：
- Username 是 `__token__`（两个下划线）
- Password 是完整的 Token（包含 `pypi-` 前缀）
- Token 未过期

### Q3: 依赖项安装失败

TestPyPI 可能缺少某些依赖，使用：
```bash
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    halo-mcp-server
```

### Q4: 如何更新已发布的包？

1. 修改代码
2. 更新版本号
3. 重新构建
4. 上传新版本

---

## 📚 更多资源

- **详细文档**: [PYPI_PUBLISH.md](PYPI_PUBLISH.md)
- **PyPI 官方指南**: https://packaging.python.org/
- **Twine 文档**: https://twine.readthedocs.io/

---

## 🎊 恭喜！

你已经准备好发布你的包到 PyPI 了！

**下一步操作：**
1. ✅ 获取 PyPI Token
2. ✅ 上传到 TestPyPI 测试
3. ✅ 上传到正式 PyPI
4. ✅ 宣传推广

祝发布顺利！🚀

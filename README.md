# Halo MCP Server

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-orange.svg)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/Huangwh826/halo-mcp-server)

**让AI成为你的博客管理助手**

通过 Model Context Protocol (MCP) 将 [Halo](https://www.halo.run/) 博客系统与 AI 助手（如 Claude）无缝集成

[快速开始](#-快速开始) • [功能特性](#-功能特性) • [文档](#-文档) • [示例](#-使用示例) • [开发](#-开发)

</div>

---

## 📖 简介

Halo MCP Server 是一个基于 Python 的 MCP 服务器，为 AI 助手提供完整的 Halo 博客管理能力。通过自然语言对话，你可以轻松完成文章创建、编辑、发布等所有博客管理操作，并利用 AI 的强大能力进行智能写作、内容优化和 SEO 提升。

**注意**: Halo MCP Server 功能基本可用但未做全面测试，欢迎反馈和贡献（2025-10-24 ）

### 🎯 核心价值

- **🤖 AI 驱动** - 用自然语言管理博客，无需记忆复杂命令
- **✍️ 智能写作** - 10个专业 Prompts 助手，覆盖写作全流程
- **🚀 高效管理** - 30+ 管理工具，一句话完成复杂操作
- **🔄 无缝集成** - 与 Claude Desktop 完美配合，开箱即用
- **📝 完整功能** - 支持文章、分类、标签、附件等全部管理功能

---

## ✨ 功能特性

### 📝 文章管理（9个工具）

<table>
<tr>
<td width="50%">

**基础操作**
- ✅ 创建文章（支持 Markdown）
- ✅ 编辑文章（标题、内容、设置）
- ✅ 发布/取消发布文章
- ✅ 删除文章（回收站）
- ✅ 列出我的文章（分页、筛选）

</td>
<td width="50%">

**高级功能**
- ✅ 草稿管理（查看、编辑草稿）
- ✅ 分类和标签管理
- ✅ 文章置顶/取消置顶
- ✅ 设置封面图片
- ✅ 自定义 URL 别名

</td>
</tr>
</table>

### 🏷️ 分类标签（13个工具）

<table>
<tr>
<td width="50%">

**分类管理（6个）**
- ✅ 列出所有分类
- ✅ 创建分类（支持层级结构）
- ✅ 更新分类（名称、描述、封面）
- ✅ 删除分类
- ✅ 获取分类详情
- ✅ 查看分类下的文章

</td>
<td width="50%">

**标签管理（7个）**
- ✅ 列出所有标签
- ✅ 创建标签（支持颜色）
- ✅ 更新标签（名称、颜色）
- ✅ 删除标签
- ✅ 获取标签详情
- ✅ 查看标签下的文章
- ✅ 控制台标签列表

</td>
</tr>
</table>

### 📎 附件管理（8个工具）

- ✅ 列出附件（支持筛选）
- ✅ 上传本地文件
- ✅ 从 URL 上传
- ✅ 删除附件
- ✅ 附件分组管理
- ✅ 查看附件详情
- ✅ 创建附件分组
- ✅ 查看存储策略

### 🤖 AI 写作助手（10个 Prompts）

<table>
<tr>
<td width="50%">

**内容创作**
- 🎨 博客写作助手 - 生成高质量文章
- ✨ 内容优化器 - 提升可读性和结构
- 🎯 SEO 优化器 - 提高搜索排名
- 📰 标题生成器 - 创作吸引人的标题
- 📋 摘要生成器 - 自动生成文章摘要

</td>
<td width="50%">

**辅助功能**
- 🏷️ 标签建议器 - 智能推荐标签
- 📂 分类建议器 - 推荐合适分类
- 🌐 内容翻译器 - 多语言翻译
- ✏️ 内容校对器 - 语法和拼写检查
- 📚 系列规划器 - 规划系列文章

</td>
</tr>
</table>

---

## 🚀 快速开始

### 📋 前置要求

1. **Python 3.10 或更高版本**
   ```bash
   python --version  # 确认版本 >= 3.10
   ```

2. **运行中的 Halo 博客系统**
   - Halo 2.21 或更高版本
   - 记录服务器地址（如 `http://localhost:8091` 或 `https://yourdomain.com`）

3. **Claude Desktop 或其他 MCP 兼容客户端**
   - 下载地址：[Claude Desktop](https://claude.ai/download)

### 📦 安装

#### 方式一：从源码安装（开发）

```bash
# 1. 克隆或下载项目
git clone https://github.com/Huangwh826/halo-mcp-server.git
cd halo-mcp-server

# 2. 创建虚拟环境（推荐）
python -m venv venv

# 3. 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. 安装项目（可编辑模式）
pip install -e .
```

#### 方式二：使用 pip 安装（推荐）

```bash
pip install halo-mcp-server
```

### 🔧 配置

#### 步骤 1: 获取 Halo 访问令牌

1. 登录 Halo 后台管理系统
2. 进入 **个人中心** → **个人令牌**
3. 点击 **生成新令牌**
4. 设置令牌名称（如 "MCP Server"）
5. 选择权限（建议勾选所有内容管理权限）
6. **保存并复制生成的令牌**（仅显示一次）

#### 步骤 2: 配置 Claude Desktop

找到并编辑 Claude Desktop 配置文件：

**文件位置：**
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**配置内容：**

```json
{
  "mcpServers": {
    "halo-mcp-server": {
      "command": "python",
      "args": [
        "-m",
        "halo_mcp_server"
      ],
      "env": {
        "HALO_BASE_URL": "your_halo_base_url_here",
        "HALO_TOKEN": "your_halo_token_here"
      }
    }
  }
}
```

**📝 配置说明：**

| 配置项 | 说明 | 示例 |
|-------|------|------|
| `command` | Python 解释器路径 | `python` 或 `C:\\Python310\\python.exe` |
| `HALO_BASE_URL` | Halo 服务器地址 | `http://localhost:8091` 或 `https://blog.example.com` |
| `HALO_TOKEN` | API 访问令牌 | 从 Halo 后台获取的令牌 |

**💡 提示：**

1. **使用虚拟环境时**，将 `command` 指向虚拟环境的 Python：
   ```json
   "command": "D:\\Project\\halo-mcp\\venv\\Scripts\\python.exe"
   ```

2. **查找 Python 路径**：
   ```bash
   # Windows
   where python
   
   # macOS/Linux
   which python
   ```

3. **远程 Halo 服务**，确保使用完整 URL（包含 `http://` 或 `https://`）

#### 步骤 3: 重启 Claude Desktop

完全关闭并重新启动 Claude Desktop 以加载新配置。

### ✅ 验证安装

在 Claude Desktop 中输入以下测试命令：

```
请列出我的所有博客文章
```

**预期结果：**
- Claude 会调用 Halo MCP Server
- 返回你的文章列表
- 如果没有文章，会提示"暂无文章"

**成功标志：**
- ✅ 没有报错
- ✅ 返回了文章列表或提示信息
- ✅ Claude 理解了"列出文章"的指令

---

## 💬 使用示例

### 🌟 自然语言交互（推荐）

Halo MCP Server 的最大优势是支持自然语言对话，无需记忆复杂命令：

#### 📝 文章创作

```
👤 用户：帮我写一篇关于 Python 异步编程的技术文章并发布

🤖 Claude：
好的！我来帮你创作这篇文章。

[自动触发 halo_blog_writing_assistant Prompt]
→ 生成 2000 字专业文章
→ 推荐标签：Python、异步编程、asyncio
→ 推荐分类：技术教程
→ 调用 create_post 创建文章
→ 调用 publish_post 发布

✓ 文章《Python异步编程完全指南》已成功创建并发布！
```

#### 🔍 文章管理

```
# 查看文章
请显示我最近发布的5篇文章

# 搜索文章
搜索标题包含"Python"的文章

# 编辑文章
把"Python教程"这篇文章的标题改为"Python入门指南"

# 删除文章
删除名为"test-post"的文章
```

#### ✨ 内容优化

```
# 优化文章
请优化"Python教程"这篇文章，让它更通俗易懂

# 生成标题
为这篇文章生成5个吸引人的标题

# SEO优化
帮这篇文章做SEO优化，关键词是：Python、教程、入门
```

#### 🏷️ 分类标签

```
# 创建分类
创建一个名为"技术教程"的分类，描述是"各类技术教程文章"

# 创建标签
创建标签：Python、JavaScript、TypeScript，颜色设置为蓝色

# 批量操作
为"Python教程"文章添加标签：Python、编程、教程
```

#### 📎 附件管理

```
# 上传图片
上传这张图片作为文章封面：https://example.com/image.jpg

# 查看附件
列出所有图片附件

# 创建分组
创建一个名为"文章配图"的附件分组
```

### 📚 完整工作流示例

#### 场景：从零开始发布一篇技术博客

```
👤 用户：我想写一篇关于 Docker 容器化的技术文章

🤖 Claude：
好的！我来帮你完成整个创作和发布流程。

步骤1: 内容创作
[触发 halo_blog_writing_assistant]
→ 生成完整文章（包含简介、核心概念、实践示例、总结）

步骤2: 标题优化
[触发 halo_title_generator]
→ 提供5个标题选项供选择

步骤3: SEO优化
[触发 halo_seo_optimizer]
→ 优化关键词布局
→ 生成Meta描述

步骤4: 分类标签
[触发 halo_tag_suggester]
→ 推荐标签：Docker、容器化、DevOps、云原生
[触发 halo_category_suggester]
→ 推荐分类：云原生技术

步骤5: 创建并发布
[调用 create_post]
→ 创建文章
[调用 publish_post]
→ 发布文章

✓ 完成！文章《Docker容器化实践指南》已成功发布
  - 字数：2000字
  - 标签：Docker、容器化、DevOps、云原生
  - 分类：云原生技术
  - 文章链接：https://yourblog.com/posts/docker-guide
```

---

## 🎯 核心概念

### MCP Tools vs Prompts

Halo MCP Server 提供两种不同的能力：

<table>
<tr>
<th width="15%">类型</th>
<th width="35%">Tools（工具）</th>
<th width="35%">Prompts（提示助手）</th>
<th width="15%">对比</th>
</tr>
<tr>
<td><strong>数量</strong></td>
<td>30 个</td>
<td>10 个</td>
<td>互补配合</td>
</tr>
<tr>
<td><strong>用途</strong></td>
<td>执行具体操作（CRUD）</td>
<td>生成内容指导</td>
<td>工具执行<br>提示生成</td>
</tr>
<tr>
<td><strong>显示</strong></td>
<td>✅ 在工具列表中可见</td>
<td>❌ 后台自动触发</td>
<td>显式 vs 隐式</td>
</tr>
<tr>
<td><strong>调用</strong></td>
<td>Claude 主动调用 API</td>
<td>根据意图自动匹配</td>
<td>API vs 智能</td>
</tr>
<tr>
<td><strong>示例</strong></td>
<td>
• create_post - 创建文章<br>
• list_categories - 列出分类<br>
• upload_attachment - 上传附件
</td>
<td>
• 博客写作助手 - 生成文章<br>
• SEO优化器 - 优化内容<br>
• 标签建议器 - 推荐标签
</td>
<td>操作 vs 创作</td>
</tr>
<tr>
<td><strong>触发方式</strong></td>
<td>
明确的操作指令：<br>
"创建文章"<br>
"上传图片"
</td>
<td>
描述性需求：<br>
"写一篇文章"<br>
"优化内容"
</td>
<td>命令 vs 对话</td>
</tr>
</table>

**💡 实际工作流：**

```
用户: "帮我写一篇Python教程并发布"
     ↓
Prompts: halo_blog_writing_assistant → 生成文章内容
     ↓
Tools: create_post → 创建文章到 Halo
     ↓
Tools: publish_post → 发布文章
     ↓
结果: ✓ 文章创建并发布成功
```

### 为什么看不到 Prompts？

这是 MCP 的**优秀设计**：

- ✅ **用户友好** - 无需记忆 Prompt 名称
- ✅ **智能匹配** - AI 自动理解意图并选择合适的 Prompt
- ✅ **无感知** - 后台自动工作，用户只需描述需求
- ✅ **灵活性** - 可以用各种方式表达同一个需求

**对比传统方式：**

```bash
# ❌ 传统 CLI 方式
$ halo-cli create-post \
  --title "Python教程" \
  --content-file article.md \
  --tags "Python,教程" \
  --category "编程" \
  --publish

# ✅ MCP 方式（自然语言）
帮我写一篇Python教程并发布
```

---

## 📚 文档

### 核心文档

| 文档 | 描述 |
|------|------|
| [快速开始](QUICKSTART.md) | 5分钟快速上手指南 |
| [设计文档](DESIGN.md) | 系统架构和设计理念 |
| [MCP Prompts 指南](MCP_PROMPTS_GUIDE.md) | 10个写作助手详细说明 |
| [Prompts vs Tools](PROMPTS_VS_TOOLS_GUIDE.md) | 两者区别和使用方法 |
| [使用示例](examples/usage_examples.md) | 完整的使用示例集 |

### API 文档

| 文档 | 描述 |
|------|------|
| [Console API](halo_apis_docs/apis_console.json) | Halo 控制台 API |
| [Public API](halo_apis_docs/apis_public.json) | Halo 公开 API |
| [UC API](halo_apis_docs/apis_uc.json) | Halo 用户内容 API |
| [Extension API](halo_apis_docs/apis_extension.json) | Halo 扩展 API |

### 示例代码

| 示例 | 描述 |
|------|------|
| [文章管理示例](examples/usage_examples.md) | 创建、编辑、发布文章 |
| [分类管理示例](examples/category_management_examples.py) | 分类的增删改查 |
| [标签管理示例](examples/tag_management_examples.py) | 标签的管理操作 |
| [附件管理示例](examples/attachment_management_examples.py) | 文件上传和管理 |
| [Prompts 示例](examples/mcp_prompts_examples.py) | AI写作助手使用 |

---

## 🔧 配置说明

### 环境变量

创建 `.env` 文件或在 Claude Desktop 配置中设置：

```env
# ========== 必需配置 ==========
HALO_BASE_URL=http://localhost:8091    # Halo 服务器地址
HALO_TOKEN=your_token_here              # API 访问令牌

# ========== 可选配置 ==========
MCP_LOG_LEVEL=INFO                      # 日志级别: DEBUG, INFO, WARNING, ERROR
MCP_TIMEOUT=30                          # HTTP 请求超时（秒）

# ========== 功能开关 ==========
ENABLE_IMAGE_COMPRESSION=true           # 启用图片压缩
IMAGE_MAX_WIDTH=1920                    # 压缩后最大宽度（像素）
IMAGE_QUALITY=85                        # 图片质量 (1-100)
MAX_UPLOAD_SIZE_MB=10                   # 最大上传大小（MB）

# ========== 高级配置 ==========
HTTP_POOL_SIZE=10                       # HTTP 连接池大小
MAX_RETRIES=3                           # 请求重试次数
ENABLE_CACHE=true                       # 启用缓存
CACHE_TTL=300                           # 缓存过期时间（秒）
```

完整配置说明请参考 [.env.example](.env.example)

---

## 🛠️ 故障排除

### 常见问题

#### 1. Claude 无法识别 Halo 工具

**症状：** Claude 不响应博客管理命令

**解决方案：**
```bash
# 检查配置文件
# Windows: %APPDATA%\Claude\claude_desktop_config.json
# macOS: ~/Library/Application Support/Claude/claude_desktop_config.json

# 验证配置格式（JSON必须正确）
# 确认 Python 路径正确
# 重启 Claude Desktop
```

#### 2. 认证失败

**症状：** 报错"Authentication failed"或"Invalid token"

**解决方案：**
1. 检查 `HALO_TOKEN` 是否正确（无多余空格）
2. 确认 Token 未过期
3. 验证 `HALO_BASE_URL` 是否可访问
4. 测试网络连接：
   ```bash
   curl http://localhost:8091/apis/api.console.halo.run/v1alpha1/posts
   ```

#### 3. 模块导入错误

**症状：** "No module named 'halo-mcp-server'"

**解决方案：**
```bash
# 重新安装
pip install -e .

# 验证安装
pip show halo-mcp-server

# 检查 Python 路径
python -c "import halo-mcp-server; print(halo_mcp_server.__version__)"
```

#### 4. Prompts 不生效

**症状：** AI 不能自动生成文章内容

**说明：** Prompts 是隐藏的，通过自然语言触发

**测试方法：**
```
# ✅ 正确方式（会触发写作 Prompt）
帮我写一篇关于Python的文章

# ❌ 错误理解（不需要这样）
使用 halo_blog_writing_assistant 写文章
```

### 调试方法

#### 查看日志

**设置调试级别：**
```json
{
  "mcpServers": {
    "halo": {
      "env": {
        "MCP_LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

**日志位置：**
- Claude Desktop 日志：帮助 → 开发者工具 → Console
- MCP 服务日志：查看标准输出

#### 手动测试

**测试认证：**
```bash
# 使用 curl 测试
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8091/apis/uc.api.content.halo.run/v1alpha1/posts
```

**测试 Python 模块：**
```bash
# 进入 Python 环境
python

# 导入并测试
>>> from halo_mcp_server.client import HaloClient
>>> import asyncio
>>> client = HaloClient()
>>> asyncio.run(client.authenticate())
>>> print("✓ 认证成功")
```

---

## 🏗️ 开发

### 开发环境设置

```bash
# 1. 克隆项目
git clone https://github.com/Huangwh826/halo_mcp_server.git
cd halo-mcp-server

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装开发依赖
pip install -e ".[dev]"

# 4. 安装 pre-commit hooks
pre-commit install
```

### 项目结构

```
halo-mcp-server/
├── src/halo-mcp-server/           # 源代码
│   ├── __init__.py
│   ├── __main__.py         # 入口文件
│   ├── config.py           # 配置管理
│   ├── server.py           # MCP 服务器
│   ├── exceptions.py       # 异常定义
│   ├── client/             # Halo API 客户端
│   │   ├── base.py
│   │   └── halo_client.py
│   ├── tools/              # MCP Tools
│   │   ├── post_tools.py
│   │   ├── category_tools.py
│   │   ├── tag_tools.py
│   │   └── attachment_tools.py
│   ├── prompts/            # MCP Prompts
│   │   └── blog_prompts.py
│   └── utils/              # 工具函数
│       └── logger.py
├── tests/                  # 单元测试
├── examples/               # 使用示例
├── halo_apis_docs/         # API 文档
├── debug_tests/            # 调试脚本
├── pyproject.toml          # 项目配置
└── README.md               # 本文件
```

### 代码规范

```bash
# 格式化代码
black src/ tests/
isort src/ tests/

# 类型检查
mypy src/

# 代码检查
ruff check src/ tests/

# 运行测试
pytest tests/ -v --cov=halo-mcp-server
```

### 添加新功能

1. **添加新 Tool：**
   ```python
   # src/halo-mcp-server/tools/custom_tools.py
   from mcp.types import Tool
   
   async def my_custom_tool(client, arguments):
       """实现你的工具逻辑"""
       pass
   
   MY_TOOLS = [
       Tool(
           name="my_tool",
           description="工具描述",
           inputSchema={...}
       )
   ]
   ```

2. **添加新 Prompt：**
   ```python
   # src/halo-mcp-server/prompts/custom_prompts.py
   from mcp.types import Prompt, PromptArgument
   
   CUSTOM_PROMPTS = [
       Prompt(
           name="my_prompt",
           description="Prompt 描述",
           arguments=[...]
       )
   ]
   ```

3. **注册到 Server：**
   ```python
   # src/halo-mcp-server/server.py
   from halo_mcp_server.tools.custom_tools import MY_TOOLS
   from halo_mcp_server.prompts.custom_prompts import CUSTOM_PROMPTS
   
   # 添加到对应列表
   all_tools += MY_TOOLS
   all_prompts += CUSTOM_PROMPTS
   ```

### 贡献指南

欢迎贡献！请查看 [DEVELOPMENT.md](DEVELOPMENT.md) 了解详细信息。

---

## 📊 功能对照表

### 完整工具列表（30个）

<details>
<summary><b>📝 文章管理工具（9个）</b></summary>

| 工具名称 | 功能说明 | 调用示例 |
|---------|---------|---------|
| `list_my_posts` | 列出我的文章 | "列出我的所有文章" |
| `get_post` | 获取文章详情 | "显示post-xxx的详情" |
| `create_post` | 创建文章 | "创建一篇文章" |
| `update_post` | 更新文章 | "更新文章标题" |
| `publish_post` | 发布文章 | "发布这篇文章" |
| `unpublish_post` | 取消发布 | "下线这篇文章" |
| `delete_post` | 删除文章 | "删除这篇文章" |
| `get_post_draft` | 获取草稿 | "查看草稿内容" |
| `update_post_draft` | 更新草稿 | "修改草稿" |

</details>

<details>
<summary><b>🏷️ 分类管理工具（6个）</b></summary>

| 工具名称 | 功能说明 | 调用示例 |
|---------|---------|---------|
| `list_categories` | 列出分类 | "列出所有分类" |
| `get_category` | 获取分类详情 | "查看分类详情" |
| `create_category` | 创建分类 | "创建技术分类" |
| `update_category` | 更新分类 | "修改分类名称" |
| `delete_category` | 删除分类 | "删除这个分类" |
| `get_category_posts` | 获取分类下文章 | "查看分类下的文章" |

</details>

<details>
<summary><b>🔖 标签管理工具（7个）</b></summary>

| 工具名称 | 功能说明 | 调用示例 |
|---------|---------|---------|
| `list_tags` | 列出标签 | "列出所有标签" |
| `get_tag` | 获取标签详情 | "查看标签详情" |
| `create_tag` | 创建标签 | "创建Python标签" |
| `update_tag` | 更新标签 | "修改标签颜色" |
| `delete_tag` | 删除标签 | "删除这个标签" |
| `get_tag_posts` | 获取标签下文章 | "查看标签下的文章" |
| `list_console_tags` | 控制台标签列表 | "查看控制台标签" |

</details>

<details>
<summary><b>📎 附件管理工具（8个）</b></summary>

| 工具名称 | 功能说明 | 调用示例 |
|---------|---------|---------|
| `list_attachments` | 列出附件 | "列出所有附件" |
| `get_attachment` | 获取附件详情 | "查看附件详情" |
| `upload_attachment` | 上传文件 | "上传这个文件" |
| `upload_attachment_from_url` | 从URL上传 | "从URL上传图片" |
| `delete_attachment` | 删除附件 | "删除这个附件" |
| `list_attachment_groups` | 列出附件分组 | "列出附件分组" |
| `create_attachment_group` | 创建分组 | "创建图片分组" |
| `get_attachment_policies` | 获取存储策略 | "查看存储策略" |

</details>

### 完整 Prompts 列表（10个）

<details>
<summary><b>🤖 AI 写作助手详细说明</b></summary>

| Prompt 名称 | 功能说明 | 触发示例 | 主要参数 |
|------------|---------|---------|---------|
| `halo_blog_writing_assistant` | 博客写作助手 | "写一篇Python文章" | topic, audience, type, word_count |
| `halo_content_optimizer` | 内容优化器 | "优化这篇文章" | content, focus, length |
| `halo_seo_optimizer` | SEO优化器 | "SEO优化" | title, content, keywords |
| `halo_title_generator` | 标题生成器 | "生成5个标题" | content_summary, style, count |
| `halo_excerpt_generator` | 摘要生成器 | "生成摘要" | content, length, style |
| `halo_tag_suggester` | 标签建议器 | "推荐标签" | title, content, existing_tags |
| `halo_category_suggester` | 分类建议器 | "推荐分类" | title, content, existing_categories |
| `halo_content_translator` | 内容翻译器 | "翻译成英文" | content, target_language |
| `halo_content_proofreader` | 内容校对器 | "校对文章" | content, language, focus |
| `halo_series_planner` | 系列规划器 | "规划系列文章" | series_topic, audience, count |

</details>

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

### 贡献方式

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 贡献者

感谢所有为项目做出贡献的开发者！

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [Halo](https://www.halo.run/) - 优秀的开源博客系统
- [Model Context Protocol](https://modelcontextprotocol.io) - 强大的 AI 集成协议
- [Claude](https://claude.ai) - 智能的 AI 助手
- 所有贡献者和用户

---

## 📞 联系我们

- **项目主页**: [GitHub](https://github.com/Huangwh826/halo-mcp-server)
- **问题反馈**: [Issues](https://github.com/Huangwh826/halo-mcp-server/issues)
- **文档**: [Documentation](https://github.com/Huangwh826/halo-mcp-server/blob/main/README.md)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给它一个 Star！**

Made with ❤️ by Halo MCP Contributors

</div>

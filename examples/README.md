# Halo MCP Server 示例集合

本目录包含 Halo MCP Server 的各种使用示例和最佳实践。

## 📁 目录结构

```
examples/
├── README.md                           # 本文件 - 示例总览
├── quick_start_example.md              # 快速开始示例
├── usage_examples.md                   # 使用示例合集
├── category_management_examples.py     # 分类管理示例
├── tag_management_examples.py          # 标签管理示例
├── attachment_management_examples.py   # 附件管理示例
└── mcp_prompts_examples.py             # AI写作助手示例
```

## 🚀 快速开始

### 新手入门

如果你是第一次使用 Halo MCP Server，推荐按以下顺序学习：

1. **[快速开始示例](quick_start_example.md)** ⭐ 必读
   - 5分钟快速上手
   - 实际调用示例
   - 基础概念介绍

2. **[使用示例合集](usage_examples.md)** ⭐ 推荐
   - 自然语言交互示例
   - 常见场景演示
   - 实用技巧分享

### 进阶学习

掌握基础后，可以学习具体功能模块：

3. **分类管理** - [category_management_examples.py](category_management_examples.py)
4. **标签管理** - [tag_management_examples.py](tag_management_examples.py)
5. **附件管理** - [attachment_management_examples.py](attachment_management_examples.py)
6. **AI写作助手** - [mcp_prompts_examples.py](mcp_prompts_examples.py)

## 📋 示例分类

### 按功能分类

| 功能模块 | 示例文件 | 说明 |
|---------|---------|------|
| **文章管理** | [usage_examples.md](usage_examples.md) | 创建、编辑、发布文章 |
| **分类管理** | [category_management_examples.py](category_management_examples.py) | 分类的增删改查 |
| **标签管理** | [tag_management_examples.py](tag_management_examples.py) | 标签的管理操作 |
| **附件管理** | [attachment_management_examples.py](attachment_management_examples.py) | 文件上传和管理 |
| **AI写作** | [mcp_prompts_examples.py](mcp_prompts_examples.py) | 10个AI写作助手 |

### 按难度分类

| 难度 | 示例 | 适合人群 |
|------|------|---------|
| 🟢 **入门** | [quick_start_example.md](quick_start_example.md) | 初次使用者 |
| 🟡 **中级** | [usage_examples.md](usage_examples.md) | 熟悉基础操作 |
| 🔴 **高级** | Python示例文件 | 需要编程能力 |

## 📚 详细说明

### 1. 快速开始示例

**文件**: [`quick_start_example.md`](quick_start_example.md)

**内容**:
- 实际的 MCP 工具调用
- `list_my_posts` 工具演示
- 返回数据结构解析
- 后续操作指南

**适合场景**:
- ✅ 第一次使用 Halo MCP Server
- ✅ 想快速了解功能
- ✅ 验证环境配置

**运行方式**: 阅读文档，通过 MCP 客户端（如 Claude Desktop）调用

---

### 2. 使用示例合集

**文件**: [`usage_examples.md`](usage_examples.md)

**内容**:
- 基础操作（列出、查看、搜索文章）
- 文章管理（创建、更新、发布、删除）
- 高级用法（批量操作、AI辅助写作）
- 常见场景（技术笔记、草稿管理、内容迁移）
- 实用技巧（自然语言、分步操作、上下文）

**适合场景**:
- ✅ 学习自然语言交互
- ✅ 了解常见使用场景
- ✅ 掌握实用技巧

**运行方式**: 阅读文档，在 Claude Desktop 中尝试

---

### 3. 分类管理示例

**文件**: [`category_management_examples.py`](category_management_examples.py)

**内容**:
- ✅ 创建新分类
- ✅ 列出所有分类
- ✅ 搜索分类
- ✅ 获取分类详情
- ✅ 更新分类
- ✅ 创建子分类（层级结构）
- ✅ 获取分类下的文章
- ✅ 批量创建分类
- ✅ 分类统计
- ✅ 清理测试数据

**高级功能**:
- 分层分类结构
- 分类模板使用
- 分类可见性控制

**运行方式**:
```bash
# 设置环境变量
export HALO_BASE_URL="http://localhost:8091"
export HALO_TOKEN="your_token_here"

# 运行示例
python category_management_examples.py
```

**预期输出**:
```
=== Halo MCP 分类管理示例 ===

1. 创建新分类
✓ 创建分类成功: category-xxx

2. 列出所有分类
✓ 找到 10 个分类:
  - 技术分享 (category-xxx)
  ...
```

---

### 4. 标签管理示例

**文件**: [`tag_management_examples.py`](tag_management_examples.py)

**内容**:
- ✅ 创建新标签（带颜色）
- ✅ 列出所有标签
- ✅ 搜索标签
- ✅ 获取标签详情
- ✅ 更新标签（修改颜色）
- ✅ 批量创建标签
- ✅ 获取标签下的文章
- ✅ 标签颜色管理
- ✅ 控制台标签管理
- ✅ 标签统计分析

**高级功能**:
- 标签分组管理（编程语言、前端框架、后端技术）
- 标签颜色主题（Material Design、GitHub）
- 标签搜索和过滤
- 标签使用分析

**颜色示例**:
- Python: `#3776ab`
- JavaScript: `#f7df1e`
- React: `#61dafb`
- Vue.js: `#4fc08d`

**运行方式**:
```bash
# 设置环境变量
export HALO_BASE_URL="http://localhost:8091"
export HALO_TOKEN="your_token_here"

# 运行示例
python tag_management_examples.py
```

**最佳实践**:
- 命名规范：简洁明确
- 颜色选择：相关标签用相似色系
- 标签分类：按技术栈分组
- 使用策略：每篇文章3-8个标签

---

### 5. 附件管理示例

**文件**: [`attachment_management_examples.py`](attachment_management_examples.py)

**内容**:
- ✅ 创建测试文件
- ✅ 获取存储策略
- ✅ 创建附件分组
- ✅ 上传本地文件
- ✅ 从URL上传文件
- ✅ 列出附件
- ✅ 搜索特定类型附件（图片、文档）
- ✅ 获取附件详情
- ✅ 附件分组管理
- ✅ 附件搜索
- ✅ 附件统计
- ✅ 清理测试数据

**高级功能**:
- 批量上传处理
- 附件分类管理（图片素材、文档资料、代码文件）
- 存储策略分析
- 附件性能优化建议

**文件类型支持**:
- 图片：JPEG, PNG, SVG, WebP
- 文档：PDF, Markdown, TXT
- 代码：Python, JSON, 纯文本
- 视频：MP4, WebM, AVI
- 音频：MP3, OGG, WAV

**运行方式**:
```bash
# 设置环境变量
export HALO_BASE_URL="http://localhost:8091"
export HALO_TOKEN="your_token_here"

# 运行示例
python attachment_management_examples.py
```

**优化建议**:
- 图片：使用WebP格式，压缩质量80-90%
- 文件：限制单文件大小，验证文件类型
- 管理：定期清理无用附件，使用CDN加速

---

### 6. AI写作助手示例

**文件**: [`mcp_prompts_examples.py`](mcp_prompts_examples.py)

**内容**:
10个AI写作助手的详细说明和使用示例

#### 6.1 博客写作助手
**功能**: 提供写作建议、结构规划和内容优化  
**参数**:
- `topic`: 文章主题
- `style`: 写作风格（技术教程/经验分享/观点评论）
- `target_audience`: 目标读者

**示例**: `topic='Python异步编程', style='技术教程', target_audience='中级开发者'`

#### 6.2 内容优化器
**功能**: 优化文章内容的可读性、结构和表达  
**参数**:
- `content`: 原始内容
- `optimization_goals`: 优化目标

#### 6.3 SEO优化器
**功能**: 优化文章的搜索引擎友好性  
**参数**:
- `content`: 文章内容
- `target_keywords`: 目标关键词

#### 6.4 标题生成器
**功能**: 根据内容生成吸引人的标题  
**参数**:
- `content`: 文章内容
- `style`: 标题风格
- `count`: 生成数量

#### 6.5 摘要生成器
**功能**: 生成文章摘要  
**参数**:
- `content`: 文章内容
- `max_length`: 最大长度

#### 6.6 标签建议器
**功能**: 根据内容建议合适的标签  
**参数**:
- `content`: 文章内容
- `max_tags`: 最大标签数

#### 6.7 分类建议器
**功能**: 建议文章分类  
**参数**:
- `content`: 文章内容
- `existing_categories`: 现有分类

#### 6.8 内容翻译器
**功能**: 翻译文章内容  
**参数**:
- `content`: 原始内容
- `target_language`: 目标语言

#### 6.9 内容校对器
**功能**: 校对文章的语法和表达  
**参数**:
- `content`: 文章内容
- `language`: 语言

#### 6.10 系列规划器
**功能**: 规划文章系列的结构和内容  
**参数**:
- `topic`: 系列主题
- `target_audience`: 目标读者
- `article_count`: 文章数量

**完整写作工作流程**:
```
1. 主题规划 → halo_series_planner
2. 内容创作 → halo_blog_writing_assistant
3. 标题优化 → halo_title_generator
4. 内容优化 → halo_content_optimizer
5. SEO优化 → halo_seo_optimizer
6. 摘要生成 → halo_excerpt_generator
7. 标签建议 → halo_tag_suggester
8. 分类建议 → halo_category_suggester
9. 内容校对 → halo_content_proofreader
10. 多语言版本 → halo_content_translator
```

**运行方式**:
```bash
python mcp_prompts_examples.py
```

**注意**: 这些Prompt需要在支持MCP的客户端（如Claude Desktop）中使用

---

## 🎯 使用场景

### 场景 1: 技术博客创建

**需求**: 创建一篇Python技术文章

**使用示例**:
1. 先阅读 [`quick_start_example.md`](quick_start_example.md) 了解基础
2. 参考 [`mcp_prompts_examples.py`](mcp_prompts_examples.py) 中的写作助手
3. 使用 [`tag_management_examples.py`](tag_management_examples.py) 创建标签
4. 使用 [`category_management_examples.py`](category_management_examples.py) 设置分类

**工作流程**:
```
创建分类和标签 → AI辅助写作 → 上传配图 → 发布文章
```

### 场景 2: 批量内容迁移

**需求**: 将多篇文章批量导入Halo

**使用示例**:
1. 参考 [`attachment_management_examples.py`](attachment_management_examples.py) 批量上传图片
2. 参考 [`usage_examples.md`](usage_examples.md) 中的批量操作
3. 使用Python脚本自动化处理

### 场景 3: 多语言博客

**需求**: 创建中英双语博客

**使用示例**:
1. 使用 `halo_blog_writing_assistant` 创建中文内容
2. 使用 `halo_content_translator` 翻译为英文
3. 使用 `halo_content_proofreader` 校对两个版本
4. 分别优化中英文SEO

## 💡 最佳实践

### 开发环境设置

```bash
# 1. 克隆项目
git clone https://github.com/Huangwh826/halo-mcp-server.git
cd halo-mcp-server

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -e .

# 4. 设置环境变量
export HALO_BASE_URL="http://localhost:8091"
export HALO_TOKEN="your_token_here"
```

### 运行Python示例

```bash
# 进入examples目录
cd examples

# 运行单个示例
python category_management_examples.py
python tag_management_examples.py
python attachment_management_examples.py
python mcp_prompts_examples.py

# 查看输出，学习用法
```

### 自然语言交互

在Claude Desktop中尝试：

```
# 基础操作
"列出所有文章"
"创建一篇关于Python的文章"
"上传一张图片"

# 复杂操作
"写一篇2000字的技术文章，主题是Docker容器化"
"优化我最近发布的文章，提升SEO"
"批量处理所有草稿，统一添加分类和标签"
```

## 🔧 故障排除

### 常见问题

**Q1: Python示例运行失败**

**原因**: 未设置环境变量

**解决方案**:
```bash
export HALO_BASE_URL="http://localhost:8091"
export HALO_TOKEN="your_token_here"
```

**Q2: 无法导入模块**

**原因**: 未安装项目

**解决方案**:
```bash
cd /path/to/halo-mcp-server
pip install -e .
```

**Q3: API调用失败**

**原因**: Token无效或Halo服务未运行

**解决方案**:
- 检查Halo服务是否运行
- 验证Token是否正确
- 检查网络连接

## 📖 相关文档

### 项目文档
- 📘 [主 README](../README.md) - 项目总览
- 📋 [设计文档](../DESIGN.md) - 架构设计
- 🧪 [测试指南](../tests/README.md) - 测试文档
- 🚀 [快速开始](../QUICKSTART.md) - 快速上手

### API文档
- 📚 [Halo API](../halo_apis_docs/apis.md) - API参考
- 🔧 [MCP协议](https://modelcontextprotocol.io) - MCP规范

## 🤝 贡献示例

欢迎贡献新的示例！

### 贡献步骤

1. Fork项目
2. 创建示例文件
3. 添加详细注释
4. 更新本README
5. 提交PR

### 示例模板

```python
#!/usr/bin/env python3
"""
示例标题

本文件展示...
"""

import asyncio
import os
from halo_mcp_server.client.halo_client import HaloClient


async def example_function():
    """功能说明"""
    
    client = HaloClient(
        base_url=os.getenv("HALO_BASE_URL"),
        token=os.getenv("HALO_TOKEN")
    )
    
    print("=== 示例开始 ===\n")
    
    # 1. 第一步
    print("1. 描述")
    try:
        # 代码
        pass
    except Exception as e:
        print(f"✗ 失败: {e}")
    
    print("\n=== 示例完成 ===")


if __name__ == "__main__":
    asyncio.run(example_function())
```

## 📊 示例统计

| 类型 | 数量 | 文件 |
|------|------|------|
| Markdown文档 | 2 | quick_start_example.md, usage_examples.md |
| Python脚本 | 4 | 分类、标签、附件、Prompts示例 |
| **总计** | **6** | - |

**代码行数统计**:
- category_management_examples.py: ~280行
- tag_management_examples.py: ~375行
- attachment_management_examples.py: ~480行
- mcp_prompts_examples.py: ~340行

## ✨ 总结

本示例集合涵盖了Halo MCP Server的所有主要功能：

1. ✅ **文章管理** - 完整的CRUD操作
2. ✅ **分类标签** - 层级结构和批量操作
3. ✅ **附件上传** - 本地和URL上传
4. ✅ **AI写作** - 10个智能助手

通过这些示例，你可以：
- 🎓 快速学习Halo MCP Server
- 💡 了解最佳实践
- 🚀 开发自己的应用
- 🔧 解决实际问题

---

**开始探索**: 从 [`quick_start_example.md`](quick_start_example.md) 开始你的学习之旅！

如果遇到问题，请查看 [FAQ](../README.md#常见问题) 或提交 [Issue](https://github.com/Huangwh826/halo-mcp-server/issues)。

# Halo MCP Server 快速开始示例

本示例演示如何使用 Halo MCP Server 工具进行博客管理。

## 🎯 示例目标

展示如何调用 `list_my_posts` 工具获取博客文章列表，这是最常用的基础操作之一。

## 📋 前置条件

1. 已安装并配置 Halo MCP Server
2. 已配置环境变量：
   - `HALO_BASE_URL`: Halo 服务器地址
   - `HALO_TOKEN`: Halo 访问令牌

## 🚀 实际调用示例

### 步骤 1: 调用工具

使用以下参数调用 `list_my_posts` 工具：

```python
{
  "page": 0,      # 第一页
  "size": 5       # 每页5条
}
```

### 步骤 2: 查看返回结果

成功调用后，返回的数据结构如下：

```json
{
  "page": 1,
  "size": 5,
  "total": 20,
  "items": [
    {
      "name": "post-20251024054815",
      "title": "深入理解 Python 异步编程：从基础到实战",
      "slug": "shen-ru-li-jie-python-yi-bu-bian-cheng-cong-ji-chu-dao-shi-zhan",
      "excerpt": "深入探讨 Python 异步编程的核心概念、实现原理和实战应用...",
      "cover": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1200",
      "visible": "PUBLIC",
      "pinned": false,
      "allowComment": true,
      "publishTime": "2025-10-23T21:48:16.481425737Z",
      "phase": "PUBLISHED",
      "permalink": "/archives/shen-ru-li-jie-python-yi-bu-bian-cheng-cong-ji-chu-dao-shi-zhan",
      "stats": {
        "visit": 1,
        "upvote": 0,
        "totalComment": 0,
        "approvedComment": 0
      }
    }
    // ... 更多文章
  ],
  "first": true,
  "last": false,
  "hasNext": true,
  "hasPrevious": false,
  "totalPages": 4
}
```

### 步骤 3: 解读结果

从返回结果中我们可以看到：

- **总文章数**: 20 篇
- **当前页**: 第 1 页（共 4 页）
- **每页显示**: 5 篇文章
- **文章状态**: 包含已发布（PUBLISHED）和草稿（DRAFT）

## 📊 返回字段说明

| 字段 | 说明 |
|------|------|
| `name` | 文章唯一标识符（用于其他 API 调用） |
| `title` | 文章标题 |
| `slug` | URL 友好的别名 |
| `excerpt` | 文章摘要 |
| `cover` | 封面图片 URL |
| `phase` | 发布状态（DRAFT/PUBLISHED/PENDING_APPROVAL） |
| `permalink` | 文章永久链接 |
| `publishTime` | 发布时间 |
| `stats` | 统计数据（访问量、点赞、评论等） |

## 🎨 实际应用场景

### 场景 1: 查看所有已发布文章

```python
{
  "page": 0,
  "size": 20,
  "publish_phase": "PUBLISHED"
}
```

### 场景 2: 搜索包含关键词的文章

```python
{
  "page": 0,
  "size": 10,
  "keyword": "Python"
}
```

### 场景 3: 按分类筛选文章

```python
{
  "page": 0,
  "size": 10,
  "category": "技术"
}
```

### 场景 4: 查看草稿文章

```python
{
  "page": 0,
  "size": 20,
  "publish_phase": "DRAFT"
}
```

## 🔗 后续操作

获取文章列表后，你可以：

1. **查看文章详情**
   ```python
   mcp_halo_get_post(name="post-20251024054815")
   ```

2. **发布草稿文章**
   ```python
   mcp_halo_publish_post(name="post-20251024053542")
   ```

3. **更新文章内容**
   ```python
   mcp_halo_update_post(
       name="post-20251024054815",
       title="新标题"
   )
   ```

4. **删除文章**
   ```python
   mcp_halo_delete_post(name="post-20251024054815")
   ```

## 💡 使用技巧

### 技巧 1: 分页获取所有文章

```python
# 第一页
page_1 = mcp_halo_list_my_posts(page=0, size=20)

# 第二页
page_2 = mcp_halo_list_my_posts(page=1, size=20)

# 根据 totalPages 循环获取所有页
total_pages = page_1["totalPages"]
for page in range(total_pages):
    posts = mcp_halo_list_my_posts(page=page, size=20)
    # 处理文章...
```

### 技巧 2: 批量处理文章

```python
# 获取所有草稿
drafts = mcp_halo_list_my_posts(publish_phase="DRAFT", size=100)

# 批量发布
for item in drafts["items"]:
    mcp_halo_publish_post(name=item["name"])
    print(f"已发布: {item['title']}")
```

### 技巧 3: 数据统计

```python
posts = mcp_halo_list_my_posts(size=100)

# 统计总访问量
total_visits = sum(item["stats"]["visit"] for item in posts["items"])

# 统计发布状态分布
published = sum(1 for item in posts["items"] if item["phase"] == "PUBLISHED")
draft = sum(1 for item in posts["items"] if item["phase"] == "DRAFT")

print(f"总访问量: {total_visits}")
print(f"已发布: {published}, 草稿: {draft}")
```

## 🎯 完整工作流示例

以下是一个完整的博客管理工作流：

```python
# 1. 列出所有草稿
drafts = mcp_halo_list_my_posts(
    publish_phase="DRAFT",
    size=10
)

print(f"找到 {drafts['total']} 篇草稿")

# 2. 选择要发布的文章
for item in drafts["items"]:
    print(f"- {item['title']} ({item['name']})")

# 3. 发布选定的文章
post_to_publish = drafts["items"][0]
result = mcp_halo_publish_post(name=post_to_publish["name"])

print(f"✓ 已发布: {post_to_publish['title']}")
print(f"访问链接: {post_to_publish['permalink']}")

# 4. 验证发布结果
published_posts = mcp_halo_list_my_posts(
    publish_phase="PUBLISHED",
    size=5
)

print(f"\n最新发布的文章:")
for item in published_posts["items"][:3]:
    print(f"- {item['title']} (访问量: {item['stats']['visit']})")
```

## 📚 相关资源

- [完整 API 文档](../halo_apis_docs/apis_uc.json)
- [更多使用示例](./usage_examples.md)
- [分类管理示例](./category_management_examples.py)
- [标签管理示例](./tag_management_examples.py)
- [附件管理示例](./attachment_management_examples.py)

## 🐛 常见问题

### Q1: 为什么返回的文章数量少于预期？

**A**: 检查以下几点：
- 确认 `size` 参数设置是否正确
- 检查是否有筛选条件（`publish_phase`, `keyword`, `category`）
- 验证用户权限是否正确

### Q2: 如何获取文章的完整内容？

**A**: `list_my_posts` 只返回文章摘要信息。要获取完整内容，使用：
```python
mcp_halo_get_post(name="文章标识符")
```

### Q3: 文章的 `name` 和 `slug` 有什么区别？

**A**: 
- `name`: 系统内部唯一标识符（如 `post-20251024054815`），用于 API 调用
- `slug`: URL 友好的别名（如 `python-async-guide`），用于生成永久链接

### Q4: 如何处理大量文章？

**A**: 使用分页机制，避免一次性加载所有数据：
```python
# 每次加载 50 条
page = 0
while True:
    result = mcp_halo_list_my_posts(page=page, size=50)
    
    # 处理当前页文章
    process_posts(result["items"])
    
    # 检查是否还有下一页
    if not result["hasNext"]:
        break
    
    page += 1
```

## ✨ 总结

本示例展示了如何：

1. ✅ 成功调用 Halo MCP Server 工具
2. ✅ 理解返回的数据结构
3. ✅ 解读文章状态和统计信息
4. ✅ 应用于实际使用场景
5. ✅ 组合多个工具完成复杂任务

这只是 Halo MCP Server 30+ 工具中的一个基础工具。结合其他工具（创建、更新、删除、分类、标签、附件等），你可以实现完整的博客管理自动化！

---

**下一步**: 尝试 [创建文章示例](./usage_examples.md#创建文章) 或 [AI 辅助写作示例](./mcp_prompts_examples.py)

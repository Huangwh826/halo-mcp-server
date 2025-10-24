"""Post management tools for Halo MCP Server."""

import json
import re
from datetime import datetime
from typing import Any, Dict

import markdown
from loguru import logger
from slugify import slugify

from halo_mcp_server.client.halo_client import HaloClient
from halo_mcp_server.models.common import ToolResult


def markdown_to_html(md_text: str) -> str:
    """
    Convert Markdown to HTML.

    Args:
        md_text: Markdown text

    Returns:
        HTML content
    """
    if not md_text:
        return ""

    try:
        # Configure markdown extensions for better rendering
        extensions = [
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            "markdown.extensions.toc",
            "markdown.extensions.tables",
        ]

        html = markdown.markdown(md_text, extensions=extensions)
        return html
    except Exception as e:
        logger.warning(f"Failed to convert markdown to HTML: {e}")
        return md_text


def _validate_post_params(args: Dict[str, Any], required_fields: list = None) -> ToolResult:
    """
    Validate post parameters.

    Args:
        args: Parameters to validate
        required_fields: List of required field names

    Returns:
        ToolResult with validation result
    """
    if required_fields:
        for field in required_fields:
            if not args.get(field):
                return ToolResult.error_result(f"Error: '{field}' parameter is required")

    # Validate title length
    title = args.get("title")
    if title and len(title) > 255:
        return ToolResult.error_result("Error: Title too long (max 255 characters)")

    # Validate slug format
    slug = args.get("slug")
    if slug and not re.match(r"^[a-z0-9-]+$", slug):
        return ToolResult.error_result(
            "Error: Invalid slug format (only lowercase letters, numbers, and hyphens allowed)"
        )

    # Validate cover URL format
    cover = args.get("cover")
    if cover and not cover.startswith(("http://", "https://")):
        return ToolResult.error_result(
            "Error: Cover must be a valid URL starting with http:// or https://"
        )

    # Validate excerpt length
    excerpt = args.get("excerpt")
    if excerpt and len(excerpt) > 500:
        return ToolResult.error_result("Error: Excerpt too long (max 500 characters)")

    # Validate content length
    content = args.get("content")
    if content and len(content) > 100000:  # 100KB limit
        return ToolResult.error_result("Error: Content too long (max 100KB)")

    # Validate visible enum
    visible = args.get("visible")
    if visible and visible not in ["PUBLIC", "PRIVATE"]:
        return ToolResult.error_result("Error: Visible must be either 'PUBLIC' or 'PRIVATE'")

    return ToolResult.success_result("Validation passed")


async def list_my_posts_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    List user's posts.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        JSON string of posts list
    """
    try:
        page = args.get("page", 0)
        size = args.get("size", 20)
        publish_phase = args.get("publish_phase")
        keyword = args.get("keyword")
        category = args.get("category")

        logger.debug(f"Listing posts: page={page}, size={size}")

        result = await client.list_my_posts(
            page=page,
            size=size,
            publish_phase=publish_phase,
            keyword=keyword,
            category=category,
        )

        # Format the result for better readability
        posts = result.get("items", [])
        formatted_posts = []

        for item in posts:
            # The actual post data is nested in the 'post' field
            post_data = item.get("post", {})
            spec = post_data.get("spec", {})
            status = post_data.get("status", {})
            metadata = post_data.get("metadata", {})

            # Additional fields from the item level
            categories = item.get("categories", [])
            tags = item.get("tags", [])
            owner = item.get("owner", {})
            stats = item.get("stats", {})

            formatted_post = {
                "name": metadata.get("name", ""),
                "title": spec.get("title", ""),
                "slug": spec.get("slug", ""),
                "excerpt": (
                    spec.get("excerpt", {}).get("raw", "")
                    if isinstance(spec.get("excerpt"), dict)
                    else spec.get("excerpt", "")
                ),
                "cover": spec.get("cover", ""),
                "visible": spec.get("visible", "PUBLIC"),
                "pinned": spec.get("pinned", False),
                "allowComment": spec.get("allowComment", True),
                "categories": [cat.get("displayName", cat.get("name", "")) for cat in categories],
                "tags": [tag.get("displayName", tag.get("name", "")) for tag in tags],
                "publishTime": spec.get("publishTime"),
                "phase": status.get("phase", "DRAFT"),
                "permalink": status.get("permalink", ""),
                "creationTimestamp": metadata.get("creationTimestamp", ""),
                "version": metadata.get("version", 0),
                "owner": owner.get("displayName", owner.get("name", "")),
                "stats": stats,
                # Additional metadata for filtering
                "labels": metadata.get("labels", {}),
                "is_deleted": metadata.get("labels", {}).get("content.halo.run/deleted") == "true",
                "is_published": metadata.get("labels", {}).get("content.halo.run/published")
                == "true",
            }
            formatted_posts.append(formatted_post)

        result["items"] = formatted_posts

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Error listing posts: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def get_post_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """Get post details."""
    try:
        # Validate parameters
        validation = _validate_post_params(args, required_fields=["name"])
        if not validation.success:
            return validation.model_dump_json()

        name = args.get("name")
        logger.debug(f"Getting post: {name}")

        result = await client.get_post(name)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Error getting post: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def create_post_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Create a new post.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        Result message
    """
    try:
        # Validate parameters
        validation = _validate_post_params(args, required_fields=["title", "content"])
        if not validation.success:
            return validation.model_dump_json()

        title = args.get("title")
        content = args.get("content")

        # Generate slug if not provided
        slug = args.get("slug") or slugify(title)

        # Build post data - 参考Java版本的正确结构
        # 注意：post 和 content 是两个独立的对象！
        post_data = {
            "post": {
                "apiVersion": "content.halo.run/v1alpha1",
                "kind": "Post",
                "metadata": {
                    "name": f"post-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "annotations": {},
                },
                "spec": {
                    "title": title,
                    "slug": slug,
                    "releaseSnapshot": "",
                    "headSnapshot": "",
                    "baseSnapshot": "",
                    "owner": "",
                    "template": "",
                    "cover": args.get("cover", ""),
                    "deleted": False,
                    "publish": False,
                    "publishTime": None,
                    "pinned": args.get("pinned", False),
                    "allowComment": args.get("allow_comment", True),
                    "visible": args.get("visible", "PUBLIC"),
                    "priority": 0,
                    "excerpt": {
                        "autoGenerate": True,
                        "raw": args.get("excerpt", ""),
                    },
                    "categories": args.get("categories", []),
                    "tags": args.get("tags", []),
                    "htmlMetas": [],
                },
            },
            "content": {
                "raw": markdown_to_html(content),  # Markdown 原文转换为HTML后的内容
                "content": markdown_to_html(content),  # HTML 转换后的内容
                "rawType": "HTML",
            },
        }

        logger.debug(f"Creating post: {title}")

        result = await client.create_post(post_data)
        post_name = result.get("metadata", {}).get("name", "")

        # Publish immediately if requested
        if args.get("publish_immediately", False):
            await client.publish_post(post_name)
            success_result = ToolResult.success_result(
                f"✓ Post '{title}' created and published successfully!",
                data={"post_name": post_name, "published": True},
            )
            return success_result.model_dump_json()

        success_result = ToolResult.success_result(
            f"✓ Post '{title}' created successfully as draft!",
            data={"post_name": post_name, "published": False},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"Error creating post: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def update_post_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """Update an existing post."""
    try:
        # Validate parameters
        validation = _validate_post_params(args, required_fields=["name"])
        if not validation.success:
            return validation.model_dump_json()

        name = args.get("name")
        has_content_update = "content" in args

        # Get current post
        post = await client.get_post(name)

        # Update metadata fields
        spec = post.get("spec", {})
        metadata_updated = False

        if "title" in args:
            spec["title"] = args["title"]
            metadata_updated = True
        if "excerpt" in args:
            if "excerpt" not in spec:
                spec["excerpt"] = {"autoGenerate": True, "raw": ""}
            spec["excerpt"]["raw"] = args["excerpt"]
            metadata_updated = True
        if "categories" in args:
            spec["categories"] = args["categories"]
            metadata_updated = True
        if "tags" in args:
            spec["tags"] = args["tags"]
            metadata_updated = True
        if "cover" in args:
            spec["cover"] = args["cover"]
            metadata_updated = True
        if "allow_comment" in args:
            spec["allowComment"] = args["allow_comment"]
            metadata_updated = True
        if "pinned" in args:
            spec["pinned"] = args["pinned"]
            metadata_updated = True
        if "visible" in args:
            spec["visible"] = args["visible"]
            metadata_updated = True

        # Update metadata if there are changes
        if metadata_updated:
            logger.debug(f"Updating post metadata: {name}")
            await client.update_post(name, post)

        # Update content if provided (must use draft API)
        if has_content_update:
            logger.debug(f"Updating post content: {name}")

            # Get current draft
            current_draft = await client.get_post_draft(name, patched=False)

            # Convert Markdown to HTML
            content = args["content"]
            html_content = markdown_to_html(content)

            # 根据 API 文档,需要在 metadata.annotations 中设置 "content.halo.run/content-json"
            # Content 对象结构: {"raw": "...", "content": "...", "rawType": "HTML"}
            metadata = current_draft.get("metadata", {})
            if "annotations" not in metadata:
                metadata["annotations"] = {}

            # 设置 content-json annotation (必须是 JSON 字符串)
            content_obj = {
                "raw": html_content,  # HTML 内容（与content字段保持一致）
                "content": html_content,  # HTML 内容
                "rawType": "HTML",  # 原始类型
            }
            metadata["annotations"]["content.halo.run/content-json"] = json.dumps(
                content_obj, ensure_ascii=False
            )

            logger.debug(f"Setting content-json annotation with {len(content)} chars")

            # Update draft - 只更新 metadata,spec 保持不变
            draft_data = {
                "apiVersion": current_draft.get("apiVersion", "content.halo.run/v1alpha1"),
                "kind": current_draft.get("kind", "Snapshot"),
                "metadata": metadata,
                "spec": current_draft.get("spec", {}),  # spec 保持原样
            }

            logger.debug(f"Calling update_post_draft with content-json annotation")
            await client.update_post_draft(name, draft_data)

            # 重新发布以应用新内容
            logger.debug(f"Re-publishing post to apply content changes: {name}")
            await client.publish_post(name)

        success_result = ToolResult.success_result(
            f"✓ Post '{name}' updated successfully!"
            + (" Content has been updated and re-published." if has_content_update else ""),
            data={"post_name": name, "content_updated": has_content_update},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"Error updating post: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def publish_post_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """Publish a post."""
    try:
        # Validate parameters
        validation = _validate_post_params(args, required_fields=["name"])
        if not validation.success:
            return validation.model_dump_json()

        name = args.get("name")
        logger.debug(f"Publishing post: {name}")

        await client.publish_post(name)

        success_result = ToolResult.success_result(
            f"✓ Post '{name}' published successfully!", data={"post_name": name, "published": True}
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"Error publishing post: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def unpublish_post_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """Unpublish a post."""
    try:
        # Validate parameters
        validation = _validate_post_params(args, required_fields=["name"])
        if not validation.success:
            return validation.model_dump_json()

        name = args.get("name")
        logger.debug(f"Unpublishing post: {name}")

        await client.unpublish_post(name)

        success_result = ToolResult.success_result(
            f"✓ Post '{name}' unpublished successfully!",
            data={"post_name": name, "published": False},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"Error unpublishing post: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def delete_post_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """Delete a post."""
    try:
        # Validate parameters
        validation = _validate_post_params(args, required_fields=["name"])
        if not validation.success:
            return validation.model_dump_json()

        name = args.get("name")
        logger.debug(f"Deleting post: {name}")

        await client.delete_post(name)

        success_result = ToolResult.success_result(
            f"✓ Post '{name}' deleted successfully!", data={"post_name": name, "deleted": True}
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"Error deleting post: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def get_post_draft_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """Get post draft content."""
    try:
        # Validate parameters
        validation = _validate_post_params(args, required_fields=["name"])
        if not validation.success:
            return validation.model_dump_json()

        name = args.get("name")
        include_patched = args.get("include_patched", False)

        logger.debug(f"Getting post draft: {name}")

        result = await client.get_post_draft(name, include_patched)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Error getting post draft: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def update_post_draft_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """Update post draft content."""
    try:
        # Validate parameters
        validation = _validate_post_params(args, required_fields=["name", "content"])
        if not validation.success:
            return validation.model_dump_json()

        name = args.get("name")
        content = args.get("content")

        logger.debug(f"Updating post draft: {name}")

        # 首先获取当前草稿
        current_draft = await client.get_post_draft(name, patched=False)

        # 将 Markdown 转换为 HTML
        html_content = markdown_to_html(content)

        # 构造正确的 Snapshot 数据结构
        draft_data = {
            "apiVersion": current_draft.get("apiVersion", "content.halo.run/v1alpha1"),
            "kind": current_draft.get("kind", "Snapshot"),
            "metadata": current_draft.get("metadata", {}),
            "spec": {
                **current_draft.get("spec", {}),
                "rawType": "HTML",
                "rawPatch": html_content,  # 转换后的HTML内容（与contentPatch保持一致）
                "contentPatch": html_content,  # 转换后的 HTML 内容
                "lastModifyTime": datetime.now().isoformat() + "Z",
            },
        }

        await client.update_post_draft(name, draft_data)

        success_result = ToolResult.success_result(
            f"✓ Post draft '{name}' updated successfully!",
            data={"post_name": name, "draft_updated": True},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"Error updating post draft: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


# MCP Tool 定义
from mcp.types import Tool

POST_TOOLS = [
    Tool(
        name="list_my_posts",
        description="列出当前用户的所有文章，支持按发布状态、关键词和分类筛选",
        inputSchema={
            "type": "object",
            "properties": {
                "page": {
                    "type": "number",
                    "description": "页码（默认：0）",
                    "default": 0,
                },
                "size": {
                    "type": "number",
                    "description": "每页数量（默认：20）",
                    "default": 20,
                },
                "publish_phase": {
                    "type": "string",
                    "description": "按发布状态筛选：DRAFT（草稿）、PENDING_APPROVAL（待审核）、PUBLISHED（已发布）、FAILED（失败）",
                    "enum": ["DRAFT", "PENDING_APPROVAL", "PUBLISHED", "FAILED"],
                },
                "keyword": {
                    "type": "string",
                    "description": "搜索关键词",
                },
                "category": {
                    "type": "string",
                    "description": "按分类名称筛选（包含子分类）",
                },
            },
        },
    ),
    Tool(
        name="get_post",
        description="获取指定文章的详细信息，包括内容、元数据和设置",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "文章名称/标识符（必填）",
                },
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="create_post",
        description="创建一篇新的博客文章，包括标题、内容、分类、标签等设置",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "文章标题（必填）",
                },
                "content": {
                    "type": "string",
                    "description": "文章内容，Markdown 格式（必填）",
                },
                "slug": {
                    "type": "string",
                    "description": "URL 别名（不提供则自动生成）",
                },
                "excerpt": {
                    "type": "string",
                    "description": "文章摘要/简介",
                },
                "cover": {
                    "type": "string",
                    "description": "封面图片 URL",
                },
                "categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "分类内部标识符列表（必须使用分类的 metadata.name 字段，而非 displayName！例如：['category-yJfRu', 'category-kfyBb']）。可通过 list_categories 工具获取所有分类的标识符。",
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "标签内部标识符列表（必须使用标签的 metadata.name 字段，而非 displayName！例如：['tag-LrsQn', 'c33ceabb-d8f1-4711-8991-bb8f5c92ad7c']）。可通过 list_tags 工具获取所有标签的标识符。",
                },
                "visible": {
                    "type": "string",
                    "description": "可见性：PUBLIC（公开）或 PRIVATE（私密），默认：PUBLIC",
                    "enum": ["PUBLIC", "PRIVATE"],
                    "default": "PUBLIC",
                },
                "allow_comment": {
                    "type": "boolean",
                    "description": "是否允许评论（默认：true）",
                    "default": True,
                },
                "pinned": {
                    "type": "boolean",
                    "description": "是否置顶（默认：false）",
                    "default": False,
                },
                "publish_immediately": {
                    "type": "boolean",
                    "description": "创建后立即发布（默认：false）",
                    "default": False,
                },
            },
            "required": ["title", "content"],
        },
    ),
    Tool(
        name="update_post",
        description="更新现有文章的标题、内容、分类、标签或其他设置",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "文章名称/标识符（必填）",
                },
                "title": {
                    "type": "string",
                    "description": "新标题",
                },
                "content": {
                    "type": "string",
                    "description": "新内容，Markdown 格式",
                },
                "excerpt": {
                    "type": "string",
                    "description": "新摘要",
                },
                "cover": {
                    "type": "string",
                    "description": "新封面图片 URL",
                },
                "categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "新分类内部标识符列表（必须使用分类的 metadata.name 字段，而非 displayName！例如：['category-yJfRu', 'category-kfyBb']）。可通过 list_categories 工具获取所有分类的标识符。",
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "新标签内部标识符列表（必须使用标签的 metadata.name 字段，而非 displayName！例如：['tag-LrsQn', 'c33ceabb-d8f1-4711-8991-bb8f5c92ad7c']）。可通过 list_tags 工具获取所有标签的标识符。",
                },
                "visible": {
                    "type": "string",
                    "description": "可见性：PUBLIC（公开）或 PRIVATE（私密）",
                    "enum": ["PUBLIC", "PRIVATE"],
                },
                "allow_comment": {
                    "type": "boolean",
                    "description": "是否允许评论",
                },
                "pinned": {
                    "type": "boolean",
                    "description": "是否置顶",
                },
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="publish_post",
        description="发布草稿文章，使其公开可见",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "文章名称/标识符（必填）",
                },
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="unpublish_post",
        description="取消发布文章，将其转换回草稿状态",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "文章名称/标识符（必填）",
                },
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="delete_post",
        description="删除文章（移至回收站）",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "文章名称/标识符（必填）",
                },
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="get_post_draft",
        description="获取文章的草稿版本及可编辑内容",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "文章名称/标识符（必填）",
                },
                "include_patched": {
                    "type": "boolean",
                    "description": "是否包含补丁内容（默认：false）",
                    "default": False,
                },
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="update_post_draft",
        description="更新文章的草稿内容，不会发布",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "文章名称/标识符（必填）",
                },
                "content": {
                    "type": "string",
                    "description": "草稿内容，Markdown 格式（必填）",
                },
            },
            "required": ["name", "content"],
        },
    ),
]

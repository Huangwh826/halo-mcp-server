# -*- coding: utf-8 -*-
"""Halo MCP Server 的文章管理工具。"""

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
    """使用 markdown-it-py（含常用扩展）将 Markdown 转为 HTML。"""
    # 空内容直接返回空字符串
    if not md_text:
        return ""
    try:
        from markdown_it import MarkdownIt
        from mdit_py_plugins.anchors import anchors_plugin
        from mdit_py_plugins.footnote import footnote_plugin
        from mdit_py_plugins.front_matter import front_matter_plugin
        from mdit_py_plugins.tasklists import tasklists_plugin
        from mdit_py_plugins.texmath import texmath_plugin
        from mdit_py_toc import toc_plugin

        md = (
            MarkdownIt("gfm-like", {"linkify": True, "breaks": False, "html": True})
            .use(anchors_plugin, max_level=6)
            .use(footnote_plugin)
            .use(front_matter_plugin)
            .use(tasklists_plugin)
            .use(texmath_plugin)
            .use(toc_plugin)
        )
        md.enable("table")
        return md.render(md_text)
    except Exception as e:
        logger.warning(f"markdown-it-py 渲染失败，回退到 Python-Markdown：{e}")
        try:
            # 采用用户指定的 Python-Markdown 扩展组合作为兜底
            return markdown.markdown(
                md_text,
                extensions=[
                    "markdown.extensions.extra",
                    "markdown.extensions.codehilite",
                    "markdown.extensions.toc",
                    "markdown.extensions.tables",
                ],
            )
        except Exception as e2:
            logger.warning(f"Markdown 转换为 HTML 失败：{e2}")
            return md_text


def looks_like_html(text: str) -> bool:
    """HTML 内容的启发式检测。
    - 检查是否以 '<' 开头、是否包含常见 HTML 标签或闭合标签。
    """
    if not text:
        return False
    sample = text.strip()
    if sample.startswith("<") and ">" in sample:
        html_tag_patterns = [
            "<p",
            "<div",
            "<span",
            "<h1",
            "<h2",
            "<h3",
            "<h4",
            "<h5",
            "<h6",
            "<ul",
            "<ol",
            "<li",
            "<a",
            "<img",
            "<code",
            "<pre",
            "<blockquote",
        ]
        lower = sample.lower()
        if any(tag in lower for tag in html_tag_patterns):
            return True
    return bool(re.search(r"</[a-zA-Z][^>]*>", sample))


def _validate_post_params(args: Dict[str, Any], required_fields: list = None) -> ToolResult:
    if required_fields:
        for field in required_fields:
            if field not in args or args[field] is None:
                return ToolResult.error_result(f"错误：缺少必填参数 '{field}'")

    # 基础类型与长度校验
    title = args.get("title")
    if title and len(title) > 256:
        return ToolResult.error_result("错误：标题过长（最多 256 字符）")

    content = args.get("content")
    if content and len(content) > 100000:
        return ToolResult.error_result("错误：内容过长（最多 100000 字符）")

    visible = args.get("visible")
    if visible and visible not in ["PUBLIC", "PRIVATE"]:
        return ToolResult.error_result("错误：可见性必须是 'PUBLIC' 或 'PRIVATE'")

    # 如提供 content_format 则进行校验
    cf = args.get("content_format")
    if cf and cf not in ["MARKDOWN", "HTML", "AUTO"]:
        return ToolResult.error_result("错误：content_format 必须是 'MARKDOWN'、'HTML' 或 'AUTO'")

    return ToolResult.success_result("验证通过")


async def list_my_posts_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    列出用户的文章。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        文章列表的 JSON 字符串
    """
    try:
        page = args.get("page", 0)
        size = args.get("size", 20)
        publish_phase = args.get("publish_phase")
        keyword = args.get("keyword")
        category = args.get("category")

        logger.debug(f"正在列出文章：page={page}, size={size}")

        result = await client.list_my_posts(
            page=page,
            size=size,
            publish_phase=publish_phase,
            keyword=keyword,
            category=category,
        )

        # 为了更好地可读性，对结果进行格式化
        posts = result.get("items", [])
        formatted_posts = []

        for item in posts:
            # 实际的文章数据嵌套在 'post' 字段中
            post_data = item.get("post", {})
            spec = post_data.get("spec", {})
            status = post_data.get("status", {})
            metadata = post_data.get("metadata", {})

            # 来自 item 层的附加字段
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
                # 额外的筛选用元数据
                "labels": metadata.get("labels", {}),
                "is_deleted": metadata.get("labels", {}).get("content.halo.run/deleted") == "true",
                "is_published": metadata.get("labels", {}).get("content.halo.run/published")
                == "true",
            }
            formatted_posts.append(formatted_post)

        result["items"] = formatted_posts

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"列出文章时发生错误：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def get_post_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """获取文章详情。"""
    try:
        # 参数校验
        validation = _validate_post_params(args, required_fields=["name"])
        if not validation.success:
            return validation.model_dump_json()

        name = args.get("name")
        logger.debug(f"获取文章：{name}")

        result = await client.get_post(name)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"获取文章出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def create_post_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    创建一篇新文章。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        操作结果消息
    """
    try:
        # 参数校验
        validation = _validate_post_params(args, required_fields=["title", "content"])
        if not validation.success:
            return validation.model_dump_json()

        title = args.get("title")
        content = args.get("content")

        # 若未提供则自动生成 slug
        slug = args.get("slug") or slugify(title)

        # 判定内容格式并渲染
        content_format = (args.get("content_format") or "MARKDOWN").upper()
        if content_format not in ["MARKDOWN", "HTML", "AUTO"]:
            return ToolResult.error_result(
                "错误：content_format 必须是 'MARKDOWN'、'HTML' 或 'AUTO'"
            ).model_dump_json()
        if content_format == "AUTO":
            is_html = looks_like_html(content)
        else:
            is_html = content_format == "HTML"

        if is_html:
            html_content = content
            content_obj = {
                "raw": html_content,
                "content": html_content,
                "rawType": "HTML",
            }
        else:
            html_content = markdown_to_html(content)
            content_obj = {
                "raw": html_content,
                "content": html_content,
                "rawType": "HTML",
            }

        # 构建文章数据 - 参考 Java 版本的正确结构
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
                "raw": content_obj["raw"],
                "content": content_obj["content"],
                "rawType": content_obj["rawType"],
            },
        }

        logger.debug(f"正在创建文章：{title}")

        result = await client.create_post(post_data)
        post_name = result.get("metadata", {}).get("name", "")

        # 若请求则立即发布
        if args.get("publish_immediately", False):
            await client.publish_post(post_name)
            success_result = ToolResult.success_result(
                f"✓ 文章『{title}』创建并成功发布！",
                data={"post_name": post_name, "published": True},
            )
            return success_result.model_dump_json()

        success_result = ToolResult.success_result(
            f"✓ 文章『{title}』创建成功（草稿）！",
            data={"post_name": post_name, "published": False},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"创建文章出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def update_post_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """更新现有文章。"""
    try:
        # 参数校验
        validation = _validate_post_params(args, required_fields=["name"])
        if not validation.success:
            return validation.model_dump_json()

        name = args.get("name")
        has_content_update = "content" in args

        # 获取当前文章
        post = await client.get_post(name)

        # 更新元数据字段
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

        # 如有变更则更新元数据
        if metadata_updated:
            logger.debug(f"更新文章元数据：{name}")
            await client.update_post(name, post)

        # 如提供内容则更新（需使用草稿 API）
        if has_content_update:
            logger.debug(f"更新文章内容：{name}")

            # 获取当前草稿
            current_draft = await client.get_post_draft(name, patched=False)

            # 判定内容格式并渲染
            content = args["content"]
            content_format = (args.get("content_format") or "MARKDOWN").upper()
            if content_format not in ["MARKDOWN", "HTML", "AUTO"]:
                return ToolResult.error_result(
                    "错误：content_format 必须是 'MARKDOWN'、'HTML' 或 'AUTO'"
                ).model_dump_json()
            if content_format == "AUTO":
                is_html = looks_like_html(content)
            else:
                is_html = content_format == "HTML"

            if is_html:
                html_content = content
                content_obj = {"raw": html_content, "content": html_content, "rawType": "HTML"}
                raw_type = "HTML"
                raw_patch = html_content
                content_patch = html_content
            else:
                html_content = markdown_to_html(content)
                content_obj = {"raw": html_content, "content": html_content, "rawType": "HTML"}
                raw_type = "HTML"
                raw_patch = html_content
                content_patch = html_content

            # 根据 API 文档,需要在 metadata.annotations 中设置 "content.halo.run/content-json"
            metadata = current_draft.get("metadata", {})
            if "annotations" not in metadata:
                metadata["annotations"] = {}

            # 设置 content-json 注解（必须是 JSON 字符串）
            metadata["annotations"]["content.halo.run/content-json"] = json.dumps(
                content_obj, ensure_ascii=False
            )

            logger.debug(f"设置 content-json 注解，原始内容长度 {len(content)} 字符")

            # 更新草稿 —— 需要补充 spec 的 patch 字段以应用内容
            draft_data = {
                "apiVersion": current_draft.get("apiVersion", "content.halo.run/v1alpha1"),
                "kind": current_draft.get("kind", "Snapshot"),
                "metadata": metadata,
                "spec": {
                    **current_draft.get("spec", {}),
                    "rawType": raw_type,
                    "rawPatch": raw_patch,
                    "contentPatch": content_patch,
                    "lastModifyTime": datetime.now().isoformat() + "Z",
                },
            }

            logger.debug(f"调用 update_post_draft 并设置 content-json 注解")
            await client.update_post_draft(name, draft_data)

            # 重新发布以应用新内容
            logger.debug(f"重新发布文章以应用内容变更：{name}")
            await client.publish_post(name)

        success_result = ToolResult.success_result(
            f"✓ 文章『{name}』更新成功！"
            + (" 内容已更新并重新发布。" if has_content_update else ""),
            data={"post_name": name, "content_updated": has_content_update},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"更新文章出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def publish_post_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """发布文章。"""
    try:
        # 参数校验
        validation = _validate_post_params(args, required_fields=["name"])
        if not validation.success:
            return validation.model_dump_json()

        name = args.get("name")
        logger.debug(f"正在发布文章：{name}")

        await client.publish_post(name)

        success_result = ToolResult.success_result(
            f"✓ 文章『{name}』发布成功！", data={"post_name": name, "published": True}
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"发布文章出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def unpublish_post_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """取消发布文章。"""
    try:
        # 参数校验
        validation = _validate_post_params(args, required_fields=["name"])
        if not validation.success:
            return validation.model_dump_json()

        name = args.get("name")
        logger.debug(f"正在取消发布文章：{name}")

        await client.unpublish_post(name)

        success_result = ToolResult.success_result(
            f"✓ 文章『{name}』已取消发布！",
            data={"post_name": name, "published": False},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"取消发布文章出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def delete_post_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """删除文章。"""
    try:
        # 参数校验
        validation = _validate_post_params(args, required_fields=["name"])
        if not validation.success:
            return validation.model_dump_json()

        name = args.get("name")
        logger.debug(f"正在删除文章：{name}")

        await client.delete_post(name)

        success_result = ToolResult.success_result(
            f"✓ 文章『{name}』删除成功！", data={"post_name": name, "deleted": True}
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"删除文章出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def get_post_draft_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """获取文章草稿内容。"""
    try:
        # 参数校验
        validation = _validate_post_params(args, required_fields=["name"])
        if not validation.success:
            return validation.model_dump_json()

        name = args.get("name")
        include_patched = args.get("include_patched", False)

        logger.debug(f"获取文章草稿：{name}")

        result = await client.get_post_draft(name, include_patched)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"获取文章草稿出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def update_post_draft_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """更新文章草稿内容。"""
    try:
        # 参数校验
        validation = _validate_post_params(args, required_fields=["name", "content"])
        if not validation.success:
            return validation.model_dump_json()

        name = args.get("name")
        content = args.get("content")

        logger.debug(f"更新文章草稿：{name}")

        # 首先获取当前草稿
        current_draft = await client.get_post_draft(name, patched=False)

        # 判定内容格式并渲染
        content_format = (args.get("content_format") or "MARKDOWN").upper()
        if content_format not in ["MARKDOWN", "HTML", "AUTO"]:
            return ToolResult.error_result(
                "错误：content_format 必须是 'MARKDOWN'、'HTML' 或 'AUTO'"
            ).model_dump_json()
        if content_format == "AUTO":
            is_html = looks_like_html(content)
        else:
            is_html = content_format == "HTML"

        if is_html:
            html_content = content
            content_obj = {"raw": html_content, "content": html_content, "rawType": "HTML"}
            raw_type = "HTML"
            raw_patch = html_content
            content_patch = html_content
        else:
            html_content = markdown_to_html(content)
            content_obj = {"raw": html_content, "content": html_content, "rawType": "HTML"}
            raw_type = "HTML"
            raw_patch = html_content
            content_patch = html_content

        # 设置 content-json 注解（根据 API 要求必须设置）
        metadata = current_draft.get("metadata", {})
        if "annotations" not in metadata:
            metadata["annotations"] = {}
        metadata["annotations"]["content.halo.run/content-json"] = json.dumps(
            content_obj,
            ensure_ascii=False,
        )

        # 构造正确的 Snapshot 数据结构（保留并补充 patch 字段）
        draft_data = {
            "apiVersion": current_draft.get("apiVersion", "content.halo.run/v1alpha1"),
            "kind": current_draft.get("kind", "Snapshot"),
            "metadata": metadata,
            "spec": {
                **current_draft.get("spec", {}),
                "rawType": raw_type,
                "rawPatch": raw_patch,
                "contentPatch": content_patch,
                "lastModifyTime": datetime.now().isoformat() + "Z",
            },
        }

        await client.update_post_draft(name, draft_data)

        success_result = ToolResult.success_result(
            f"✓ 文章草稿『{name}』更新成功！",
            data={"post_name": name, "draft_updated": True},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"更新文章草稿出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
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
        description="创建一篇新的文章，内容支持 Markdown 或原生 HTML 富文本",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "文章标题（必填）",
                },
                "content": {
                    "type": "string",
                    "description": "文章内容，支持 Markdown 或 HTML 富文本（必填）",
                },
                "content_format": {
                    "type": "string",
                    "description": "内容格式：MARKDOWN、HTML 或 AUTO（默认：MARKDOWN）",
                    "enum": ["MARKDOWN", "HTML", "AUTO"],
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
        description="更新现有文章的标题、内容（支持 Markdown 或 HTML 富文本）、分类、标签或其他设置",
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
                    "description": "新内容，支持 Markdown 或 HTML 富文本",
                },
                "content_format": {
                    "type": "string",
                    "description": "内容格式：MARKDOWN、HTML 或 AUTO（默认：MARKDOWN）",
                    "enum": ["MARKDOWN", "HTML", "AUTO"],
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
        description="更新文章草稿内容（支持 Markdown 或 HTML 富文本），不会发布",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "文章名称/标识符（必填）",
                },
                "content": {
                    "type": "string",
                    "description": "草稿内容，支持 Markdown 或 HTML 富文本（必填）",
                },
                "content_format": {
                    "type": "string",
                    "description": "内容格式：MARKDOWN、HTML 或 AUTO（默认：MARKDOWN）",
                    "enum": ["MARKDOWN", "HTML", "AUTO"],
                },
            },
            "required": ["name", "content"],
        },
    ),
]

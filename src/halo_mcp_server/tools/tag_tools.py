"""Tag management tools for Halo MCP."""

"""Tag management tools for Halo MCP."""

import json
from typing import Any, Dict, List, Optional

from loguru import logger
from mcp.types import Tool

from halo_mcp_server.client.halo_client import HaloClient
from halo_mcp_server.exceptions import HaloMCPError
from halo_mcp_server.models.common import ToolResult


async def list_tags(
    page: int = 0,
    size: int = 100,
    keyword: Optional[str] = None,
    sort: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    列出所有标签。

    Args:
        page: 页码，默认为 0
        size: 每页大小，默认为 100
        keyword: 搜索关键词
        sort: 排序条件，格式: ["property,(asc|desc)"]

    Returns:
        标签列表数据

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = HaloClient()
        await client.ensure_authenticated()

        params = {"page": page, "size": size}
        if keyword:
            params["keyword"] = keyword
        if sort:
            params["sort"] = sort

        # 使用 Extension API 获取完整的标签信息
        response = await client.get("/apis/content.halo.run/v1alpha1/tags", params=params)
        return response

    except Exception as e:
        raise HaloMCPError(f"Failed to list tags: {e}")


async def get_tag(name: str) -> Dict[str, Any]:
    """
    获取指定标签的详细信息。

    Args:
        name: 标签名称/标识符

    Returns:
        标签详细信息

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = HaloClient()
        await client.ensure_authenticated()

        response = await client.get(f"/apis/content.halo.run/v1alpha1/tags/{name}")
        return response

    except Exception as e:
        raise HaloMCPError(f"Failed to get tag '{name}': {e}")


async def create_tag(
    display_name: str,
    slug: Optional[str] = None,
    color: Optional[str] = None,
    cover: Optional[str] = None,
) -> Dict[str, Any]:
    """
    创建新标签。

    Args:
        display_name: 标签显示名称
        slug: URL 别名（不提供则自动生成）
        color: 标签颜色（十六进制颜色代码，如 #FF0000）
        cover: 封面图片 URL

    Returns:
        创建的标签信息

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = HaloClient()
        await client.ensure_authenticated()

        # 构建标签数据
        tag_data = {
            "spec": {
                "displayName": display_name,
            },
            "apiVersion": "content.halo.run/v1alpha1",
            "kind": "Tag",
            "metadata": {
                "generateName": "tag-",
            },
        }

        # 添加可选字段
        if slug:
            tag_data["spec"]["slug"] = slug
        if color:
            tag_data["spec"]["color"] = color
        if cover:
            tag_data["spec"]["cover"] = cover

        response = await client.post("/apis/content.halo.run/v1alpha1/tags", json=tag_data)
        return response

    except Exception as e:
        raise HaloMCPError(f"Failed to create tag: {e}")


async def update_tag(
    name: str,
    display_name: Optional[str] = None,
    slug: Optional[str] = None,
    color: Optional[str] = None,
    cover: Optional[str] = None,
) -> Dict[str, Any]:
    """
    更新现有标签。

    Args:
        name: 标签名称/标识符
        display_name: 新的显示名称
        slug: 新的 URL 别名
        color: 新的标签颜色（十六进制颜色代码）
        cover: 新的封面图片 URL

    Returns:
        更新后的标签信息

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = HaloClient()
        await client.ensure_authenticated()

        # 先获取现有标签信息
        existing_tag = await client.get(f"/apis/content.halo.run/v1alpha1/tags/{name}")

        # 更新指定字段
        if display_name is not None:
            existing_tag["spec"]["displayName"] = display_name
        if slug is not None:
            existing_tag["spec"]["slug"] = slug
        if color is not None:
            existing_tag["spec"]["color"] = color
        if cover is not None:
            existing_tag["spec"]["cover"] = cover

        response = await client.put(
            f"/apis/content.halo.run/v1alpha1/tags/{name}",
            json=existing_tag,
        )
        return response

    except Exception as e:
        raise HaloMCPError(f"Failed to update tag '{name}': {e}")


async def delete_tag(name: str) -> Dict[str, Any]:
    """
    删除标签。

    Args:
        name: 标签名称/标识符

    Returns:
        删除操作结果

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = HaloClient()
        await client.ensure_authenticated()

        response = await client.delete(f"/apis/content.halo.run/v1alpha1/tags/{name}")
        return response

    except Exception as e:
        raise HaloMCPError(f"Failed to delete tag '{name}': {e}")


async def get_tag_posts(
    name: str,
    page: int = 0,
    size: int = 20,
    sort: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    获取指定标签下的文章列表。

    Args:
        name: 标签名称/标识符
        page: 页码，默认为 0
        size: 每页大小，默认为 20
        sort: 排序条件，格式: ["property,(asc|desc)"]

    Returns:
        标签下的文章列表

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = HaloClient()

        params = {"page": page, "size": size}
        if sort:
            params["sort"] = sort

        # 使用 Public API 获取标签下的文章
        response = await client.get(
            f"/apis/api.content.halo.run/v1alpha1/tags/{name}/posts",
            params=params,
        )
        return response

    except Exception as e:
        raise HaloMCPError(f"Failed to get posts for tag '{name}': {e}")


async def list_console_tags(
    page: int = 0,
    size: int = 100,
    keyword: Optional[str] = None,
    sort: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    列出控制台标签（用于后台管理）。

    Args:
        page: 页码，默认为 0
        size: 每页大小，默认为 100
        keyword: 搜索关键词
        sort: 排序条件，格式: ["property,(asc|desc)"]

    Returns:
        控制台标签列表数据

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = HaloClient()
        await client.ensure_authenticated()

        params = {"page": page, "size": size}
        if keyword:
            params["keyword"] = keyword
        if sort:
            params["sort"] = sort

        # 使用 Console API 获取标签信息
        response = await client.get("/apis/api.console.halo.run/v1alpha1/tags", params=params)
        return response

    except Exception as e:
        raise HaloMCPError(f"Failed to list console tags: {e}")


# MCP Tool 定义
TAG_TOOLS = [
    Tool(
        name="list_tags",
        description="列出所有标签，支持分页和关键词搜索。返回结果中 items 列表的每个标签对象包含：metadata.name 字段（内部标识符，如 'tag-LrsQn' 或 'c33ceabb-d8f1-4711-8991-bb8f5c92ad7c'）和 spec.displayName 字段（显示名称，如 'Linux'）。重要：创建或更新文章时必须使用 metadata.name 字段作为标签标识符，而非 spec.displayName。",
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
                    "description": "每页数量（默认：100）",
                    "default": 100,
                },
                "keyword": {
                    "type": "string",
                    "description": "搜索关键词",
                },
                "sort": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "排序条件，格式: ['property,(asc|desc)']",
                },
            },
        },
    ),
    Tool(
        name="get_tag",
        description="获取指定标签的详细信息",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "标签名称/标识符（必填）",
                },
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="create_tag",
        description="创建新的标签",
        inputSchema={
            "type": "object",
            "properties": {
                "display_name": {
                    "type": "string",
                    "description": "标签显示名称（必填）",
                },
                "slug": {
                    "type": "string",
                    "description": "URL 别名（不提供则自动生成）",
                },
                "color": {
                    "type": "string",
                    "description": "标签颜色（十六进制颜色代码，如 #FF0000）",
                },
                "cover": {
                    "type": "string",
                    "description": "封面图片 URL",
                },
            },
            "required": ["display_name"],
        },
    ),
    Tool(
        name="update_tag",
        description="更新现有标签的信息",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "标签名称/标识符（必填）",
                },
                "display_name": {
                    "type": "string",
                    "description": "新的显示名称",
                },
                "slug": {
                    "type": "string",
                    "description": "新的 URL 别名",
                },
                "color": {
                    "type": "string",
                    "description": "新的标签颜色（十六进制颜色代码）",
                },
                "cover": {
                    "type": "string",
                    "description": "新的封面图片 URL",
                },
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="delete_tag",
        description="删除标签",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "标签名称/标识符（必填）",
                },
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="get_tag_posts",
        description="获取指定标签下的文章列表",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "标签名称/标识符（必填）",
                },
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
                "sort": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "排序条件，格式: ['property,(asc|desc)']",
                },
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="list_console_tags",
        description="列出控制台标签（用于后台管理），支持分页和关键词搜索",
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
                    "description": "每页数量（默认：100）",
                    "default": 100,
                },
                "keyword": {
                    "type": "string",
                    "description": "搜索关键词",
                },
                "sort": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "排序条件，格式: ['property,(asc|desc)']",
                },
            },
        },
    ),
]


# Tool handler functions for MCP


async def list_tags_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for listing tags.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        JSON string of tags list
    """
    try:
        page = args.get("page", 0)
        size = args.get("size", 100)
        keyword = args.get("keyword")
        sort = args.get("sort")

        logger.debug(f"Listing tags: page={page}, size={size}, keyword={keyword}")

        result = await list_tags(page=page, size=size, keyword=keyword, sort=sort)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Error listing tags: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def get_tag_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for getting tag details.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        JSON string of tag details
    """
    try:
        name = args.get("name")
        if not name:
            error_result = ToolResult.error_result("Error: 'name' parameter is required")
            return error_result.model_dump_json()

        logger.debug(f"Getting tag: {name}")

        result = await get_tag(name)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Error getting tag: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def create_tag_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for creating a new tag.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        JSON string of operation result
    """
    try:
        display_name = args.get("display_name")
        if not display_name:
            error_result = ToolResult.error_result("Error: 'display_name' parameter is required")
            return error_result.model_dump_json()

        slug = args.get("slug")
        color = args.get("color")
        cover = args.get("cover")

        logger.debug(f"Creating tag: {display_name}")

        result = await create_tag(display_name=display_name, slug=slug, color=color, cover=cover)

        tag_name = result.get("metadata", {}).get("name", "")
        success_result = ToolResult.success_result(
            f"✓ Tag '{display_name}' created successfully!",
            data={"tag_name": tag_name, "display_name": display_name},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"Error creating tag: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def update_tag_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for updating a tag.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        JSON string of operation result
    """
    try:
        name = args.get("name")
        if not name:
            error_result = ToolResult.error_result("Error: 'name' parameter is required")
            return error_result.model_dump_json()

        display_name = args.get("display_name")
        slug = args.get("slug")
        color = args.get("color")
        cover = args.get("cover")

        logger.debug(f"Updating tag: {name}")

        result = await update_tag(
            name=name, display_name=display_name, slug=slug, color=color, cover=cover
        )

        updated_display_name = result.get("spec", {}).get("displayName", name)
        success_result = ToolResult.success_result(
            f"✓ Tag '{updated_display_name}' updated successfully!",
            data={"tag_name": name, "updated": True},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"Error updating tag: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def delete_tag_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for deleting a tag.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        JSON string of operation result
    """
    try:
        name = args.get("name")
        if not name:
            error_result = ToolResult.error_result("Error: 'name' parameter is required")
            return error_result.model_dump_json()

        logger.debug(f"Deleting tag: {name}")

        await delete_tag(name)

        success_result = ToolResult.success_result(
            f"✓ Tag '{name}' deleted successfully!",
            data={"tag_name": name, "deleted": True},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"Error deleting tag: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def get_posts_under_tag_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for getting posts under a tag.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        JSON string of posts list
    """
    try:
        name = args.get("name")
        if not name:
            error_result = ToolResult.error_result("Error: 'name' parameter is required")
            return error_result.model_dump_json()

        page = args.get("page", 0)
        size = args.get("size", 20)
        sort = args.get("sort")

        logger.debug(f"Getting posts under tag: {name}, page={page}, size={size}")

        result = await get_tag_posts(name=name, page=page, size=size, sort=sort)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Error getting posts under tag: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def list_console_tags_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for listing console tags.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        JSON string of console tags list
    """
    try:
        page = args.get("page", 0)
        size = args.get("size", 100)
        keyword = args.get("keyword")
        sort = args.get("sort")

        logger.debug(f"Listing console tags: page={page}, size={size}, keyword={keyword}")

        result = await list_console_tags(page=page, size=size, keyword=keyword, sort=sort)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Error listing console tags: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()

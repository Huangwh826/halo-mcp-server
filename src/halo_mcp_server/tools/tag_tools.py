"""Halo MCP 标签管理工具"""

"""Halo MCP 标签管理工具"""

import json
from typing import Any, Dict, List, Optional

from loguru import logger
from mcp.types import Tool

from halo_mcp_server.client.halo_client import HaloClient
from halo_mcp_server.exceptions import HaloMCPError
from halo_mcp_server.models.common import ToolResult
import re
from slugify import slugify


async def list_tags(
    page: int = 0,
    size: int = 100,
    keyword: Optional[str] = None,
    sort: Optional[List[str]] = None,
    client: Optional[HaloClient] = None,
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
        client = client or HaloClient()
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
        raise HaloMCPError(f"获取标签列表失败：{e}")


async def get_tag(name: str, client: Optional[HaloClient] = None) -> Dict[str, Any]:
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
        client = client or HaloClient()
        await client.ensure_authenticated()

        response = await client.get(f"/apis/content.halo.run/v1alpha1/tags/{name}")
        return response

    except Exception as e:
        raise HaloMCPError(f"获取标签 '{name}' 失败：{e}")


async def create_tag(
    display_name: str,
    slug: Optional[str] = None,
    color: Optional[str] = None,
    cover: Optional[str] = None,
    client: Optional[HaloClient] = None,
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
        client = client or HaloClient()
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
        raise HaloMCPError(f"创建标签失败：{e}")


async def update_tag(
    name: str,
    display_name: Optional[str] = None,
    slug: Optional[str] = None,
    color: Optional[str] = None,
    cover: Optional[str] = None,
    client: Optional[HaloClient] = None,
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
        client = client or HaloClient()
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
        raise HaloMCPError(f"更新标签 '{name}' 失败：{e}")


async def delete_tag(name: str, client: Optional[HaloClient] = None) -> Dict[str, Any]:
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
        client = client or HaloClient()
        await client.ensure_authenticated()

        response = await client.delete(f"/apis/content.halo.run/v1alpha1/tags/{name}")
        return response

    except Exception as e:
        raise HaloMCPError(f"删除标签 '{name}' 失败：{e}")


async def get_tag_posts(
    name: str,
    page: int = 0,
    size: int = 20,
    sort: Optional[List[str]] = None,
    client: Optional[HaloClient] = None,
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
        client = client or HaloClient()
        # 公共接口无需强制认证

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
        raise HaloMCPError(f"获取标签下的文章失败：{e}")


async def list_console_tags(
    page: int = 0,
    size: int = 100,
    keyword: Optional[str] = None,
    sort: Optional[List[str]] = None,
    client: Optional[HaloClient] = None,
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
        client = client or HaloClient()
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
        raise HaloMCPError(f"列出控制台标签失败：{e}")


# MCP Tool 定义
TAG_TOOLS = [
    Tool(
        name="list_tags",
        description="列出所有标签，支持分页和关键词搜索。返回结果中 items 列表的每个标签对象包含：`metadata.name` 字段（内部标识符，如 'tag-LrsQn' 或 'c33ceabb-d8f1-4711-8991-bb8f5c92ad7c'）和 `spec.displayName` 字段（显示名称，如 'Linux'）。重要：创建或更新文章时必须使用 `metadata.name` 字段作为标签标识符，而非 `spec.displayName`。推荐用法：获取标签字典；用于文章的标签选择与校验。",
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
        description="获取指定标签的详细信息。推荐用法：查看标签详情，用于展示或管理。",
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
        description="创建新的标签。推荐用法：新增标签；可选 `slug`、`color`、`cover`。",
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
        description="更新现有标签的信息。推荐用法：修改标签显示名、别名、颜色与封面等。",
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
        description="删除标签。推荐用法：删除指定标签；谨慎确认未被大量使用。",
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
        description="获取指定标签下的文章列表。推荐用法：按标签浏览文章；支持分页与排序。",
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
        description="列出控制台标签（用于后台管理），支持分页和关键词搜索。推荐用法：管理后台场景下的标签查询；与公开标签列表区分使用。",
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
    工具处理器：列出标签。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        标签列表的 JSON 字符串
    """
    try:
        page = args.get("page", 0)
        size = args.get("size", 100)
        keyword = args.get("keyword")
        sort = args.get("sort")

        logger.debug(f"正在列出标签：page={page}, size={size}, keyword={keyword}")

        result = await list_tags(page=page, size=size, keyword=keyword, sort=sort, client=client)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"列出标签出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def get_tag_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：获取标签详情。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        标签详情的 JSON 字符串
    """
    try:
        name = args.get("name")
        if not name:
            error_result = ToolResult.error_result("错误：缺少参数 'name'")
            return error_result.model_dump_json()

        logger.debug(f"正在获取标签：{name}")

        result = await get_tag(name, client=client)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"获取标签出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def create_tag_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：创建新标签。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        操作结果的 JSON 字符串
    """
    try:
        display_name = args.get("display_name")
        if not display_name:
            error_result = ToolResult.error_result("错误：缺少参数 'display_name'")
            return error_result.model_dump_json()

        if len(display_name) > 100:
            error_result = ToolResult.error_result("错误：显示名称过长（最大 100 字符）")
            return error_result.model_dump_json()

        slug = args.get("slug") or slugify(display_name)
        color = args.get("color")
        cover = args.get("cover")

        if color and not re.match(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", color):
            error_result = ToolResult.error_result(
                "错误：color 必须是 3 或 6 位十六进制颜色，如 #FFF 或 #FF0000"
            )
            return error_result.model_dump_json()

        logger.debug(f"正在创建标签：{display_name}")

        result = await create_tag(
            display_name=display_name, slug=slug, color=color, cover=cover, client=client
        )

        tag_name = result.get("metadata", {}).get("name", "")
        success_result = ToolResult.success_result(
            f"✓ 标签 '{display_name}' 创建成功！",
            data={"tag_name": tag_name, "display_name": display_name},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"创建标签出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def update_tag_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：更新标签。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        操作结果的 JSON 字符串
    """
    try:
        name = args.get("name")
        if not name:
            error_result = ToolResult.error_result("错误：缺少参数 'name'")
            return error_result.model_dump_json()

        display_name = args.get("display_name")
        if display_name and len(display_name) > 100:
            error_result = ToolResult.error_result("错误：显示名称过长（最大 100 字符）")
            return error_result.model_dump_json()

        slug = args.get("slug")
        color = args.get("color")
        cover = args.get("cover")

        if color and not re.match(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", color):
            error_result = ToolResult.error_result(
                "错误：color 必须是 3 或 6 位十六进制颜色，如 #FFF 或 #FF0000"
            )
            return error_result.model_dump_json()

        logger.debug(f"正在更新标签：{name}")

        result = await update_tag(
            name=name, display_name=display_name, slug=slug, color=color, cover=cover, client=client
        )

        updated_display_name = result.get("spec", {}).get("displayName", name)
        success_result = ToolResult.success_result(
            f"✓ 标签 '{updated_display_name}' 更新成功！",
            data={"tag_name": name, "updated": True},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"更新标签出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def delete_tag_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：删除标签。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        操作结果的 JSON 字符串
    """
    try:
        name = args.get("name")
        if not name:
            error_result = ToolResult.error_result("错误：缺少参数 'name'")
            return error_result.model_dump_json()

        logger.debug(f"正在删除标签：{name}")

        await delete_tag(name, client=client)

        success_result = ToolResult.success_result(
            f"✓ 标签 '{name}' 删除成功！",
            data={"tag_name": name, "deleted": True},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"删除标签出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def get_posts_under_tag_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：获取标签下的文章。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        文章列表的 JSON 字符串
    """
    try:
        name = args.get("name")
        if not name:
            error_result = ToolResult.error_result("错误：缺少参数 'name'")
            return error_result.model_dump_json()

        page = args.get("page", 0)
        size = args.get("size", 20)
        sort = args.get("sort")

        logger.debug(f"正在获取标签下的文章：{name}, page={page}, size={size}")

        result = await get_tag_posts(name=name, page=page, size=size, sort=sort, client=client)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"获取标签下文章出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def list_console_tags_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：列出控制台标签。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        控制台标签列表的 JSON 字符串
    """
    try:
        page = args.get("page", 0)
        size = args.get("size", 100)
        keyword = args.get("keyword")
        sort = args.get("sort")

        logger.debug(f"正在列出控制台标签：page={page}, size={size}, keyword={keyword}")

        result = await list_console_tags(
            page=page, size=size, keyword=keyword, sort=sort, client=client
        )
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"列出控制台标签出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()

"""Halo MCP 分类管理工具"""

import json
from typing import Any, Dict, List, Optional

from loguru import logger
from mcp.types import Tool

from halo_mcp_server.client.halo_client import HaloClient
from halo_mcp_server.exceptions import HaloMCPError
from halo_mcp_server.models.common import ToolResult
from slugify import slugify


async def list_categories(
    page: int = 0,
    size: int = 50,
    keyword: Optional[str] = None,
    sort: Optional[List[str]] = None,
    client: Optional[HaloClient] = None,
) -> Dict[str, Any]:
    """
    列出所有分类。

    Args:
        page: 页码，默认为 0
        size: 每页大小，默认为 50
        keyword: 搜索关键词
        sort: 排序条件，格式: ["property,(asc|desc)"]

    Returns:
        分类列表数据

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

        # 使用 Extension API 获取完整的分类信息
        response = await client.get("/apis/content.halo.run/v1alpha1/categories", params=params)
        return response

    except Exception as e:
        raise HaloMCPError(f"获取分类列表失败：{e}")


async def get_category(name: str, client: Optional[HaloClient] = None) -> Dict[str, Any]:
    """
    获取指定分类的详细信息。

    Args:
        name: 分类名称/标识符

    Returns:
        分类详细信息

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = client or HaloClient()
        await client.ensure_authenticated()

        response = await client.get(f"/apis/content.halo.run/v1alpha1/categories/{name}")
        return response

    except Exception as e:
        raise HaloMCPError(f"获取分类 '{name}' 失败：{e}")


async def create_category(
    display_name: str,
    slug: Optional[str] = None,
    description: Optional[str] = None,
    cover: Optional[str] = None,
    template: Optional[str] = None,
    priority: int = 0,
    hide_from_list: bool = False,
    prevent_parent_post_cascade_query: bool = False,
    children: Optional[List[str]] = None,
    client: Optional[HaloClient] = None,
) -> Dict[str, Any]:
    """
    创建新分类。

    Args:
        display_name: 分类显示名称
        slug: URL 别名（不提供则自动生成）
        description: 分类描述
        cover: 封面图片 URL
        template: 模板名称
        priority: 优先级，数字越大优先级越高
        hide_from_list: 是否在分类列表中隐藏
        prevent_parent_post_cascade_query: 是否阻止父级分类的级联查询
        children: 子分类名称列表

    Returns:
        创建的分类信息

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = client or HaloClient()
        await client.ensure_authenticated()

        # 构建分类数据
        category_data = {
            "spec": {
                "displayName": display_name,
                "priority": priority,
                "hideFromList": hide_from_list,
                "preventParentPostCascadeQuery": prevent_parent_post_cascade_query,
            },
            "apiVersion": "content.halo.run/v1alpha1",
            "kind": "Category",
            "metadata": {
                "generateName": "category-",
            },
        }

        # 添加可选字段
        if slug:
            category_data["spec"]["slug"] = slug
        if description:
            category_data["spec"]["description"] = description
        if cover:
            category_data["spec"]["cover"] = cover
        if template:
            category_data["spec"]["template"] = template
        if children:
            category_data["spec"]["children"] = children

        response = await client.post(
            "/apis/content.halo.run/v1alpha1/categories", json=category_data
        )
        return response

    except Exception as e:
        raise HaloMCPError(f"创建分类失败：{e}")


async def update_category(
    name: str,
    display_name: Optional[str] = None,
    slug: Optional[str] = None,
    description: Optional[str] = None,
    cover: Optional[str] = None,
    template: Optional[str] = None,
    priority: Optional[int] = None,
    hide_from_list: Optional[bool] = None,
    prevent_parent_post_cascade_query: Optional[bool] = None,
    children: Optional[List[str]] = None,
    client: Optional[HaloClient] = None,
) -> Dict[str, Any]:
    """
    更新现有分类。

    Args:
        name: 分类名称/标识符
        display_name: 新的显示名称
        slug: 新的 URL 别名
        description: 新的描述
        cover: 新的封面图片 URL
        template: 新的模板名称
        priority: 新的优先级
        hide_from_list: 是否在分类列表中隐藏
        prevent_parent_post_cascade_query: 是否阻止父级分类的级联查询
        children: 新的子分类名称列表

    Returns:
        更新后的分类信息

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = client or HaloClient()
        await client.ensure_authenticated()

        # 先获取现有分类信息
        existing_category = await client.get(f"/apis/content.halo.run/v1alpha1/categories/{name}")

        # 更新指定字段
        if display_name is not None:
            existing_category["spec"]["displayName"] = display_name
        if slug is not None:
            existing_category["spec"]["slug"] = slug
        if description is not None:
            existing_category["spec"]["description"] = description
        if cover is not None:
            existing_category["spec"]["cover"] = cover
        if template is not None:
            existing_category["spec"]["template"] = template
        if priority is not None:
            existing_category["spec"]["priority"] = priority
        if hide_from_list is not None:
            existing_category["spec"]["hideFromList"] = hide_from_list
        if prevent_parent_post_cascade_query is not None:
            existing_category["spec"][
                "preventParentPostCascadeQuery"
            ] = prevent_parent_post_cascade_query
        if children is not None:
            existing_category["spec"]["children"] = children

        response = await client.put(
            f"/apis/content.halo.run/v1alpha1/categories/{name}",
            json=existing_category,
        )
        return response

    except Exception as e:
        raise HaloMCPError(f"更新分类 '{name}' 失败：{e}")


async def delete_category(name: str, client: Optional[HaloClient] = None) -> Dict[str, Any]:
    """
    删除分类。

    Args:
        name: 分类名称/标识符

    Returns:
        删除操作结果

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = client or HaloClient()
        await client.ensure_authenticated()

        response = await client.delete(f"/apis/content.halo.run/v1alpha1/categories/{name}")
        return response

    except Exception as e:
        raise HaloMCPError(f"删除分类 '{name}' 失败：{e}")


async def get_category_posts(
    name: str,
    page: int = 0,
    size: int = 20,
    sort: Optional[List[str]] = None,
    client: Optional[HaloClient] = None,
) -> Dict[str, Any]:
    """
    获取指定分类下的文章列表。

    Args:
        name: 分类名称/标识符
        page: 页码，默认为 0
        size: 每页大小，默认为 20
        sort: 排序条件，格式: ["property,(asc|desc)"]

    Returns:
        分类下的文章列表

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = client or HaloClient()

        params = {"page": page, "size": size}
        if sort:
            params["sort"] = sort

        # 使用 Public API 获取分类下的文章
        response = await client.get(
            f"/apis/api.content.halo.run/v1alpha1/categories/{name}/posts",
            params=params,
        )
        return response

    except Exception as e:
        raise HaloMCPError(f"获取分类下文章失败：{e}")


# MCP Tool 定义
CATEGORY_TOOLS = [
    Tool(
        name="list_categories",
        description="列出所有分类，支持分页和关键词搜索。返回结果中 items 列表的每个分类对象包含：'name' 字段（内部标识符，如 'category-yJfRu'）和 'display_name' 字段（显示名称，如 'Linux'）。重要：创建或更新文章时必须使用 'name' 字段作为分类标识符，而非 'display_name'。推荐用法：获取分类字典；配合文章创建/更新时选取正确的内部标识符。",
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
                    "description": "每页数量（默认：50）",
                    "default": 50,
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
        name="get_category",
        description="获取指定分类的详细信息。推荐用法：查看某分类详情，用于校验或展示。",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "分类名称/标识符（必填）",
                },
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="create_category",
        description="创建新的分类。推荐用法：新增分类；可选 `slug`、`cover`、`template`、`priority` 等。",
        inputSchema={
            "type": "object",
            "properties": {
                "display_name": {
                    "type": "string",
                    "description": "分类显示名称（必填）",
                },
                "slug": {
                    "type": "string",
                    "description": "URL 别名（不提供则自动生成）",
                },
                "description": {
                    "type": "string",
                    "description": "分类描述",
                },
                "cover": {
                    "type": "string",
                    "description": "封面图片 URL",
                },
                "template": {
                    "type": "string",
                    "description": "模板名称",
                },
                "priority": {
                    "type": "number",
                    "description": "优先级，数字越大优先级越高（默认：0）",
                    "default": 0,
                },
                "hide_from_list": {
                    "type": "boolean",
                    "description": "是否在分类列表中隐藏（默认：false）",
                    "default": False,
                },
                "prevent_parent_post_cascade_query": {
                    "type": "boolean",
                    "description": "是否阻止父级分类的级联查询（默认：false）",
                    "default": False,
                },
                "children": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "子分类名称列表",
                },
            },
            "required": ["display_name"],
        },
    ),
    Tool(
        name="update_category",
        description="更新现有分类的信息。推荐用法：修改分类的显示名、描述、封面、排序与子分类列表等。",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "分类名称/标识符（必填）",
                },
                "display_name": {
                    "type": "string",
                    "description": "新的显示名称",
                },
                "slug": {
                    "type": "string",
                    "description": "新的 URL 别名",
                },
                "description": {
                    "type": "string",
                    "description": "新的描述",
                },
                "cover": {
                    "type": "string",
                    "description": "新的封面图片 URL",
                },
                "template": {
                    "type": "string",
                    "description": "新的模板名称",
                },
                "priority": {
                    "type": "number",
                    "description": "新的优先级",
                },
                "hide_from_list": {
                    "type": "boolean",
                    "description": "是否在分类列表中隐藏",
                },
                "prevent_parent_post_cascade_query": {
                    "type": "boolean",
                    "description": "是否阻止父级分类的级联查询",
                },
                "children": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "新的子分类名称列表",
                },
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="delete_category",
        description="删除分类。推荐用法：删除指定分类；先确认无关键依赖。",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "分类名称/标识符（必填）",
                },
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="get_category_posts",
        description="获取指定分类下的文章列表。推荐用法：按分类浏览文章；支持分页与排序。",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "分类名称/标识符（必填）",
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
]


# Tool handler functions for MCP


async def list_categories_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：列出分类。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        分类列表的 JSON 字符串
    """
    try:
        page = args.get("page", 0)
        size = args.get("size", 50)
        keyword = args.get("keyword")
        sort = args.get("sort")

        logger.debug(f"正在列出分类：page={page}, size={size}, keyword={keyword}")

        result = await list_categories(
            page=page, size=size, keyword=keyword, sort=sort, client=client
        )
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"列出分类出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def get_category_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：获取分类详情。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        分类详情的 JSON 字符串
    """
    try:
        name = args.get("name")
        if not name:
            error_result = ToolResult.error_result("错误：缺少参数 'name'")
            return error_result.model_dump_json()

        logger.debug(f"正在获取分类：{name}")

        result = await get_category(name, client=client)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"获取分类出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def create_category_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：创建新分类。

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
        description = args.get("description")
        cover = args.get("cover")
        template = args.get("template")
        priority = args.get("priority", 0)
        try:
            priority_int = int(priority)
        except (TypeError, ValueError):
            error_result = ToolResult.error_result("错误：priority 必须为整数")
            return error_result.model_dump_json()
        if priority_int < 0 or priority_int > 1000:
            error_result = ToolResult.error_result("错误：priority 范围为 0–1000")
            return error_result.model_dump_json()
        priority = priority_int

        hide_from_list = args.get("hide_from_list", False)
        prevent_parent_post_cascade_query = args.get("prevent_parent_post_cascade_query", False)
        children = args.get("children", [])

        logger.debug(f"正在创建分类：{display_name}")

        result = await create_category(
            display_name=display_name,
            slug=slug,
            description=description,
            cover=cover,
            template=template,
            priority=priority,
            hide_from_list=hide_from_list,
            prevent_parent_post_cascade_query=prevent_parent_post_cascade_query,
            children=children,
            client=client,
        )

        category_name = result.get("metadata", {}).get("name", "")
        success_result = ToolResult.success_result(
            f"✓ 分类 '{display_name}' 创建成功！",
            data={"category_name": category_name, "display_name": display_name},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"创建分类出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def update_category_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：更新分类。

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
        description = args.get("description")
        cover = args.get("cover")
        template = args.get("template")
        priority = args.get("priority")
        if priority is not None:
            try:
                priority_int = int(priority)
            except (TypeError, ValueError):
                error_result = ToolResult.error_result("错误：priority 必须为整数")
                return error_result.model_dump_json()
            if priority_int < 0 or priority_int > 1000:
                error_result = ToolResult.error_result("错误：priority 范围为 0–1000")
                return error_result.model_dump_json()
            priority = priority_int

        hide_from_list = args.get("hide_from_list")
        prevent_parent_post_cascade_query = args.get("prevent_parent_post_cascade_query")
        children = args.get("children")

        logger.debug(f"正在更新分类：{name}")

        result = await update_category(
            name=name,
            display_name=display_name,
            slug=slug,
            description=description,
            cover=cover,
            template=template,
            priority=priority,
            hide_from_list=hide_from_list,
            prevent_parent_post_cascade_query=prevent_parent_post_cascade_query,
            children=children,
            client=client,
        )

        updated_display_name = result.get("spec", {}).get("displayName", name)
        success_result = ToolResult.success_result(
            f"✓ 分类 '{updated_display_name}' 更新成功！",
            data={"category_name": name, "updated": True},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"更新分类出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def delete_category_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：删除分类。

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

        logger.debug(f"正在删除分类：{name}")

        await delete_category(name, client=client)

        success_result = ToolResult.success_result(
            f"✓ 分类 '{name}' 删除成功！",
            data={"category_name": name, "deleted": True},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"删除分类出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def get_posts_under_category_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：获取分类下的文章。

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

        logger.debug(f"正在获取分类下的文章：{name}, page={page}, size={size}")

        result = await get_category_posts(name=name, page=page, size=size, sort=sort, client=client)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"获取分类下文章出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()

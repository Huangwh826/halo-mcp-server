"""Category management tools for Halo MCP."""

import json
from typing import Any, Dict, List, Optional

from loguru import logger
from mcp.types import Tool

from halo_mcp_server.client.halo_client import HaloClient
from halo_mcp_server.exceptions import HaloMCPError
from halo_mcp_server.models.common import ToolResult


async def list_categories(
    page: int = 0,
    size: int = 50,
    keyword: Optional[str] = None,
    sort: Optional[List[str]] = None,
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
        client = HaloClient()
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
        raise HaloMCPError(f"Failed to list categories: {e}")


async def get_category(name: str) -> Dict[str, Any]:
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
        client = HaloClient()
        await client.ensure_authenticated()

        response = await client.get(f"/apis/content.halo.run/v1alpha1/categories/{name}")
        return response

    except Exception as e:
        raise HaloMCPError(f"Failed to get category '{name}': {e}")


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
        client = HaloClient()
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
        raise HaloMCPError(f"Failed to create category: {e}")


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
        client = HaloClient()
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
        raise HaloMCPError(f"Failed to update category '{name}': {e}")


async def delete_category(name: str) -> Dict[str, Any]:
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
        client = HaloClient()
        await client.ensure_authenticated()

        response = await client.delete(f"/apis/content.halo.run/v1alpha1/categories/{name}")
        return response

    except Exception as e:
        raise HaloMCPError(f"Failed to delete category '{name}': {e}")


async def get_category_posts(
    name: str,
    page: int = 0,
    size: int = 20,
    sort: Optional[List[str]] = None,
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
        client = HaloClient()

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
        raise HaloMCPError(f"Failed to get posts for category '{name}': {e}")


# MCP Tool 定义
CATEGORY_TOOLS = [
    Tool(
        name="list_categories",
        description="列出所有分类，支持分页和关键词搜索。返回结果中 items 列表的每个分类对象包含：'name' 字段（内部标识符，如 'category-yJfRu'）和 'display_name' 字段（显示名称，如 'Linux'）。重要：创建或更新文章时必须使用 'name' 字段作为分类标识符，而非 'display_name'。",
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
        description="获取指定分类的详细信息",
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
        description="创建新的分类",
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
        description="更新现有分类的信息",
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
        description="删除分类",
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
        description="获取指定分类下的文章列表",
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
    Tool handler for listing categories.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        JSON string of categories list
    """
    try:
        page = args.get("page", 0)
        size = args.get("size", 50)
        keyword = args.get("keyword")
        sort = args.get("sort")

        logger.debug(f"Listing categories: page={page}, size={size}, keyword={keyword}")

        result = await list_categories(page=page, size=size, keyword=keyword, sort=sort)

        # Format the result for better readability
        categories = result.get("items", [])
        formatted_categories = []

        for cat in categories:
            spec = cat.get("spec", {})
            metadata = cat.get("metadata", {})
            status = cat.get("status", {})

            formatted_cat = {
                "name": metadata.get("name", ""),
                "display_name": spec.get("displayName", ""),
                "slug": spec.get("slug", ""),
                "description": spec.get("description", ""),
                "cover": spec.get("cover", ""),
                "template": spec.get("template", ""),
                "priority": spec.get("priority", 0),
                "hide_from_list": spec.get("hideFromList", False),
                "children": spec.get("children", []),
                "post_count": status.get("postCount", 0),
                "visible_post_count": status.get("visiblePostCount", 0),
                "creation_timestamp": metadata.get("creationTimestamp", ""),
                "permalink": status.get("permalink", ""),
            }
            formatted_categories.append(formatted_cat)

        result["items"] = formatted_categories

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Error listing categories: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def get_category_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for getting category details.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        JSON string of category details
    """
    try:
        name = args.get("name")
        if not name:
            error_result = ToolResult.error_result("Error: 'name' parameter is required")
            return error_result.model_dump_json()

        logger.debug(f"Getting category: {name}")

        result = await get_category(name)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Error getting category: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def create_category_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for creating a new category.

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

        # Validate display_name length
        if len(display_name) > 100:
            error_result = ToolResult.error_result(
                "Error: Display name too long (max 100 characters)"
            )
            return error_result.model_dump_json()

        slug = args.get("slug")
        description = args.get("description")
        cover = args.get("cover")
        template = args.get("template")
        priority = args.get("priority", 0)
        hide_from_list = args.get("hide_from_list", False)
        prevent_parent_post_cascade_query = args.get("prevent_parent_post_cascade_query", False)
        children = args.get("children")

        logger.debug(f"Creating category: {display_name}")

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
        )

        category_name = result.get("metadata", {}).get("name", "")
        success_result = ToolResult.success_result(
            f"✓ Category '{display_name}' created successfully!",
            data={"category_name": category_name, "display_name": display_name},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"Error creating category: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def update_category_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for updating a category.

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
        description = args.get("description")
        cover = args.get("cover")
        template = args.get("template")
        priority = args.get("priority")
        hide_from_list = args.get("hide_from_list")
        prevent_parent_post_cascade_query = args.get("prevent_parent_post_cascade_query")
        children = args.get("children")

        logger.debug(f"Updating category: {name}")

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
        )

        updated_display_name = result.get("spec", {}).get("displayName", name)
        success_result = ToolResult.success_result(
            f"✓ Category '{updated_display_name}' updated successfully!",
            data={"category_name": name, "updated": True},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"Error updating category: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def delete_category_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for deleting a category.

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

        logger.debug(f"Deleting category: {name}")

        await delete_category(name)

        success_result = ToolResult.success_result(
            f"✓ Category '{name}' deleted successfully!",
            data={"category_name": name, "deleted": True},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"Error deleting category: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def get_posts_under_category_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for getting posts under a category.

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

        logger.debug(f"Getting posts under category: {name}, page={page}, size={size}")

        result = await get_category_posts(name=name, page=page, size=size, sort=sort)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Error getting posts under category: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()

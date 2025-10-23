"""Attachment management tools for Halo MCP."""

"""Attachment management tools for Halo MCP."""

import base64
import json
import os
from typing import Any, Dict, List, Optional

from loguru import logger
from mcp.types import Tool

from halo_mcp_server.client.halo_client import HaloClient
from halo_mcp_server.exceptions import HaloMCPError
from halo_mcp_server.models.common import ToolResult


async def list_attachments(
    page: int = 0,
    size: int = 50,
    keyword: Optional[str] = None,
    accepts: Optional[List[str]] = None,
    group_name: Optional[str] = None,
    sort: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    搜索和列出附件。

    Args:
        page: 页码，默认为 0
        size: 每页大小，默认为 50
        keyword: 搜索关键词
        accepts: 接受的文件类型，如 ["image/*", "video/*"]
        group_name: 附件分组名称
        sort: 排序条件，格式: ["property,(asc|desc)"]

    Returns:
        附件列表数据

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = HaloClient()
        await client.ensure_authenticated()

        params = {"page": page, "size": size}
        if keyword:
            params["keyword"] = keyword
        if accepts:
            params["accepts"] = accepts
        if group_name:
            params["groupName"] = group_name
        if sort:
            params["sort"] = sort

        response = await client.get(
            "/apis/api.console.halo.run/v1alpha1/attachments", params=params
        )
        return response

    except Exception as e:
        raise HaloMCPError(f"Failed to list attachments: {e}")


async def get_attachment(name: str) -> Dict[str, Any]:
    """
    获取指定附件的详细信息。

    Args:
        name: 附件名称/标识符

    Returns:
        附件详细信息

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = HaloClient()
        await client.ensure_authenticated()

        response = await client.get(f"/apis/storage.halo.run/v1alpha1/attachments/{name}")
        return response

    except Exception as e:
        raise HaloMCPError(f"Failed to get attachment '{name}': {e}")


async def upload_attachment(
    file_path: str,
    policy_name: str = "default-policy",
    group_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    上传本地文件作为附件。

    Args:
        file_path: 本地文件路径
        policy_name: 存储策略名称，默认为 "default-policy"
        group_name: 附件分组名称

    Returns:
        上传后的附件信息

    Raises:
        HaloMCPError: 文件不存在或上传失败
    """
    try:
        if not os.path.exists(file_path):
            raise HaloMCPError(f"File not found: {file_path}")

        client = HaloClient()
        await client.ensure_authenticated()

        # 读取文件内容
        with open(file_path, "rb") as f:
            file_content = f.read()

        # 获取文件名
        filename = os.path.basename(file_path)

        # 准备multipart/form-data数据
        files = {"file": (filename, file_content)}

        # 尝试使用 UC API 上传（用户中心API）
        # 这个端点通常有更宽松的权限要求
        try:
            response = await client.post(
                "/apis/uc.api.storage.halo.run/v1alpha1/attachments/-/upload",
                files=files,
            )
            logger.info(f"Successfully uploaded via UC API: {filename}")
            return response
        except Exception as uc_error:
            logger.warning(f"UC API upload failed: {uc_error}, trying Console API")

            # 如果UC API失败，尝试Console API
            data = {"policyName": policy_name}
            if group_name:
                data["groupName"] = group_name

            response = await client.post(
                "/apis/api.console.halo.run/v1alpha1/attachments/upload",
                files=files,
                data=data,
            )
            logger.info(f"Successfully uploaded via Console API: {filename}")
            return response

    except Exception as e:
        raise HaloMCPError(f"Failed to upload attachment: {e}")


async def upload_attachment_from_url(
    url: str,
    policy_name: str = "default-policy",
    group_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    从 URL 上传附件。

    Args:
        url: 文件 URL
        policy_name: 存储策略名称，默认为 "default-policy"
        group_name: 附件分组名称

    Returns:
        上传后的附件信息

    Raises:
        HaloMCPError: URL 无效或上传失败
    """
    try:
        client = HaloClient()
        await client.ensure_authenticated()

        # 从URL提取文件名
        filename = url.split("/")[-1].split("?")[0] or "downloaded_file"

        # 使用 Console API
        # 端点: POST /apis/api.console.halo.run/v1alpha1/attachments/-/upload-from-url
        # 根据API文档，需要的参数：filename, groupName, policyName, url
        upload_data = {
            "url": url,
            "filename": filename,  # API文档要求的参数
            "policyName": policy_name,
            "groupName": group_name if group_name else "",  # 空字符串，不是None
        }

        response = await client.post(
            "/apis/api.console.halo.run/v1alpha1/attachments/-/upload-from-url",
            json=upload_data,
        )
        logger.info(f"Successfully uploaded from URL: {url}")
        return response

    except Exception as e:
        raise HaloMCPError(f"Failed to upload attachment from URL: {e}")


async def delete_attachment(name: str) -> Dict[str, Any]:
    """
    删除附件。

    Args:
        name: 附件名称/标识符

    Returns:
        删除操作结果

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = HaloClient()
        await client.ensure_authenticated()

        response = await client.delete(f"/apis/storage.halo.run/v1alpha1/attachments/{name}")
        return response

    except Exception as e:
        raise HaloMCPError(f"Failed to delete attachment '{name}': {e}")


async def list_attachment_groups(
    page: int = 0,
    size: int = 100,
    sort: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    列出附件分组。

    Args:
        page: 页码，默认为 0
        size: 每页大小，默认为 100
        sort: 排序条件，格式: ["property,(asc|desc)"]

    Returns:
        附件分组列表

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = HaloClient()
        await client.ensure_authenticated()

        params = {"page": page, "size": size}
        if sort:
            params["sort"] = sort

        response = await client.get("/apis/storage.halo.run/v1alpha1/groups", params=params)
        return response

    except Exception as e:
        raise HaloMCPError(f"Failed to list attachment groups: {e}")


async def create_attachment_group(
    display_name: str,
) -> Dict[str, Any]:
    """
    创建附件分组。

    Args:
        display_name: 分组显示名称

    Returns:
        创建的分组信息

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = HaloClient()
        await client.ensure_authenticated()

        group_data = {
            "spec": {
                "displayName": display_name,
            },
            "apiVersion": "storage.halo.run/v1alpha1",
            "kind": "Group",
            "metadata": {
                "generateName": "attachment-group-",
            },
        }

        response = await client.post("/apis/storage.halo.run/v1alpha1/groups", json=group_data)
        return response

    except Exception as e:
        raise HaloMCPError(f"Failed to create attachment group: {e}")


async def get_attachment_policies() -> Dict[str, Any]:
    """
    获取存储策略列表。

    Returns:
        存储策略列表

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = HaloClient()
        await client.ensure_authenticated()

        response = await client.get("/apis/storage.halo.run/v1alpha1/policies")
        return response

    except Exception as e:
        raise HaloMCPError(f"Failed to get attachment policies: {e}")


# MCP Tool 定义
ATTACHMENT_TOOLS = [
    Tool(
        name="list_attachments",
        description="搜索和列出附件，支持分页、关键词搜索和文件类型过滤",
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
                "accepts": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "接受的文件类型，如 ['image/*', 'video/*']",
                },
                "group_name": {
                    "type": "string",
                    "description": "附件分组名称",
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
        name="get_attachment",
        description="获取指定附件的详细信息",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "附件名称/标识符（必填）",
                },
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="upload_attachment",
        description="上传本地文件作为附件",
        inputSchema={
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "本地文件路径（必填）",
                },
                "policy_name": {
                    "type": "string",
                    "description": "存储策略名称（默认：default-policy）",
                    "default": "default-policy",
                },
                "group_name": {
                    "type": "string",
                    "description": "附件分组名称",
                },
            },
            "required": ["file_path"],
        },
    ),
    Tool(
        name="upload_attachment_from_url",
        description="从 URL 上传附件",
        inputSchema={
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "文件 URL（必填）",
                },
                "policy_name": {
                    "type": "string",
                    "description": "存储策略名称（默认：default-policy）",
                    "default": "default-policy",
                },
                "group_name": {
                    "type": "string",
                    "description": "附件分组名称",
                },
            },
            "required": ["url"],
        },
    ),
    Tool(
        name="delete_attachment",
        description="删除附件",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "附件名称/标识符（必填）",
                },
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="list_attachment_groups",
        description="列出附件分组",
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
                "sort": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "排序条件，格式: ['property,(asc|desc)']",
                },
            },
        },
    ),
    Tool(
        name="create_attachment_group",
        description="创建附件分组",
        inputSchema={
            "type": "object",
            "properties": {
                "display_name": {
                    "type": "string",
                    "description": "分组显示名称（必填）",
                },
            },
            "required": ["display_name"],
        },
    ),
    Tool(
        name="get_attachment_policies",
        description="获取存储策略列表",
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
]


# Tool handler functions for MCP


async def list_attachments_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for listing attachments.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        JSON string of attachments list
    """
    try:
        page = args.get("page", 0)
        size = args.get("size", 50)
        keyword = args.get("keyword")
        accepts = args.get("accepts")
        group_name = args.get("group_name")
        sort = args.get("sort")

        logger.debug(f"Listing attachments: page={page}, size={size}, keyword={keyword}")

        result = await list_attachments(
            page=page, size=size, keyword=keyword, accepts=accepts, group_name=group_name, sort=sort
        )
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Error listing attachments: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def get_attachment_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for getting attachment details.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        JSON string of attachment details
    """
    try:
        name = args.get("name")
        if not name:
            error_result = ToolResult.error_result("Error: 'name' parameter is required")
            return error_result.model_dump_json()

        logger.debug(f"Getting attachment: {name}")

        result = await get_attachment(name)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Error getting attachment: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def upload_attachment_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for uploading attachment.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        JSON string of operation result
    """
    try:
        file_path = args.get("file_path")
        if not file_path:
            error_result = ToolResult.error_result("Error: 'file_path' parameter is required")
            return error_result.model_dump_json()

        policy_name = args.get("policy_name", "default-policy")
        group_name = args.get("group_name")

        logger.debug(f"Uploading attachment: {file_path}")

        result = await upload_attachment(
            file_path=file_path, policy_name=policy_name, group_name=group_name
        )

        attachment_name = result.get("metadata", {}).get("name", "")
        success_result = ToolResult.success_result(
            f"✓ Attachment uploaded successfully!",
            data={"attachment_name": attachment_name, "file_path": file_path},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"Error uploading attachment: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def upload_attachment_from_url_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for uploading attachment from URL.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        JSON string of operation result
    """
    try:
        url = args.get("url")
        if not url:
            error_result = ToolResult.error_result("Error: 'url' parameter is required")
            return error_result.model_dump_json()

        policy_name = args.get("policy_name", "default-policy")
        group_name = args.get("group_name")

        logger.debug(f"Uploading attachment from URL: {url}")

        result = await upload_attachment_from_url(
            url=url, policy_name=policy_name, group_name=group_name
        )

        attachment_name = result.get("metadata", {}).get("name", "")
        success_result = ToolResult.success_result(
            f"✓ Attachment uploaded from URL successfully!",
            data={"attachment_name": attachment_name, "url": url},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"Error uploading attachment from URL: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def delete_attachment_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for deleting attachment.

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

        logger.debug(f"Deleting attachment: {name}")

        await delete_attachment(name)

        success_result = ToolResult.success_result(
            f"✓ Attachment '{name}' deleted successfully!",
            data={"attachment_name": name, "deleted": True},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"Error deleting attachment: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def list_attachment_groups_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for listing attachment groups.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        JSON string of attachment groups list
    """
    try:
        page = args.get("page", 0)
        size = args.get("size", 100)
        sort = args.get("sort")

        logger.debug(f"Listing attachment groups: page={page}, size={size}")

        result = await list_attachment_groups(page=page, size=size, sort=sort)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Error listing attachment groups: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def create_attachment_group_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for creating attachment group.

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

        logger.debug(f"Creating attachment group: {display_name}")

        result = await create_attachment_group(display_name=display_name)

        group_name = result.get("metadata", {}).get("name", "")
        success_result = ToolResult.success_result(
            f"✓ Attachment group '{display_name}' created successfully!",
            data={"group_name": group_name, "display_name": display_name},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"Error creating attachment group: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()


async def list_storage_policies_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    Tool handler for listing storage policies.

    Args:
        client: Halo API client
        args: Tool arguments

    Returns:
        JSON string of storage policies list
    """
    try:
        logger.debug("Listing storage policies")

        result = await get_attachment_policies()
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Error listing storage policies: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error: {str(e)}")
        return error_result.model_dump_json()

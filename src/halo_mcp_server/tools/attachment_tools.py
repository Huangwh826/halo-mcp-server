"""Halo MCP 附件管理工具"""

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
    client: Optional[HaloClient] = None,
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
        client = client or HaloClient()
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
        raise HaloMCPError(f"获取附件列表失败：{e}")


async def get_attachment(name: str, client: Optional[HaloClient] = None) -> Dict[str, Any]:
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
        client = client or HaloClient()
        await client.ensure_authenticated()

        response = await client.get(f"/apis/storage.halo.run/v1alpha1/attachments/{name}")
        return response

    except Exception as e:
        raise HaloMCPError(f"获取附件 '{name}' 失败：{e}")


async def upload_attachment(
    file_path: str,
    policy_name: str = "default-policy",
    group_name: Optional[str] = None,
    client: Optional[HaloClient] = None,
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

        client = client or HaloClient()
        await client.ensure_authenticated()

        # 读取文件内容
        with open(file_path, "rb") as f:
            file_content = f.read()

        # 获取文件名
        filename = os.path.basename(file_path)

        # 准备multipart/form-data数据
        files = {"file": (filename, file_content)}

        uc_error_obj: Optional[Exception] = None

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
            uc_error_obj = uc_error
            logger.warning(f"UC API upload failed: {uc_error}, trying Console API")

            # 如果UC API失败，尝试Console API
            data = {"policyName": policy_name}
            if group_name:
                data["groupName"] = group_name

            try:
                response = await client.post(
                    "/apis/api.console.halo.run/v1alpha1/attachments/upload",
                    files=files,
                    data=data,
                )
                logger.info(f"Successfully uploaded via Console API: {filename}")
                return response
            except Exception as console_error:
                # 合并两次失败的详细信息，便于定位问题
                raise HaloMCPError(
                    f"Failed to upload attachment. UC error: {uc_error_obj}; Console error: {console_error}"
                )

    except Exception as e:
        raise HaloMCPError(f"Failed to upload attachment: {e}")


async def upload_attachment_from_url(
    url: str,
    policy_name: str = "default-policy",
    group_name: Optional[str] = None,
    client: Optional[HaloClient] = None,
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
        client = client or HaloClient()
        await client.ensure_authenticated()

        # 从URL提取文件名
        filename = url.split("/")[-1].split("?")[0] or "downloaded_file"

        uc_error_obj: Optional[Exception] = None

        # 先尝试 UC API（只需要 url 与可选 filename）
        try:
            response = await client.post(
                "/apis/uc.api.storage.halo.run/v1alpha1/attachments/-/upload-from-url",
                json={"url": url, "filename": filename},
            )
            logger.info(f"Successfully uploaded from URL via UC API: {url}")
            return response
        except Exception as uc_error:
            uc_error_obj = uc_error
            logger.warning(f"UC API upload-from-url failed: {uc_error}, trying Console API")

        # UC 失败后，回退到 Console API
        # Console 端点需要的参数：url、policyName，filename/groupName 可选
        upload_data: Dict[str, Any] = {
            "url": url,
            "filename": filename,
            "policyName": policy_name,
        }
        if group_name:
            upload_data["groupName"] = group_name

        try:
            response = await client.post(
                "/apis/api.console.halo.run/v1alpha1/attachments/-/upload-from-url",
                json=upload_data,
            )
            logger.info(f"Successfully uploaded from URL via Console API: {url}")
            return response
        except Exception as console_error:
            raise HaloMCPError(
                f"Failed to upload attachment from URL. UC error: {uc_error_obj}; Console error: {console_error}"
            )

    except Exception as e:
        raise HaloMCPError(f"Failed to upload attachment from URL: {e}")


async def delete_attachment(name: str, client: Optional[HaloClient] = None) -> Dict[str, Any]:
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
        client = client or HaloClient()
        await client.ensure_authenticated()

        response = await client.delete(f"/apis/storage.halo.run/v1alpha1/attachments/{name}")
        return response

    except Exception as e:
        raise HaloMCPError(f"删除附件 '{name}' 失败：{e}")


async def list_attachment_groups(
    page: int = 0,
    size: int = 100,
    sort: Optional[List[str]] = None,
    client: Optional[HaloClient] = None,
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
        client = client or HaloClient()
        await client.ensure_authenticated()

        params = {"page": page, "size": size}
        if sort:
            params["sort"] = sort

        response = await client.get("/apis/storage.halo.run/v1alpha1/groups", params=params)
        return response

    except Exception as e:
        raise HaloMCPError(f"列出附件分组失败：{e}")


async def create_attachment_group(
    display_name: str,
    client: Optional[HaloClient] = None,
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
        client = client or HaloClient()
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
        raise HaloMCPError(f"创建附件分组失败：{e}")


async def get_attachment_policies(client: Optional[HaloClient] = None) -> Dict[str, Any]:
    """
    获取存储策略列表。

    Returns:
        存储策略列表

    Raises:
        HaloMCPError: API 调用失败
    """
    try:
        client = client or HaloClient()
        await client.ensure_authenticated()

        response = await client.get("/apis/storage.halo.run/v1alpha1/policies")
        return response

    except Exception as e:
        raise HaloMCPError(f"获取附件列表失败：{e}")


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
    工具处理器：列出附件。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        附件列表的 JSON 字符串
    """
    try:
        page = args.get("page", 0)
        size = args.get("size", 50)
        keyword = args.get("keyword")
        accepts = args.get("accepts")
        group_name = args.get("group_name")
        sort = args.get("sort")

        logger.debug(
            f"正在列出附件：page={page}, size={size}, keyword={keyword}, accepts={accepts}"
        )

        result = await list_attachments(
            page=page,
            size=size,
            keyword=keyword,
            accepts=accepts,
            group_name=group_name,
            sort=sort,
            client=client,
        )
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"列出附件出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def get_attachment_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：获取附件详情。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        附件详情的 JSON 字符串
    """
    try:
        name = args.get("name")
        if not name:
            error_result = ToolResult.error_result("错误：缺少参数 'name'")
            return error_result.model_dump_json()

        logger.debug(f"正在获取附件：{name}")

        result = await get_attachment(name, client=client)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"获取附件出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def upload_attachment_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：上传本地附件。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        操作结果的 JSON 字符串
    """
    try:
        file_path = args.get("file_path")
        if not file_path:
            error_result = ToolResult.error_result("错误：缺少参数 'file_path'")
            return error_result.model_dump_json()

        policy_name = args.get("policy_name", "default-policy")
        group_name = args.get("group_name")

        logger.debug(
            f"正在上传附件：file_path={file_path}, policy={policy_name}, group={group_name}"
        )

        result = await upload_attachment(
            file_path=file_path, policy_name=policy_name, group_name=group_name, client=client
        )

        logger.info(f"附件上传完成：{result}")

        success_result = ToolResult.success_result(
            "✓ 附件上传成功！",
            data=result,
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"上传附件出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def upload_attachment_from_url_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：从 URL 上传附件。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        操作结果的 JSON 字符串
    """
    try:
        url = args.get("url")
        if not url:
            error_result = ToolResult.error_result("错误：缺少参数 'url'")
            return error_result.model_dump_json()

        policy_name = args.get("policy_name", "default-policy")
        group_name = args.get("group_name")

        logger.debug(f"正在从 URL 上传附件：url={url}, policy={policy_name}, group={group_name}")

        result = await upload_attachment_from_url(
            url=url, policy_name=policy_name, group_name=group_name, client=client
        )

        logger.info(f"URL 附件上传完成：{result}")

        success_result = ToolResult.success_result(
            "✓ 附件从 URL 上传成功！",
            data=result,
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"从 URL 上传附件出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def delete_attachment_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：删除附件。

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

        logger.debug(f"正在删除附件：{name}")

        await delete_attachment(name, client=client)

        success_result = ToolResult.success_result(
            f"✓ 附件 '{name}' 删除成功！",
            data={"attachment_name": name, "deleted": True},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"删除附件出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def list_attachment_groups_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：列出附件分组。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        附件分组列表的 JSON 字符串
    """
    try:
        page = args.get("page", 0)
        size = args.get("size", 100)
        sort = args.get("sort")

        logger.debug(f"正在列出附件分组：page={page}, size={size}")

        result = await list_attachment_groups(page=page, size=size, sort=sort, client=client)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"列出附件分组出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def create_attachment_group_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：创建附件分组。

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

        logger.debug(f"正在创建附件分组：{display_name}")

        result = await create_attachment_group(display_name=display_name, client=client)

        success_result = ToolResult.success_result(
            f"✓ 附件分组 '{display_name}' 创建成功！",
            data={"display_name": display_name},
        )
        return success_result.model_dump_json()

    except Exception as e:
        logger.error(f"创建附件分组出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()


async def list_storage_policies_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """
    工具处理器：列出存储策略。

    参数:
        client: Halo API 客户端
        args: 工具参数

    返回:
        存储策略列表的 JSON 字符串
    """
    try:
        logger.debug("正在列出存储策略")
        result = await get_attachment_policies(client=client)
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"列出存储策略出错：{e}", exc_info=True)
        error_result = ToolResult.error_result(f"错误：{str(e)}")
        return error_result.model_dump_json()

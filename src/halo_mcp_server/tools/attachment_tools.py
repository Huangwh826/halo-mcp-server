"""Halo MCP 附件管理工具"""

import asyncio
import mimetypes

from halo_mcp_server.config import settings

"""Attachment management tools for Halo MCP."""

import base64
import json
import os
from typing import Any, Dict, List, Optional, Union, Tuple

from loguru import logger
from mcp.types import Tool
import httpx

# 从 exceptions 导入所有需要的错误类型
from halo_mcp_server.exceptions import (
    AuthenticationError,
    AuthorizationError,
    HaloMCPError,
    NetworkError,
    ResourceNotFoundError,
)

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
    client: Optional[HaloClient] = None,  # 仍然接收 client 以获取 base_url 和认证信息
) -> Dict[str, Any]:
    """
    上传本地文件作为附件（参考 Console API 多表单上传）。
    使用独立的 httpx.AsyncClient 并包含完整的状态校验。

    Args:
        file_path: 本地文件路径
        policy_name: 存储策略名称，默认为 "default-policy"
        group_name: 附件分组名称（允许传空字符串）
        client: Halo API 客户端实例 (用于获取配置和认证)

    Returns:
        上传后的附件信息 (JSON 字典)

    Raises:
        HaloMCPError: 文件不存在或上传失败 (包装了底层错误)
        AuthenticationError / AuthorizationError / ResourceNotFoundError / NetworkError: API 调用特定错误
    """
    if not os.path.exists(file_path):
        logger.error(f"Upload attachment failed: File not found at {file_path}")
        raise HaloMCPError(f"File not found: {file_path}")

    _client_instance = client or HaloClient()  # 获取或创建 client 实例
    try:
        await _client_instance.ensure_authenticated()  # 确保已认证
    except Exception as auth_err:
        logger.error(f"Authentication failed before upload: {auth_err}")
        # 如果认证失败，直接抛出认证错误
        if isinstance(auth_err, AuthenticationError):
            raise
        raise HaloMCPError(f"Authentication failed: {auth_err}") from auth_err

    # 读取文件内容
    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
    except Exception as read_err:
        logger.error(f"Failed to read file content from {file_path}: {read_err}")
        raise HaloMCPError(f"无法读取文件: {file_path}, 原因: {read_err}") from read_err

    filename = os.path.basename(file_path)

    # 猜测 MIME 类型
    mimetype, _ = mimetypes.guess_type(file_path)
    mimetype = mimetype or "application/octet-stream"

    # 准备 files_data 字典
    files_data: Dict[
        str, Union[Tuple[Optional[str], Any], Tuple[Optional[str], Any, Optional[str]]]
    ] = {
        "file": (filename, file_content, mimetype),
        "policyName": (None, policy_name or "default-policy"),
        "groupName": (None, group_name if group_name is not None else ""),
    }

    # 准备 headers (仅包含认证)
    auth_token = _client_instance._headers.get("Authorization")  # 从内部获取认证头
    if not auth_token:
        # 理论上 ensure_authenticated 会处理，但作为保险
        raise AuthenticationError("无法获取认证令牌，请重新认证。")

    headers = {
        "Authorization": auth_token,
        # 不需要 Content-Type，httpx 会自动生成
    }

    # 构造完整 URL
    upload_path = "/apis/api.console.halo.run/v1alpha1/attachments/upload"
    url = f"{_client_instance.base_url}{upload_path}"

    logger.debug(f"Attempting direct httpx POST to {url} for file {filename}")
    logger.debug(f"Headers (excluding auto Content-Type): {headers}")

    # 使用独立的 httpx 客户端进行请求，并加入重试逻辑
    retry_count = 0
    # 从 settings 获取重试配置，如果 client 未初始化 settings，则使用默认值
    max_retries = getattr(settings, "max_retries", 3)
    retry_delay = getattr(settings, "retry_delay", 1.0)

    async with httpx.AsyncClient(timeout=_client_instance.timeout) as http_client:
        while retry_count <= max_retries:
            try:
                response = await http_client.post(
                    url,
                    files=files_data,
                    headers=headers,
                    follow_redirects=True,  # 保持与 BaseHTTPClient 一致
                )

                # --- 状态码校验 ---
                if 200 <= response.status_code < 300:
                    # 成功
                    logger.info(
                        f"Successfully uploaded {filename} via Console API (status: {response.status_code})"
                    )
                    try:
                        return response.json()
                    except json.JSONDecodeError as json_err:
                        logger.warning(
                            f"Failed to decode JSON response from successful upload: {json_err}. Response text: {response.text[:200]}"
                        )
                        # 即使 JSON 解析失败，也认为上传操作本身成功了，返回文本内容
                        return {"status": "success_but_no_json", "text": response.text}
                    except Exception as parse_err:  # 捕获其他可能的解析错误
                        logger.error(f"Unexpected error parsing response: {parse_err}")
                        raise HaloMCPError(f"上传成功但解析响应失败: {parse_err}") from parse_err

                elif response.status_code == 401:
                    logger.error(f"Authentication failed (401) during upload to {url}")
                    raise AuthenticationError("认证失败。请检查令牌或凭据。")
                elif response.status_code == 403:
                    logger.error(f"Authorization failed (403) during upload to {url}")
                    raise AuthorizationError("权限不足。访问受限。")
                elif response.status_code == 404:
                    logger.error(f"Resource not found (404) during upload: {url}")
                    raise ResourceNotFoundError("上传接口", upload_path)  # 使用 path
                elif response.status_code >= 400:  # 其他客户端或服务器错误
                    error_detail = response.text
                    try:
                        error_json = response.json()
                        error_detail = (
                            error_json.get("detail") or error_json.get("message") or error_detail
                        )
                    except Exception:
                        pass
                    logger.error(
                        f"HTTP {response.status_code} error during upload to {url}: {error_detail}"
                    )
                    # 对于可重试的服务器错误 (5xx)，允许重试；客户端错误 (4xx，非 401/403/404) 不重试
                    if response.status_code >= 500 and retry_count < max_retries:
                        last_error = NetworkError(
                            f"HTTP {response.status_code} 错误：{error_detail}",
                            status_code=response.status_code,
                        )
                        # 进入重试逻辑
                    else:
                        raise NetworkError(
                            f"HTTP {response.status_code} 错误：{error_detail}",
                            status_code=response.status_code,
                        )
                else:
                    # 未知状态码？理论上不应发生
                    logger.warning(
                        f"Unexpected status code {response.status_code} during upload to {url}"
                    )
                    last_error = NetworkError(
                        f"未预期的状态码: {response.status_code}", status_code=response.status_code
                    )
                    # 进入重试逻辑

            except (httpx.TimeoutException, httpx.ConnectError, httpx.NetworkError) as e:
                last_error = e
                logger.warning(f"Upload attempt {retry_count + 1} failed due to network issue: {e}")
                # 进入重试逻辑

            except (AuthenticationError, AuthorizationError, ResourceNotFoundError, NetworkError):
                raise  # 这些是明确的错误，不需要重试，直接抛出

            except Exception as e:
                # 捕获 httpx.post 可能抛出的其他异常
                last_error = e
                logger.error(f"Unexpected error during httpx.post for upload: {e}", exc_info=True)
                # 进入重试逻辑

            # 重试逻辑
            retry_count += 1
            if retry_count <= max_retries:
                logger.warning(
                    f"Retrying upload ({retry_count}/{max_retries})... Last error: {last_error}"
                )
                await asyncio.sleep(retry_delay * (2 ** (retry_count - 1)))  # 指数退避
            else:
                logger.error(
                    f"Upload failed after {max_retries} retries for {url}. Last error: {last_error}"
                )
                # 将最后一次的错误包装成 HaloMCPError 抛出
                error_message = f"上传附件失败 (重试次数耗尽): {last_error}"
                if isinstance(last_error, NetworkError):  # 如果最后是网络错误，保留状态码
                    raise HaloMCPError(
                        error_message, details={"status_code": last_error.status_code}
                    ) from last_error
                raise HaloMCPError(error_message) from last_error

    # 如果所有重试都失败，上面的循环会抛出异常
    # 理论上不会执行到这里
    raise HaloMCPError(f"上传附件 {filename} 失败，未知原因。")


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
        description="搜索和列出附件，支持分页、关键词搜索和文件类型过滤。推荐用法：附件库检索；可用 `accepts`（如 `image/*`）与分组过滤。",
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
        description="获取指定附件的详细信息。推荐用法：查看附件元数据与可用链接。",
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
        description="上传本地文件作为附件。推荐用法：通过本地路径上传；若未指定策略，默认 `default-policy`。",
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
        description="从 URL 上传附件。推荐用法：直接拉取远端文件到附件库；支持分组与策略选择。",
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
        description="删除附件。推荐用法：删除不再需要的附件；注意可能存在引用关系。",
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
        description="列出附件分组。推荐用法：浏览分组并用于上传或检索时的分组过滤。",
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
        description="创建附件分组。推荐用法：新增分组提升管理有序性；仅需显示名称。",
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
        description="获取存储策略列表。推荐用法：查看可用存储策略；选择上传时的目标策略。",
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

"""带重试与错误处理的基础 HTTP 客户端"""

from typing import Any, Dict, Optional

import httpx
from loguru import logger

from halo_mcp_server.config import settings
from halo_mcp_server.exceptions import (
    AuthenticationError,
    AuthorizationError,
    NetworkError,
    ResourceNotFoundError,
)


class BaseHTTPClient:
    """通用功能的基础 HTTP 客户端"""

    def __init__(self, base_url: str, timeout: int = 30):
        """
        初始化 HTTP 客户端。

        参数:
            base_url: API 基础地址
            timeout: 请求超时时间（秒）
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
        self._headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def __aenter__(self):
        """异步上下文管理器入口。"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出。"""
        await self.close()

    async def connect(self) -> None:
        """创建 HTTP 客户端连接。"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout,
                limits=httpx.Limits(
                    max_connections=settings.http_pool_size,
                    max_keepalive_connections=settings.http_pool_size // 2,
                ),
                headers=self._headers,
                follow_redirects=True,
            )
            logger.debug(f"HTTP 客户端已连接：{self.base_url}")

    async def close(self) -> None:
        """关闭 HTTP 客户端连接。"""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
            logger.debug("HTTP 客户端已关闭")

    def set_auth_token(self, token: str) -> None:
        """
        设置认证令牌。

        参数:
            token: Bearer 令牌
        """
        self._headers["Authorization"] = f"Bearer {token}"
        if self._client:
            self._client.headers.update({"Authorization": f"Bearer {token}"})
        logger.debug("认证令牌已设置")

    def remove_auth_token(self) -> None:
        """移除认证令牌。"""
        self._headers.pop("Authorization", None)
        if self._client:
            self._client.headers.pop("Authorization", None)
        logger.debug("认证令牌已移除")

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        发起带重试逻辑的 HTTP 请求。

        参数:
            method: HTTP 方法
            path: 请求路径
            params: 查询参数
            json: JSON 请求体
            data: 表单数据
            files: 上传文件
            headers: 额外请求头

        返回:
            响应 JSON

        异常:
            AuthenticationError：认证失败
            ResourceNotFoundError：资源未找到
            NetworkError：网络/HTTP 错误
        """
        if not self._client:
            await self.connect()

        url = path if path.startswith("http") else f"{self.base_url}{path}"
        request_headers = {**self._headers, **(headers or {})}

        # Remove Content-Type for multipart/form-data (httpx will set it)
        if files:
            request_headers.pop("Content-Type", None)

        retry_count = 0
        last_error = None

        while retry_count <= settings.max_retries:
            try:
                logger.debug(f"API 请求：{method} {url}")

                response = await self._client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    data=data,
                    files=files,
                    headers=request_headers,
                )

                # Handle error status codes
                if response.status_code == 401:
                    logger.error("认证失败（401）")
                    raise AuthenticationError("认证失败。请检查令牌或凭据。")

                if response.status_code == 403:
                    logger.error("权限不足（403）")
                    raise AuthorizationError("权限不足。访问受限。")

                if response.status_code == 404:
                    logger.error(f"资源未找到（404）：{url}")
                    raise ResourceNotFoundError("资源", path)

                if response.status_code >= 500:
                    error_detail = response.text
                    try:
                        error_json = response.json()
                        error_detail = (
                            error_json.get("detail") or error_json.get("message") or error_detail
                        )
                    except Exception:
                        pass

                    logger.error(f"HTTP {response.status_code} 错误：{error_detail}")
                    raise NetworkError(
                        f"HTTP {response.status_code} 错误：{error_detail}",
                        status_code=response.status_code,
                    )

                if response.status_code >= 400:
                    error_detail = response.text
                    try:
                        error_json = response.json()
                        error_detail = (
                            error_json.get("detail") or error_json.get("message") or error_detail
                        )
                    except Exception:
                        pass

                    logger.error(f"HTTP {response.status_code} 错误：{error_detail}")
                    raise NetworkError(
                        f"HTTP {response.status_code} 错误：{error_detail}",
                        status_code=response.status_code,
                    )

                # Parse response
                if response.status_code == 204:
                    return {}

                try:
                    result = response.json()
                    logger.debug(f"API 响应：{response.status_code}")
                    return result
                except Exception as e:
                    logger.warning(f"解析 JSON 响应失败：{e}")
                    return {"text": response.text}

            except (httpx.TimeoutException, httpx.ConnectError, httpx.NetworkError) as e:
                last_error = e
                retry_count += 1
                if retry_count <= settings.max_retries:
                    logger.warning(
                        f"请求失败，正在重试（{retry_count}/{settings.max_retries}）：{e}"
                    )
                    await self._wait_retry()
                else:
                    logger.error(f"请求在重试 {settings.max_retries} 次后仍失败：{e}")
                    raise NetworkError(f"网络错误：{e}")

            except (AuthenticationError, ResourceNotFoundError, NetworkError):
                raise

            except Exception as e:
                logger.error(f"请求过程中出现未预期错误：{e}", exc_info=True)
                raise NetworkError(f"未预期错误：{e}")

        raise NetworkError(f"请求在重试 {settings.max_retries} 次后仍失败：{last_error}")

    async def _wait_retry(self) -> None:
        """重试前等待。"""
        import asyncio

        await asyncio.sleep(settings.retry_delay)

    async def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """GET 请求。"""
        return await self._request("GET", path, params=params, headers=headers)

    async def post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """POST 请求。"""
        return await self._request(
            "POST", path, params=params, json=json, data=data, files=files, headers=headers
        )

    async def put(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """PUT 请求。"""
        return await self._request("PUT", path, params=params, json=json, headers=headers)

    async def patch(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """PATCH 请求。"""
        return await self._request("PATCH", path, params=params, json=json, headers=headers)

    async def delete(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """DELETE 请求。"""
        return await self._request("DELETE", path, params=params, headers=headers)

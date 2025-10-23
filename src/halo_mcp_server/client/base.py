"""Base HTTP client with retry and error handling."""

from typing import Any, Dict, Optional

import httpx
from loguru import logger

from halo_mcp_server.config import settings
from halo_mcp_server.exceptions import AuthenticationError, NetworkError, ResourceNotFoundError


class BaseHTTPClient:
    """Base HTTP client with common functionality."""

    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize HTTP client.

        Args:
            base_url: API base URL
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
        self._headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def connect(self) -> None:
        """Create HTTP client connection."""
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
            logger.debug(f"HTTP client connected to {self.base_url}")

    async def close(self) -> None:
        """Close HTTP client connection."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
            logger.debug("HTTP client closed")

    def set_auth_token(self, token: str) -> None:
        """
        Set authentication token.

        Args:
            token: Bearer token
        """
        self._headers["Authorization"] = f"Bearer {token}"
        if self._client:
            self._client.headers.update({"Authorization": f"Bearer {token}"})
        logger.debug("Auth token set")

    def remove_auth_token(self) -> None:
        """Remove authentication token."""
        self._headers.pop("Authorization", None)
        if self._client:
            self._client.headers.pop("Authorization", None)
        logger.debug("Auth token removed")

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
        Make HTTP request with retry logic.

        Args:
            method: HTTP method
            path: Request path
            params: Query parameters
            json: JSON body
            data: Form data
            files: Files to upload
            headers: Additional headers

        Returns:
            Response JSON

        Raises:
            AuthenticationError: Authentication failed
            ResourceNotFoundError: Resource not found
            NetworkError: Network/HTTP error
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
                logger.debug(f"API Request: {method} {url}")

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
                    logger.error("Authentication failed (401)")
                    raise AuthenticationError(
                        "Authentication failed. Please check your token or credentials."
                    )

                if response.status_code == 403:
                    logger.error("Permission denied (403)")
                    raise AuthenticationError("Permission denied. Insufficient privileges.")

                if response.status_code == 404:
                    logger.error(f"Resource not found (404): {url}")
                    raise ResourceNotFoundError("Resource", path)

                if response.status_code >= 400:
                    error_detail = response.text
                    try:
                        error_json = response.json()
                        error_detail = (
                            error_json.get("detail") or error_json.get("message") or error_detail
                        )
                    except Exception:
                        pass

                    logger.error(f"HTTP {response.status_code}: {error_detail}")
                    raise NetworkError(
                        f"HTTP {response.status_code}: {error_detail}",
                        status_code=response.status_code,
                    )

                # Parse response
                if response.status_code == 204:
                    return {}

                try:
                    result = response.json()
                    logger.debug(f"API Response: {response.status_code}")
                    return result
                except Exception as e:
                    logger.warning(f"Failed to parse JSON response: {e}")
                    return {"text": response.text}

            except (httpx.TimeoutException, httpx.ConnectError, httpx.NetworkError) as e:
                last_error = e
                retry_count += 1
                if retry_count <= settings.max_retries:
                    logger.warning(
                        f"Request failed, retrying ({retry_count}/{settings.max_retries}): {e}"
                    )
                    await self._wait_retry()
                else:
                    logger.error(f"Request failed after {settings.max_retries} retries: {e}")
                    raise NetworkError(f"Network error: {e}")

            except (AuthenticationError, ResourceNotFoundError, NetworkError):
                raise

            except Exception as e:
                logger.error(f"Unexpected error during request: {e}", exc_info=True)
                raise NetworkError(f"Unexpected error: {e}")

        raise NetworkError(f"Request failed after {settings.max_retries} retries: {last_error}")

    async def _wait_retry(self) -> None:
        """Wait before retry."""
        import asyncio

        await asyncio.sleep(settings.retry_delay)

    async def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """GET request."""
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
        """POST request."""
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
        """PUT request."""
        return await self._request("PUT", path, params=params, json=json, headers=headers)

    async def patch(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """PATCH request."""
        return await self._request("PATCH", path, params=params, json=json, headers=headers)

    async def delete(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """DELETE request."""
        return await self._request("DELETE", path, params=params, headers=headers)

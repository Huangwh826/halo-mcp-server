"""Halo API 客户端"""

from typing import Any, Dict, List, Optional

from loguru import logger

from halo_mcp_server.client.base import BaseHTTPClient
from halo_mcp_server.config import settings
from halo_mcp_server.exceptions import AuthenticationError, ConfigurationError


class HaloClient(BaseHTTPClient):
    """带认证的 Halo API 客户端"""

    def __init__(self):
        """初始化 Halo 客户端。"""
        super().__init__(
            base_url=settings.halo_base_url,
            timeout=settings.mcp_timeout,
        )
        self._authenticated = False

    async def authenticate(self) -> None:
        """
        与 Halo 服务器进行认证。

        异常:
            ConfigurationError：未配置认证方式
            AuthenticationError：认证失败
        """
        # Try token authentication first
        if settings.has_token_auth:
            token = settings.halo_token
            if token:  # Type guard to ensure token is not None
                self.set_auth_token(token)
                self._authenticated = True
                logger.info("使用令牌认证成功")
                return

        # Try password authentication
        if settings.has_password_auth:
            try:
                token = await self._login_with_password()
                self.set_auth_token(token)
                self._authenticated = True
                logger.info("使用用户名/密码认证成功")
                return
            except Exception as e:
                raise AuthenticationError(f"密码认证失败：{e}")

        raise ConfigurationError(
            "未配置任何认证方式。请设置 HALO_TOKEN 或 HALO_USERNAME/HALO_PASSWORD"
        )

    async def _login_with_password(self) -> str:
        """
        使用用户名和密码登录。

        返回:
            访问令牌

        异常:
            AuthenticationError：登录失败
        """
        try:
            response = await self.post(
                "/apis/api.console.halo.run/v1alpha1/auth/login",
                json={
                    "username": settings.halo_username,
                    "password": settings.halo_password,
                },
            )
            token = response.get("access_token")
            if not token:
                raise AuthenticationError("响应中未找到访问令牌")
            return token
        except Exception as e:
            logger.error(f"登录失败：{e}")
            raise

    async def ensure_authenticated(self) -> None:
        """确保客户端已通过认证。"""
        if not self._authenticated:
            await self.authenticate()

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
            self.set_auth_token(settings.halo_token)
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

    # ========== Post API ==========

    async def list_my_posts(
        self,
        page: int = 0,
        size: int = 20,
        publish_phase: Optional[str] = None,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
    ) -> Dict[str, Any]:
        """列出当前用户的文章。"""
        await self.ensure_authenticated()

        params = {"page": page, "size": size}
        if publish_phase:
            params["publishPhase"] = publish_phase
        if keyword:
            params["keyword"] = keyword
        if category:
            params["categoryWithChildren"] = category

        return await self.get("/apis/uc.api.content.halo.run/v1alpha1/posts", params=params)

    async def get_post(self, name: str) -> Dict[str, Any]:
        """按名称获取文章。"""
        await self.ensure_authenticated()
        return await self.get(f"/apis/uc.api.content.halo.run/v1alpha1/posts/{name}")

    async def create_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建一篇新文章。
        """
        await self.ensure_authenticated()
        return await self.post("/apis/api.console.halo.run/v1alpha1/posts", json=post_data)

    async def update_post(self, name: str, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新文章。"""
        await self.ensure_authenticated()
        return await self.put(
            f"/apis/uc.api.content.halo.run/v1alpha1/posts/{name}", json=post_data
        )

    async def publish_post(self, name: str) -> Dict[str, Any]:
        """发布文章。
        """
        await self.ensure_authenticated()
        return await self.put(
            f"/apis/api.console.halo.run/v1alpha1/posts/{name}/publish", params={"async": "true"}
        )

    async def unpublish_post(self, name: str) -> Dict[str, Any]:
        """取消发布文章。"""
        await self.ensure_authenticated()
        return await self.put(f"/apis/uc.api.content.halo.run/v1alpha1/posts/{name}/unpublish")

    async def delete_post(self, name: str) -> Dict[str, Any]:
        """删除文章（移至回收站）。"""
        await self.ensure_authenticated()
        return await self.delete(f"/apis/uc.api.content.halo.run/v1alpha1/posts/{name}/recycle")

    async def get_post_draft(self, name: str, patched: bool = False) -> Dict[str, Any]:
        """获取文章草稿。"""
        await self.ensure_authenticated()
        params = {"patched": str(patched).lower()}
        return await self.get(
            f"/apis/uc.api.content.halo.run/v1alpha1/posts/{name}/draft", params=params
        )

    async def update_post_draft(self, name: str, snapshot_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新文章草稿。"""
        await self.ensure_authenticated()
        return await self.put(
            f"/apis/uc.api.content.halo.run/v1alpha1/posts/{name}/draft",
            json=snapshot_data,
        )

    # ========== Category API = ==========

    async def list_categories(self, page: int = 0, size: int = 50) -> Dict[str, Any]:
        """列出分类。"""
        params = {"page": page, "size": size}
        return await self.get("/apis/api.content.halo.run/v1alpha1/categories", params=params)

    # ========== Tag API = ==========

    async def list_tags(self, page: int = 0, size: int = 100) -> Dict[str, Any]:
        """列出标签。"""
        params = {"page": page, "size": size}
        return await self.get("/apis/api.content.halo.run/v1alpha1/tags", params=params)

    # ========== Attachment API = ==========

    async def list_attachments(
        self,
        page: int = 0,
        size: int = 20,
        keyword: Optional[str] = None,
        accepts: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """列出附件。"""
        await self.ensure_authenticated()

        params = {"page": page, "size": size}
        if keyword:
            params["keyword"] = keyword
        if accepts:
            params["accepts"] = accepts

        return await self.get("/apis/api.console.halo.run/v1alpha1/attachments", params=params)

    async def upload_attachment(
        self,
        file_data: bytes,
        filename: str,
        group: Optional[str] = None,
    ) -> Dict[str, Any]:
        """上传附件。"""
        await self.ensure_authenticated()

        files = {"file": (filename, file_data)}
        data = {}
        if group:
            data["group"] = group

        return await self.post(
            "/apis/api.console.halo.run/v1alpha1/attachments/upload",
            files=files,
            data=data,
        )

    async def upload_from_url(self, url: str, group: Optional[str] = None) -> Dict[str, Any]:
        """从 URL 上传附件。"""
        await self.ensure_authenticated()

        json_data = {"url": url}
        if group:
            json_data["group"] = group

        return await self.post(
            "/apis/api.console.halo.run/v1alpha1/attachments/-/upload-from-url",
            json=json_data,
        )

    # ========== Search API = ==========

    async def search_posts(self, keyword: str, limit: int = 10) -> Dict[str, Any]:
        """搜索文章。"""
        json_data = {"keyword": keyword, "limit": limit}
        return await self.post("/apis/api.halo.run/v1alpha1/indices/-/search", json=json_data)

    # ========== Comment API = ==========

    async def list_comments(
        self,
        page: int = 0,
        size: int = 20,
        keyword: Optional[str] = None,
    ) -> Dict[str, Any]:
        """列出评论。"""
        await self.ensure_authenticated()

        params = {"page": page, "size": size}
        if keyword:
            params["keyword"] = keyword

        return await self.get("/apis/api.console.halo.run/v1alpha1/comments", params=params)

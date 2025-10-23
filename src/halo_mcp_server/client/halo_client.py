"""Halo API client."""

from typing import Any, Dict, List, Optional

from loguru import logger

from halo_mcp_server.client.base import BaseHTTPClient
from halo_mcp_server.config import settings
from halo_mcp_server.exceptions import AuthenticationError, ConfigurationError


class HaloClient(BaseHTTPClient):
    """Halo API client with authentication."""

    def __init__(self):
        """Initialize Halo client."""
        super().__init__(
            base_url=settings.halo_base_url,
            timeout=settings.mcp_timeout,
        )
        self._authenticated = False

    async def authenticate(self) -> None:
        """
        Authenticate with Halo server.

        Raises:
            ConfigurationError: No auth method configured
            AuthenticationError: Authentication failed
        """
        # Try token authentication first
        if settings.has_token_auth:
            self.set_auth_token(settings.halo_token)
            self._authenticated = True
            logger.info("Authenticated with token")
            return

        # Try password authentication
        if settings.has_password_auth:
            try:
                token = await self._login_with_password()
                self.set_auth_token(token)
                self._authenticated = True
                logger.info("Authenticated with username/password")
                return
            except Exception as e:
                raise AuthenticationError(f"Password authentication failed: {e}")

        raise ConfigurationError(
            "No authentication method configured. "
            "Please set HALO_TOKEN or HALO_USERNAME/HALO_PASSWORD"
        )

    async def _login_with_password(self) -> str:
        """
        Login with username and password.

        Returns:
            Access token

        Raises:
            AuthenticationError: Login failed
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
                raise AuthenticationError("No access token in response")
            return token
        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise

    async def ensure_authenticated(self) -> None:
        """Ensure client is authenticated."""
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
        """List current user's posts."""
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
        """Get post by name."""
        await self.ensure_authenticated()
        return await self.get(f"/apis/uc.api.content.halo.run/v1alpha1/posts/{name}")

    async def create_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new post.

        Note: Java version uses /apis/api.console.halo.run/v1alpha1/posts
        with a specific request structure: {post: {...}, content: {...}}
        """
        await self.ensure_authenticated()
        # Use console API endpoint like Java version
        return await self.post("/apis/api.console.halo.run/v1alpha1/posts", json=post_data)

    async def update_post(self, name: str, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a post."""
        await self.ensure_authenticated()
        return await self.put(
            f"/apis/uc.api.content.halo.run/v1alpha1/posts/{name}", json=post_data
        )

    async def publish_post(self, name: str) -> Dict[str, Any]:
        """Publish a post.

        Note: Java version uses /apis/api.console.halo.run/v1alpha1/posts/{name}/publish
        with async=true query parameter
        """
        await self.ensure_authenticated()
        return await self.put(
            f"/apis/api.console.halo.run/v1alpha1/posts/{name}/publish", params={"async": "true"}
        )

    async def unpublish_post(self, name: str) -> Dict[str, Any]:
        """Unpublish a post."""
        await self.ensure_authenticated()
        return await self.put(f"/apis/uc.api.content.halo.run/v1alpha1/posts/{name}/unpublish")

    async def delete_post(self, name: str) -> Dict[str, Any]:
        """Delete a post (move to recycle bin)."""
        await self.ensure_authenticated()
        return await self.delete(f"/apis/uc.api.content.halo.run/v1alpha1/posts/{name}/recycle")

    async def get_post_draft(self, name: str, patched: bool = False) -> Dict[str, Any]:
        """Get post draft."""
        await self.ensure_authenticated()
        params = {"patched": str(patched).lower()}
        return await self.get(
            f"/apis/uc.api.content.halo.run/v1alpha1/posts/{name}/draft", params=params
        )

    async def update_post_draft(self, name: str, snapshot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update post draft."""
        await self.ensure_authenticated()
        return await self.put(
            f"/apis/uc.api.content.halo.run/v1alpha1/posts/{name}/draft",
            json=snapshot_data,
        )

    # ========== Category API ==========

    async def list_categories(self, page: int = 0, size: int = 50) -> Dict[str, Any]:
        """List categories."""
        params = {"page": page, "size": size}
        return await self.get("/apis/api.content.halo.run/v1alpha1/categories", params=params)

    # ========== Tag API ==========

    async def list_tags(self, page: int = 0, size: int = 100) -> Dict[str, Any]:
        """List tags."""
        params = {"page": page, "size": size}
        return await self.get("/apis/api.content.halo.run/v1alpha1/tags", params=params)

    # ========== Attachment API ==========

    async def list_attachments(
        self,
        page: int = 0,
        size: int = 20,
        keyword: Optional[str] = None,
        accepts: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """List attachments."""
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
        """Upload attachment."""
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
        """Upload attachment from URL."""
        await self.ensure_authenticated()

        json_data = {"url": url}
        if group:
            json_data["group"] = group

        return await self.post(
            "/apis/api.console.halo.run/v1alpha1/attachments/-/upload-from-url",
            json=json_data,
        )

    # ========== Search API ==========

    async def search_posts(self, keyword: str, limit: int = 10) -> Dict[str, Any]:
        """Search posts."""
        json_data = {"keyword": keyword, "limit": limit}
        return await self.post("/apis/api.halo.run/v1alpha1/indices/-/search", json=json_data)

    # ========== Comment API ==========

    async def list_comments(
        self,
        page: int = 0,
        size: int = 20,
        keyword: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List comments."""
        await self.ensure_authenticated()

        params = {"page": page, "size": size}
        if keyword:
            params["keyword"] = keyword

        return await self.get("/apis/api.console.halo.run/v1alpha1/comments", params=params)

"""Configuration management for Halo MCP Server."""

from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        # 环境变量优先级高于 .env 文件
        # 这样 Claude Desktop 配置的环境变量会覆盖 .env 文件
        env_prefix="",
    )

    # ========== Halo Server Configuration ==========
    halo_base_url: str = Field(
        default="http://localhost:8091",
        description="Halo server base URL",
    )

    halo_token: Optional[str] = Field(
        default=None,
        description="Halo API bearer token (recommended)",
    )

    halo_username: Optional[str] = Field(
        default=None,
        description="Halo username for password authentication",
    )

    halo_password: Optional[str] = Field(
        default=None,
        description="Halo password for password authentication",
    )

    # ========== MCP Service Configuration ==========
    mcp_server_name: str = Field(
        default="halo-mcp-server",
        description="MCP server name",
    )

    mcp_log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)",
    )

    mcp_timeout: int = Field(
        default=30,
        ge=1,
        le=300,
        description="HTTP request timeout in seconds",
    )

    # ========== Feature Switches ==========
    enable_draft_auto_save: bool = Field(
        default=True,
        description="Enable automatic draft saving",
    )

    enable_image_compression: bool = Field(
        default=True,
        description="Enable automatic image compression",
    )

    image_max_width: int = Field(
        default=1920,
        ge=100,
        le=4096,
        description="Maximum image width in pixels after compression",
    )

    image_quality: int = Field(
        default=85,
        ge=1,
        le=100,
        description="Image quality for compression (1-100)",
    )

    max_upload_size_mb: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum upload file size in MB",
    )

    # ========== Advanced Configuration ==========
    http_pool_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="HTTP connection pool size",
    )

    max_retries: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Maximum number of request retries",
    )

    retry_delay: float = Field(
        default=1.0,
        ge=0.1,
        le=10.0,
        description="Delay between retries in seconds",
    )

    enable_cache: bool = Field(
        default=True,
        description="Enable request caching",
    )

    cache_ttl: int = Field(
        default=300,
        ge=0,
        le=3600,
        description="Cache TTL in seconds",
    )

    @field_validator("halo_base_url")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        """Validate and normalize base URL."""
        # 允许空值，在实际使用时再验证
        if v:
            return v.rstrip("/")
        return v

    @field_validator("mcp_log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Invalid log level. Must be one of {valid_levels}")
        return v_upper

    @property
    def has_token_auth(self) -> bool:
        """Check if token authentication is configured."""
        return bool(self.halo_token)

    @property
    def has_password_auth(self) -> bool:
        """Check if password authentication is configured."""
        return bool(self.halo_username and self.halo_password)

    @property
    def has_valid_auth(self) -> bool:
        """Check if any valid authentication method is configured."""
        return self.has_token_auth or self.has_password_auth

    def __repr__(self) -> str:
        """Safe repr that doesn't expose sensitive data."""
        return (
            f"Settings(halo_base_url='{self.halo_base_url}', "
            f"has_token={'Yes' if self.has_token_auth else 'No'}, "
            f"has_password={'Yes' if self.has_password_auth else 'No'}, "
            f"log_level='{self.mcp_log_level}')"
        )


# Global settings instance
settings = Settings()

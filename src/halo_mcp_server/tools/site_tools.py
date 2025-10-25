"""Site-level tools for Halo MCP Server."""

import os
from typing import Any, Dict

from loguru import logger
from mcp.types import Tool

from halo_mcp_server.client import HaloClient
from halo_mcp_server.config import settings
from halo_mcp_server.models.common import ToolResult


async def get_halo_base_url_tool(client: HaloClient, args: Dict[str, Any]) -> str:
    """Return the current Halo site's base URL sourced from HALO_BASE_URL.

    This reads the environment variable `HALO_BASE_URL` if present and reports the
    resolved value used by the server (normalized, trailing slashes stripped). If the
    environment is not set, the server's default from settings is returned.
    """
    try:
        # No authentication is needed; we just report configuration
        env_value = os.environ.get("HALO_BASE_URL")
        base_url = settings.halo_base_url  # already normalized via validator
        source = "env" if env_value else "default"

        data = {
            "base_url": base_url,
            "source": source,
            "source_env_var": "HALO_BASE_URL",
            "env_value": env_value,
        }

        logger.debug(f"HALO_BASE_URL resolved: {data}")
        result = ToolResult.success_result("已获取 Halo 站点链接地址", data)
        return result.model_dump_json()

    except Exception as e:
        logger.error(f"获取 Halo 站点链接地址失败: {e}", exc_info=True)
        result = ToolResult.error_result(f"获取站点链接地址失败：{str(e)}")
        return result.model_dump_json()


# MCP Tool definitions
SITE_TOOLS = [
    Tool(
        name="get_halo_base_url",
        description="获取当前 Halo 站点的基础链接地址（来源：环境变量 HALO_BASE_URL）",
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
]

"""Pytest 配置文件

提供测试 fixtures 和全局配置。
"""

import pytest


@pytest.fixture
async def halo_client():
    """创建测试用 Halo 客户端"""
    from halo_mcp_server.client.halo_client import HaloClient
    
    client = HaloClient()
    await client.connect()
    await client.authenticate()
    yield client
    await client.close()


@pytest.fixture
def mock_settings():
    """Mock 配置用于单元测试"""
    from halo_mcp_server.config import Settings

    return Settings(
        halo_base_url="http://localhost:8091",
        halo_token="test_token",
        mcp_server_name="test-server",
        mcp_log_level="DEBUG",
    )

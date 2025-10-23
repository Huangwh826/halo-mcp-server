"""Test configuration."""

import pytest


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    from halo_mcp_server.config import Settings

    return Settings(
        halo_base_url="http://localhost:8091",
        halo_token="test_token",
        mcp_server_name="test-server",
        mcp_log_level="DEBUG",
    )

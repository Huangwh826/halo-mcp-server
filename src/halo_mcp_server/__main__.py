"""Entry point for running Halo MCP Server as a module."""

import asyncio
import sys

from loguru import logger

from halo_mcp_server.server import run_server


def main() -> None:
    """Main entry point for the MCP server."""
    try:
        logger.info("Starting Halo MCP Server...")
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

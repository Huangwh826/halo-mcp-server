import asyncio
import sys
import os
sys.path.insert(0, '../src')

from halo_mcp_server.tools.attachment_tools import upload_attachment_tool
from halo_mcp_server.client.halo_client import HaloClient

async def main():
    try:
        client = HaloClient()
        args = {
            'file_path': r'C:\Users\sa\Pictures\微信图片_2025-10-18_164046_028.jpg',
            'policy_name': 'default-policy'
        }
        result = await upload_attachment_tool(client, args)
        print('上传结果:', result)
    except Exception as e:
        print('上传失败:', str(e))

if __name__ == "__main__":
    asyncio.run(main())
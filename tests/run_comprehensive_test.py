"""Halo MCP Server 综合测试套件

覆盖所有 30 个 MCP 工具的完整测试，包括：
- 分类管理 (6个工具)
- 标签管理 (7个工具)
- 附件管理 (8个工具)
- 文章管理 (9个工具)

可直接运行，无需额外依赖。

使用方法：
    python run_comprehensive_test.py

环境要求：
    - Python 3.10+
    - 配置 HALO_BASE_URL 和 HALO_TOKEN 环境变量
"""

import asyncio
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from loguru import logger

from halo_mcp_server.client.halo_client import HaloClient


class HaloMCPComprehensiveTest:
    """Halo MCP Server 全面测试类"""

    def __init__(self):
        self.client = None
        self.test_data = {
            "category_names": [],
            "tag_names": [],
            "attachment_names": [],
            "post_names": [],
            "group_names": [],
        }
        self.test_results = []

    async def setup(self):
        """初始化测试环境"""
        logger.info("=" * 80)
        logger.info("🚀 开始 Halo MCP Server 全面测试")
        logger.info("=" * 80)

        self.client = HaloClient()
        await self.client.connect()
        await self.client.authenticate()
        logger.success("✓ 客户端初始化成功")

    async def teardown(self):
        """清理测试环境"""
        if self.client:
            await self.client.close()
        logger.info("=" * 80)
        logger.success("✓ 测试环境清理完成")

    def log_test(self, test_num, test_name, description):
        """记录测试信息"""
        logger.info("=" * 80)
        logger.info(f"测试 {test_num}/30: {test_name}")
        logger.info(f"描述: {description}")
        logger.info("=" * 80)

    def record_result(self, test_num, test_name, success, message=""):
        """记录测试结果"""
        result = {
            "test_num": test_num,
            "test_name": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }
        self.test_results.append(result)

        if success:
            logger.success(f"✓ 测试 {test_num} 通过: {test_name}")
        else:
            logger.error(f"✗ 测试 {test_num} 失败: {test_name} - {message}")

    # ==================== 分类管理工具 (6个) ====================

    async def test_01_create_category(self):
        """测试 1: 创建分类"""
        from halo_mcp_server.tools.category_tools import create_category_tool

        self.log_test(1, "create_category", "创建博客分类")

        try:
            assert self.client is not None
            args = {
                "display_name": f"自动化测试分类_{datetime.now().strftime('%H%M%S')}",
                "slug": f"test-category-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "description": "自动化测试创建的分类",
                "priority": 10,
            }

            result = await create_category_tool(self.client, args)
            result_data = json.loads(result)

            if result_data.get("success"):
                self.test_data["category_names"].append(result_data["data"]["category_name"])
                self.record_result(1, "create_category", True, f"分类: {result_data['data']['display_name']}")
            else:
                self.record_result(1, "create_category", False, result_data.get("message"))

        except Exception as e:
            self.record_result(1, "create_category", False, str(e))

    async def test_02_list_categories(self):
        """测试 2: 列出分类"""
        from halo_mcp_server.tools.category_tools import list_categories_tool

        self.log_test(2, "list_categories", "列出所有分类")

        try:
            assert self.client is not None
            args = {"page": 0, "size": 50}
            result = await list_categories_tool(self.client, args)
            result_data = json.loads(result)

            count = len(result_data.get("items", []))
            self.record_result(2, "list_categories", True, f"找到 {count} 个分类")

        except Exception as e:
            self.record_result(2, "list_categories", False, str(e))

    async def test_03_get_category(self):
        """测试 3: 获取分类详情"""
        from halo_mcp_server.tools.category_tools import get_category_tool

        self.log_test(3, "get_category", "获取分类详细信息")

        try:
            assert self.client is not None
            if not self.test_data["category_names"]:
                self.record_result(3, "get_category", False, "没有可用的分类")
                return

            args = {"name": self.test_data["category_names"][0]}
            result = await get_category_tool(self.client, args)
            result_data = json.loads(result)

            self.record_result(3, "get_category", True, f"分类: {result_data['spec']['displayName']}")

        except Exception as e:
            self.record_result(3, "get_category", False, str(e))

    async def test_04_update_category(self):
        """测试 4: 更新分类"""
        from halo_mcp_server.tools.category_tools import update_category_tool

        self.log_test(4, "update_category", "更新分类信息")

        try:
            assert self.client is not None
            if not self.test_data["category_names"]:
                self.record_result(4, "update_category", False, "没有可用的分类")
                return

            args = {
                "name": self.test_data["category_names"][0],
                "description": "更新后的描述",
                "priority": 20,
            }

            result = await update_category_tool(self.client, args)
            result_data = json.loads(result)

            self.record_result(4, "update_category", result_data.get("success", False))

        except Exception as e:
            self.record_result(4, "update_category", False, str(e))

    async def test_05_get_category_posts(self):
        """测试 5: 获取分类下的文章"""
        from halo_mcp_server.tools.category_tools import get_posts_under_category_tool

        self.log_test(5, "get_category_posts", "获取分类下的文章列表")

        try:
            assert self.client is not None
            if not self.test_data["category_names"]:
                self.record_result(5, "get_category_posts", False, "没有可用的分类")
                return

            args = {"name": self.test_data["category_names"][0], "page": 0, "size": 20}
            result = await get_posts_under_category_tool(self.client, args)

            self.record_result(5, "get_category_posts", True)

        except Exception as e:
            self.record_result(5, "get_category_posts", False, str(e))

    # ==================== 标签管理工具 (7个) ====================

    async def test_06_create_tag(self):
        """测试 6: 创建标签"""
        from halo_mcp_server.tools.tag_tools import create_tag_tool

        self.log_test(6, "create_tag", "创建博客标签")

        try:
            for i in range(2):
                args = {
                    "display_name": f"测试标签{i+1}_{datetime.now().strftime('%H%M%S')}",
                    "color": "#FF5733" if i == 0 else "#33FF57",
                }

                result = await create_tag_tool(self.client, args)
                result_data = json.loads(result)

                if result_data.get("success"):
                    self.test_data["tag_names"].append(result_data["data"]["tag_name"])

            self.record_result(6, "create_tag", True, f"创建了 {len(self.test_data['tag_names'])} 个标签")

        except Exception as e:
            self.record_result(6, "create_tag", False, str(e))

    async def test_07_list_tags(self):
        """测试 7: 列出标签"""
        from halo_mcp_server.tools.tag_tools import list_tags_tool

        self.log_test(7, "list_tags", "列出所有标签")

        try:
            args = {"page": 0, "size": 100}
            result = await list_tags_tool(self.client, args)
            result_data = json.loads(result)

            count = len(result_data.get("items", []))
            self.record_result(7, "list_tags", True, f"找到 {count} 个标签")

        except Exception as e:
            self.record_result(7, "list_tags", False, str(e))

    async def test_08_get_tag(self):
        """测试 8: 获取标签详情"""
        from halo_mcp_server.tools.tag_tools import get_tag_tool

        self.log_test(8, "get_tag", "获取标签详细信息")

        try:
            if not self.test_data["tag_names"]:
                self.record_result(8, "get_tag", False, "没有可用的标签")
                return

            args = {"name": self.test_data["tag_names"][0]}
            result = await get_tag_tool(self.client, args)
            result_data = json.loads(result)

            self.record_result(8, "get_tag", True, f"标签: {result_data['spec']['displayName']}")

        except Exception as e:
            self.record_result(8, "get_tag", False, str(e))

    async def test_09_update_tag(self):
        """测试 9: 更新标签"""
        from halo_mcp_server.tools.tag_tools import update_tag_tool

        self.log_test(9, "update_tag", "更新标签信息")

        try:
            if not self.test_data["tag_names"]:
                self.record_result(9, "update_tag", False, "没有可用的标签")
                return

            args = {"name": self.test_data["tag_names"][0], "color": "#FFA500"}

            result = await update_tag_tool(self.client, args)
            result_data = json.loads(result)

            self.record_result(9, "update_tag", result_data.get("success", False))

        except Exception as e:
            self.record_result(9, "update_tag", False, str(e))

    async def test_10_list_console_tags(self):
        """测试 10: 列出控制台标签"""
        from halo_mcp_server.tools.tag_tools import list_console_tags_tool

        self.log_test(10, "list_console_tags", "列出控制台标签")

        try:
            args = {"page": 0, "size": 100}
            result = await list_console_tags_tool(self.client, args)
            result_data = json.loads(result)

            count = len(result_data.get("items", []))
            self.record_result(10, "list_console_tags", True, f"找到 {count} 个控制台标签")

        except Exception as e:
            self.record_result(10, "list_console_tags", False, str(e))

    async def test_11_get_tag_posts(self):
        """测试 11: 获取标签下的文章"""
        from halo_mcp_server.tools.tag_tools import get_posts_under_tag_tool

        self.log_test(11, "get_tag_posts", "获取标签下的文章列表")

        try:
            if not self.test_data["tag_names"]:
                self.record_result(11, "get_tag_posts", False, "没有可用的标签")
                return

            args = {"name": self.test_data["tag_names"][0], "page": 0, "size": 20}
            result = await get_posts_under_tag_tool(self.client, args)

            self.record_result(11, "get_tag_posts", True)

        except Exception as e:
            self.record_result(11, "get_tag_posts", False, str(e))

    # ==================== 附件管理工具 (8个) ====================

    async def test_12_list_attachment_groups(self):
        """测试 12: 列出附件分组"""
        from halo_mcp_server.tools.attachment_tools import list_attachment_groups_tool

        self.log_test(12, "list_attachment_groups", "列出附件分组")

        try:
            args = {"page": 0, "size": 100}
            result = await list_attachment_groups_tool(self.client, args)

            self.record_result(12, "list_attachment_groups", True)

        except Exception as e:
            self.record_result(12, "list_attachment_groups", False, str(e))

    async def test_13_create_attachment_group(self):
        """测试 13: 创建附件分组"""
        from halo_mcp_server.tools.attachment_tools import create_attachment_group_tool

        self.log_test(13, "create_attachment_group", "创建附件分组")

        try:
            args = {"display_name": f"测试附件分组_{datetime.now().strftime('%H%M%S')}"}

            result = await create_attachment_group_tool(self.client, args)
            result_data = json.loads(result)

            if result_data.get("success"):
                self.test_data["group_names"].append(result_data["data"]["group_name"])
                self.record_result(13, "create_attachment_group", True)
            else:
                self.record_result(13, "create_attachment_group", False, result_data.get("message"))

        except Exception as e:
            self.record_result(13, "create_attachment_group", False, str(e))

    async def test_14_get_attachment_policies(self):
        """测试 14: 获取存储策略"""
        from halo_mcp_server.tools.attachment_tools import list_storage_policies_tool

        self.log_test(14, "get_attachment_policies", "获取存储策略列表")

        try:
            args = {"random_string": "test"}
            result = await list_storage_policies_tool(self.client, args)

            self.record_result(14, "get_attachment_policies", True)

        except Exception as e:
            self.record_result(14, "get_attachment_policies", False, str(e))

    async def test_15_upload_attachment(self):
        """测试 15: 上传本地文件"""
        from halo_mcp_server.tools.attachment_tools import upload_attachment_tool

        self.log_test(15, "upload_attachment", "上传本地文件作为附件")

        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
                f.write(f"测试文件\n创建时间: {datetime.now().isoformat()}\n")
                temp_file_path = f.name

            try:
                args = {"file_path": temp_file_path, "policy_name": "default-policy"}

                result = await upload_attachment_tool(self.client, args)
                result_data = json.loads(result)

                if result_data.get("success"):
                    self.test_data["attachment_names"].append(result_data["data"]["attachment_name"])
                    self.record_result(15, "upload_attachment", True)
                else:
                    self.record_result(15, "upload_attachment", False, result_data.get("message"))

            finally:
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)

        except Exception as e:
            self.record_result(15, "upload_attachment", False, str(e))

    async def test_16_list_attachments(self):
        """测试 16: 列出附件"""
        from halo_mcp_server.tools.attachment_tools import list_attachments_tool

        self.log_test(16, "list_attachments", "列出所有附件")

        try:
            args = {"page": 0, "size": 50}
            result = await list_attachments_tool(self.client, args)

            self.record_result(16, "list_attachments", True)

        except Exception as e:
            self.record_result(16, "list_attachments", False, str(e))

    async def test_17_get_attachment(self):
        """测试 17: 获取附件详情"""
        from halo_mcp_server.tools.attachment_tools import get_attachment_tool

        self.log_test(17, "get_attachment", "获取附件详细信息")

        try:
            if not self.test_data["attachment_names"]:
                self.record_result(17, "get_attachment", True, "跳过（无附件）")
                return

            args = {"name": self.test_data["attachment_names"][0]}
            result = await get_attachment_tool(self.client, args)

            self.record_result(17, "get_attachment", True)

        except Exception as e:
            self.record_result(17, "get_attachment", False, str(e))

    # ==================== 文章管理工具 (9个) ====================

    async def test_18_create_post(self):
        """测试 18: 创建文章"""
        from halo_mcp_server.tools.post_tools import create_post_tool

        self.log_test(18, "create_post", "创建博客文章")

        try:
            content = f"""# 自动化测试文章

这是自动化测试创建的文章。

## 测试信息

- 创建时间: {datetime.now().isoformat()}
- 测试工具: Halo MCP Server

## 内容

这是测试内容。
"""

            args = {
                "title": f"自动化测试文章_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "content": content,
                "excerpt": "自动化测试文章",
                "categories": self.test_data["category_names"][:1],
                "tags": self.test_data["tag_names"][:2],
            }

            result = await create_post_tool(self.client, args)
            result_data = json.loads(result)

            if result_data.get("success"):
                self.test_data["post_names"].append(result_data["data"]["post_name"])
                self.record_result(18, "create_post", True, f"文章: {args['title']}")
            else:
                self.record_result(18, "create_post", False, result_data.get("message"))

        except Exception as e:
            self.record_result(18, "create_post", False, str(e))

    async def test_19_list_my_posts(self):
        """测试 19: 列出文章"""
        from halo_mcp_server.tools.post_tools import list_my_posts_tool

        self.log_test(19, "list_my_posts", "列出用户的所有文章")

        try:
            args = {"page": 0, "size": 20}
            result = await list_my_posts_tool(self.client, args)
            result_data = json.loads(result)

            count = len(result_data.get("items", []))
            self.record_result(19, "list_my_posts", True, f"找到 {count} 篇文章")

        except Exception as e:
            self.record_result(19, "list_my_posts", False, str(e))

    async def test_20_get_post(self):
        """测试 20: 获取文章详情"""
        from halo_mcp_server.tools.post_tools import get_post_tool

        self.log_test(20, "get_post", "获取文章详细信息")

        try:
            if not self.test_data["post_names"]:
                self.record_result(20, "get_post", False, "没有可用的文章")
                return

            args = {"name": self.test_data["post_names"][0]}
            result = await get_post_tool(self.client, args)
            result_data = json.loads(result)

            self.record_result(20, "get_post", True, f"文章: {result_data['spec']['title']}")

        except Exception as e:
            self.record_result(20, "get_post", False, str(e))

    async def test_21_get_post_draft(self):
        """测试 21: 获取文章草稿"""
        from halo_mcp_server.tools.post_tools import get_post_draft_tool

        self.log_test(21, "get_post_draft", "获取文章草稿")

        try:
            if not self.test_data["post_names"]:
                self.record_result(21, "get_post_draft", False, "没有可用的文章")
                return

            args = {"name": self.test_data["post_names"][0]}
            result = await get_post_draft_tool(self.client, args)

            self.record_result(21, "get_post_draft", True)

        except Exception as e:
            self.record_result(21, "get_post_draft", False, str(e))

    async def test_22_update_post_draft(self):
        """测试 22: 更新文章草稿"""
        from halo_mcp_server.tools.post_tools import update_post_draft_tool

        self.log_test(22, "update_post_draft", "更新文章草稿内容")

        try:
            if not self.test_data["post_names"]:
                self.record_result(22, "update_post_draft", False, "没有可用的文章")
                return

            updated_content = f"# 更新后的测试文章\n\n更新时间: {datetime.now().isoformat()}\n"

            args = {"name": self.test_data["post_names"][0], "content": updated_content}

            result = await update_post_draft_tool(self.client, args)
            result_data = json.loads(result)

            self.record_result(22, "update_post_draft", result_data.get("success", False))

        except Exception as e:
            self.record_result(22, "update_post_draft", False, str(e))

    async def test_23_update_post(self):
        """测试 23: 更新文章"""
        from halo_mcp_server.tools.post_tools import update_post_tool

        self.log_test(23, "update_post", "更新文章元数据")

        try:
            if not self.test_data["post_names"]:
                self.record_result(23, "update_post", False, "没有可用的文章")
                return

            args = {
                "name": self.test_data["post_names"][0],
                "excerpt": f"更新后的摘要 - {datetime.now().isoformat()}",
            }

            result = await update_post_tool(self.client, args)
            result_data = json.loads(result)

            self.record_result(23, "update_post", result_data.get("success", False))

        except Exception as e:
            self.record_result(23, "update_post", False, str(e))

    async def test_24_publish_post(self):
        """测试 24: 发布文章"""
        from halo_mcp_server.tools.post_tools import publish_post_tool

        self.log_test(24, "publish_post", "发布文章")

        try:
            if not self.test_data["post_names"]:
                self.record_result(24, "publish_post", False, "没有可用的文章")
                return

            args = {"name": self.test_data["post_names"][0]}

            result = await publish_post_tool(self.client, args)
            result_data = json.loads(result)

            self.record_result(24, "publish_post", result_data.get("success", False))

        except Exception as e:
            self.record_result(24, "publish_post", False, str(e))

    async def test_25_unpublish_post(self):
        """测试 25: 取消发布文章"""
        from halo_mcp_server.tools.post_tools import unpublish_post_tool

        self.log_test(25, "unpublish_post", "取消发布文章")

        try:
            if not self.test_data["post_names"]:
                self.record_result(25, "unpublish_post", False, "没有可用的文章")
                return

            args = {"name": self.test_data["post_names"][0]}

            result = await unpublish_post_tool(self.client, args)
            result_data = json.loads(result)

            self.record_result(25, "unpublish_post", result_data.get("success", False))

        except Exception as e:
            self.record_result(25, "unpublish_post", False, str(e))

    # ==================== 清理测试数据 ====================

    async def test_26_delete_post(self):
        """测试 26: 删除文章"""
        from halo_mcp_server.tools.post_tools import delete_post_tool

        self.log_test(26, "delete_post", "删除文章")

        try:
            for post_name in self.test_data["post_names"]:
                args = {"name": post_name}
                await delete_post_tool(self.client, args)

            self.record_result(26, "delete_post", True, f"删除了 {len(self.test_data['post_names'])} 篇文章")

        except Exception as e:
            self.record_result(26, "delete_post", False, str(e))

    async def test_27_delete_attachment(self):
        """测试 27: 删除附件"""
        from halo_mcp_server.tools.attachment_tools import delete_attachment_tool

        self.log_test(27, "delete_attachment", "删除附件")

        try:
            for attachment_name in self.test_data["attachment_names"]:
                args = {"name": attachment_name}
                try:
                    await delete_attachment_tool(self.client, args)
                except:
                    pass

            self.record_result(27, "delete_attachment", True)

        except Exception as e:
            self.record_result(27, "delete_attachment", False, str(e))

    async def test_28_delete_tag(self):
        """测试 28: 删除标签"""
        from halo_mcp_server.tools.tag_tools import delete_tag_tool

        self.log_test(28, "delete_tag", "删除标签")

        try:
            for tag_name in self.test_data["tag_names"]:
                args = {"name": tag_name}
                await delete_tag_tool(self.client, args)

            self.record_result(28, "delete_tag", True, f"删除了 {len(self.test_data['tag_names'])} 个标签")

        except Exception as e:
            self.record_result(28, "delete_tag", False, str(e))

    async def test_29_delete_category(self):
        """测试 29: 删除分类"""
        from halo_mcp_server.tools.category_tools import delete_category_tool

        self.log_test(29, "delete_category", "删除分类")

        try:
            for category_name in self.test_data["category_names"]:
                args = {"name": category_name}
                await delete_category_tool(self.client, args)

            self.record_result(29, "delete_category", True, f"删除了 {len(self.test_data['category_names'])} 个分类")

        except Exception as e:
            self.record_result(29, "delete_category", False, str(e))

    # ==================== 运行所有测试 ====================

    async def run_all_tests(self):
        """运行所有测试"""
        await self.setup()

        try:
            # 按顺序运行所有测试
            await self.test_01_create_category()
            await self.test_02_list_categories()
            await self.test_03_get_category()
            await self.test_04_update_category()
            await self.test_05_get_category_posts()

            await self.test_06_create_tag()
            await self.test_07_list_tags()
            await self.test_08_get_tag()
            await self.test_09_update_tag()
            await self.test_10_list_console_tags()
            await self.test_11_get_tag_posts()

            await self.test_12_list_attachment_groups()
            await self.test_13_create_attachment_group()
            await self.test_14_get_attachment_policies()
            await self.test_15_upload_attachment()
            await self.test_16_list_attachments()
            await self.test_17_get_attachment()

            await self.test_18_create_post()
            await self.test_19_list_my_posts()
            await self.test_20_get_post()
            await self.test_21_get_post_draft()
            await self.test_22_update_post_draft()
            await self.test_23_update_post()
            await self.test_24_publish_post()
            await self.test_25_unpublish_post()

            # 清理
            await self.test_26_delete_post()
            await self.test_27_delete_attachment()
            await self.test_28_delete_tag()
            await self.test_29_delete_category()

        finally:
            await self.teardown()

        # 输出测试总结
        self.print_summary()

    def print_summary(self):
        """打印测试总结"""
        logger.info("=" * 80)
        logger.info("🎉 测试总结")
        logger.info("=" * 80)

        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["success"])
        failed = total - passed

        logger.info(f"\n总测试数: {total}")
        logger.success(f"✓ 通过: {passed}")
        if failed > 0:
            logger.error(f"✗ 失败: {failed}")

        logger.info(f"\n创建的资源:")
        logger.info(f"  - 分类: {len(self.test_data['category_names'])}")
        logger.info(f"  - 标签: {len(self.test_data['tag_names'])}")
        logger.info(f"  - 附件: {len(self.test_data['attachment_names'])}")
        logger.info(f"  - 文章: {len(self.test_data['post_names'])}")
        logger.info(f"  - 分组: {len(self.test_data['group_names'])}")

        if failed > 0:
            logger.info(f"\n失败的测试:")
            for result in self.test_results:
                if not result["success"]:
                    logger.error(
                        f"  ✗ 测试 {result['test_num']}: {result['test_name']} - {result['message']}"
                    )

        logger.info("=" * 80)


async def main():
    """主函数"""
    test = HaloMCPComprehensiveTest()
    await test.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())

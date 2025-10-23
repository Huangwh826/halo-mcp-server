#!/usr/bin/env python3
"""
Halo MCP 附件管理示例

本文件展示如何使用 Halo MCP 的附件管理功能。
"""

import asyncio
import os
import tempfile
from pathlib import Path
from halo_mcp_server.client.halo_client import HaloClient


async def attachment_management_examples():
    """附件管理功能示例"""
    
    # 初始化客户端
    client = HaloClient(
        base_url=os.getenv("HALO_BASE_URL"),
        token=os.getenv("HALO_TOKEN")
    )
    
    print("=== Halo MCP 附件管理示例 ===\n")
    
    # 1. 创建测试文件
    print("1. 创建测试文件")
    test_files = []
    try:
        # 创建临时目录
        temp_dir = Path(tempfile.mkdtemp())
        
        # 创建测试图片文件（SVG格式）
        svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="200" height="200" fill="#4CAF50"/>
  <text x="100" y="100" text-anchor="middle" dy=".3em" fill="white" font-size="20">测试图片</text>
</svg>'''
        
        test_image = temp_dir / "test_image.svg"
        test_image.write_text(svg_content, encoding='utf-8')
        test_files.append(test_image)
        
        # 创建测试文档文件
        doc_content = """# 测试文档

这是一个测试文档，用于演示附件上传功能。

## 内容
- 项目介绍
- 使用说明
- 注意事项
"""
        
        test_doc = temp_dir / "test_document.md"
        test_doc.write_text(doc_content, encoding='utf-8')
        test_files.append(test_doc)
        
        print(f"✓ 创建测试文件: {len(test_files)} 个")
        for file in test_files:
            print(f"  - {file.name} ({file.stat().st_size} bytes)")
            
    except Exception as e:
        print(f"✗ 创建测试文件失败: {e}")
        return
    
    # 2. 获取存储策略
    print("\n2. 获取存储策略")
    try:
        policies = await client.get_attachment_policies()
        print(f"✓ 可用存储策略:")
        for policy in policies:
            print(f"  - {policy['metadata']['name']}: {policy['spec']['displayName']}")
        
        # 使用默认策略
        default_policy = "default-policy"
        
    except Exception as e:
        print(f"✗ 获取存储策略失败: {e}")
        default_policy = "default-policy"
    
    # 3. 创建附件分组
    print("\n3. 创建附件分组")
    try:
        test_group = await client.create_attachment_group(
            display_name="测试附件组"
        )
        group_name = test_group['metadata']['name']
        print(f"✓ 创建附件分组: {group_name}")
        
    except Exception as e:
        print(f"✗ 创建附件分组失败: {e}")
        group_name = None
    
    # 4. 上传本地文件
    print("\n4. 上传本地文件")
    uploaded_attachments = []
    
    for test_file in test_files:
        try:
            attachment = await client.upload_attachment(
                file_path=str(test_file),
                group_name=group_name,
                policy_name=default_policy
            )
            uploaded_attachments.append(attachment['metadata']['name'])
            print(f"✓ 上传文件: {test_file.name} -> {attachment['metadata']['name']}")
            print(f"  URL: {attachment['status']['permalink']}")
            
        except Exception as e:
            print(f"✗ 上传文件 {test_file.name} 失败: {e}")
    
    # 5. 从URL上传文件
    print("\n5. 从URL上传文件")
    test_urls = [
        "https://via.placeholder.com/300x200/4CAF50/FFFFFF?text=Test+Image+1",
        "https://via.placeholder.com/400x300/2196F3/FFFFFF?text=Test+Image+2"
    ]
    
    for i, url in enumerate(test_urls, 1):
        try:
            attachment = await client.upload_attachment_from_url(
                url=url,
                group_name=group_name,
                policy_name=default_policy
            )
            uploaded_attachments.append(attachment['metadata']['name'])
            print(f"✓ 从URL上传: 测试图片{i} -> {attachment['metadata']['name']}")
            
        except Exception as e:
            print(f"✗ 从URL上传失败: {e}")
    
    # 6. 列出附件
    print("\n6. 列出附件")
    try:
        attachments = await client.list_attachments(
            page=0,
            size=10,
            group_name=group_name
        )
        print(f"✓ 找到 {attachments['total']} 个附件:")
        for attachment in attachments['items']:
            size = attachment['spec'].get('size', 0)
            media_type = attachment['spec'].get('mediaType', '未知')
            print(f"  - {attachment['spec']['displayName']} ({media_type}, {size} bytes)")
            
    except Exception as e:
        print(f"✗ 列出附件失败: {e}")
    
    # 7. 搜索特定类型的附件
    print("\n7. 搜索特定类型的附件")
    try:
        # 搜索图片
        images = await client.list_attachments(
            accepts=["image/*"],
            page=0,
            size=5
        )
        print(f"✓ 图片附件: {images['total']} 个")
        
        # 搜索文档
        documents = await client.list_attachments(
            accepts=["text/*", "application/pdf"],
            page=0,
            size=5
        )
        print(f"✓ 文档附件: {documents['total']} 个")
        
    except Exception as e:
        print(f"✗ 搜索附件失败: {e}")
    
    # 8. 获取附件详情
    print("\n8. 获取附件详情")
    if uploaded_attachments:
        try:
            attachment_name = uploaded_attachments[0]
            detail = await client.get_attachment(attachment_name)
            
            print(f"✓ 附件详情:")
            print(f"  名称: {detail['spec']['displayName']}")
            print(f"  类型: {detail['spec'].get('mediaType', '未知')}")
            print(f"  大小: {detail['spec'].get('size', 0)} bytes")
            print(f"  URL: {detail['status']['permalink']}")
            print(f"  上传时间: {detail['metadata']['creationTimestamp']}")
            
        except Exception as e:
            print(f"✗ 获取附件详情失败: {e}")
    
    # 9. 附件分组管理
    print("\n9. 附件分组管理")
    try:
        # 列出所有分组
        groups = await client.list_attachment_groups(page=0, size=10)
        print(f"✓ 附件分组: {groups['total']} 个")
        for group in groups['items']:
            print(f"  - {group['spec']['displayName']} ({group['metadata']['name']})")
        
        # 创建更多分组
        additional_groups = ["博客图片", "文档资料", "项目截图"]
        created_groups = []
        
        for group_display_name in additional_groups:
            try:
                new_group = await client.create_attachment_group(
                    display_name=group_display_name
                )
                created_groups.append(new_group['metadata']['name'])
                print(f"✓ 创建分组: {group_display_name}")
            except Exception as e:
                print(f"✗ 创建分组 {group_display_name} 失败: {e}")
        
    except Exception as e:
        print(f"✗ 分组管理失败: {e}")
        created_groups = []
    
    # 10. 附件搜索
    print("\n10. 附件搜索")
    try:
        # 按关键词搜索
        search_results = await client.list_attachments(
            keyword="test",
            page=0,
            size=5
        )
        print(f"✓ 搜索 'test': {search_results['total']} 个结果")
        
        # 按文件类型搜索
        type_searches = {
            "图片": ["image/*"],
            "文档": ["text/*", "application/*"],
            "视频": ["video/*"]
        }
        
        for type_name, accepts in type_searches.items():
            results = await client.list_attachments(
                accepts=accepts,
                page=0,
                size=1
            )
            print(f"✓ {type_name}文件: {results['total']} 个")
            
    except Exception as e:
        print(f"✗ 附件搜索失败: {e}")
    
    # 11. 附件统计
    print("\n11. 附件统计")
    try:
        all_attachments = await client.list_attachments(page=0, size=100)
        total_count = all_attachments['total']
        
        # 统计文件类型
        type_stats = {}
        total_size = 0
        
        for attachment in all_attachments['items']:
            media_type = attachment['spec'].get('mediaType', '未知')
            type_category = media_type.split('/')[0] if '/' in media_type else '其他'
            
            type_stats[type_category] = type_stats.get(type_category, 0) + 1
            total_size += attachment['spec'].get('size', 0)
        
        print(f"✓ 附件统计:")
        print(f"  总数量: {total_count}")
        print(f"  总大小: {total_size / 1024 / 1024:.2f} MB")
        print(f"  类型分布:")
        for type_name, count in type_stats.items():
            print(f"    {type_name}: {count} 个")
            
    except Exception as e:
        print(f"✗ 附件统计失败: {e}")
    
    # 12. 清理测试数据
    print("\n12. 清理测试数据")
    
    # 删除上传的附件
    for attachment_name in uploaded_attachments:
        try:
            await client.delete_attachment(attachment_name)
            print(f"✓ 删除附件: {attachment_name}")
        except Exception as e:
            print(f"✗ 删除附件 {attachment_name} 失败: {e}")
    
    # 删除创建的分组
    cleanup_groups = [group_name] + (created_groups if 'created_groups' in locals() else [])
    for group_to_delete in cleanup_groups:
        if group_to_delete:
            try:
                # 注意：实际的Halo API可能不支持删除分组，这里仅作示例
                print(f"ℹ 分组 {group_to_delete} 需要手动删除")
            except Exception as e:
                print(f"✗ 删除分组 {group_to_delete} 失败: {e}")
    
    # 删除临时文件
    try:
        for test_file in test_files:
            test_file.unlink()
        temp_dir.rmdir()
        print(f"✓ 清理临时文件")
    except Exception as e:
        print(f"✗ 清理临时文件失败: {e}")
    
    print("\n=== 附件管理示例完成 ===")


async def advanced_attachment_examples():
    """高级附件管理示例"""
    
    client = HaloClient(
        base_url=os.getenv("HALO_BASE_URL"),
        token=os.getenv("HALO_TOKEN")
    )
    
    print("\n=== 高级附件管理示例 ===\n")
    
    # 1. 批量上传处理
    print("1. 批量上传处理")
    try:
        # 模拟批量上传场景
        batch_urls = [
            f"https://via.placeholder.com/300x200/FF5722/FFFFFF?text=Batch+{i}"
            for i in range(1, 4)
        ]
        
        batch_results = []
        for i, url in enumerate(batch_urls, 1):
            try:
                result = await client.upload_attachment_from_url(url=url)
                batch_results.append(result['metadata']['name'])
                print(f"✓ 批量上传 {i}/{len(batch_urls)}: 成功")
            except Exception as e:
                print(f"✗ 批量上传 {i}/{len(batch_urls)}: {e}")
        
        print(f"✓ 批量上传完成: {len(batch_results)}/{len(batch_urls)} 成功")
        
        # 清理批量上传的文件
        for attachment_name in batch_results:
            try:
                await client.delete_attachment(attachment_name)
            except:
                pass
                
    except Exception as e:
        print(f"✗ 批量上传失败: {e}")
    
    # 2. 附件分类管理
    print("\n2. 附件分类管理")
    file_categories = {
        "图片素材": {
            "description": "博客文章配图和素材",
            "accepts": ["image/jpeg", "image/png", "image/svg+xml", "image/webp"]
        },
        "文档资料": {
            "description": "PDF文档和文本文件",
            "accepts": ["application/pdf", "text/markdown", "text/plain"]
        },
        "代码文件": {
            "description": "源代码和配置文件",
            "accepts": ["text/plain", "application/json", "text/x-python"]
        }
    }
    
    for category, info in file_categories.items():
        print(f"  {category}:")
        print(f"    描述: {info['description']}")
        print(f"    支持格式: {', '.join(info['accepts'])}")
    
    # 3. 存储策略分析
    print("\n3. 存储策略分析")
    try:
        policies = await client.get_attachment_policies()
        
        print("✓ 存储策略详情:")
        for policy in policies:
            spec = policy.get('spec', {})
            print(f"  - {spec.get('displayName', '未知策略')}:")
            print(f"    模板: {spec.get('templateName', '默认')}")
            if 'configMapName' in spec:
                print(f"    配置: {spec['configMapName']}")
                
    except Exception as e:
        print(f"✗ 存储策略分析失败: {e}")
    
    # 4. 附件性能优化建议
    print("\n4. 附件性能优化建议")
    optimization_tips = {
        "图片优化": [
            "使用WebP格式减少文件大小",
            "压缩图片质量到80-90%",
            "为不同设备提供不同尺寸",
            "使用SVG格式的矢量图标"
        ],
        "文件管理": [
            "定期清理无用附件",
            "使用CDN加速访问",
            "合理设置缓存策略",
            "监控存储空间使用"
        ],
        "上传策略": [
            "限制单文件大小",
            "验证文件类型",
            "使用异步上传",
            "提供上传进度反馈"
        ]
    }
    
    for category, tips in optimization_tips.items():
        print(f"  {category}:")
        for tip in tips:
            print(f"    • {tip}")
    
    print("\n=== 高级附件管理示例完成 ===")


async def attachment_best_practices():
    """附件管理最佳实践"""
    
    print("\n=== 附件管理最佳实践 ===\n")
    
    best_practices = {
        "文件命名": [
            "使用有意义的文件名",
            "避免特殊字符和空格",
            "包含日期或版本信息",
            "保持命名一致性"
        ],
        "分组策略": [
            "按内容类型分组",
            "按项目或主题分组",
            "按时间周期分组",
            "设置合理的分组层级"
        ],
        "安全考虑": [
            "验证文件类型和大小",
            "扫描恶意文件",
            "设置访问权限",
            "定期备份重要文件"
        ],
        "维护管理": [
            "定期清理无用文件",
            "监控存储使用情况",
            "优化文件访问性能",
            "建立文件归档策略"
        ]
    }
    
    for category, practices in best_practices.items():
        print(f"{category}:")
        for practice in practices:
            print(f"  • {practice}")
        print()
    
    # 文件类型建议
    print("推荐文件格式:")
    file_formats = {
        "图片": "WebP > PNG > JPEG > SVG(矢量图)",
        "文档": "Markdown > PDF > TXT",
        "代码": "原始格式 > 压缩包",
        "视频": "MP4 > WebM > AVI",
        "音频": "MP3 > OGG > WAV"
    }
    
    for type_name, formats in file_formats.items():
        print(f"  {type_name}: {formats}")
    
    print("\n=== 最佳实践介绍完成 ===")


if __name__ == "__main__":
    # 确保环境变量已设置
    if not os.getenv("HALO_BASE_URL") or not os.getenv("HALO_TOKEN"):
        print("请设置 HALO_BASE_URL 和 HALO_TOKEN 环境变量")
        exit(1)
    
    # 运行示例
    asyncio.run(attachment_management_examples())
    asyncio.run(advanced_attachment_examples())
    asyncio.run(attachment_best_practices())
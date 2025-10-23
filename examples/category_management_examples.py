#!/usr/bin/env python3
"""
Halo MCP 分类管理示例

本文件展示如何使用 Halo MCP 的分类管理功能。
"""

import asyncio
import os
from halo_mcp_server.client.halo_client import HaloClient


async def category_management_examples():
    """分类管理功能示例"""
    
    # 初始化客户端
    client = HaloClient(
        base_url=os.getenv("HALO_BASE_URL"),
        token=os.getenv("HALO_TOKEN")
    )
    
    print("=== Halo MCP 分类管理示例 ===\n")
    
    # 1. 创建新分类
    print("1. 创建新分类")
    try:
        new_category = await client.create_category(
            display_name="技术分享",
            description="分享编程技术和开发经验",
            slug="tech-sharing",
            priority=10
        )
        print(f"✓ 创建分类成功: {new_category['metadata']['name']}")
        category_name = new_category['metadata']['name']
    except Exception as e:
        print(f"✗ 创建分类失败: {e}")
        return
    
    # 2. 列出所有分类
    print("\n2. 列出所有分类")
    try:
        categories = await client.list_categories(page=0, size=10)
        print(f"✓ 找到 {categories['total']} 个分类:")
        for category in categories['items']:
            print(f"  - {category['spec']['displayName']} ({category['metadata']['name']})")
    except Exception as e:
        print(f"✗ 列出分类失败: {e}")
    
    # 3. 搜索分类
    print("\n3. 搜索分类")
    try:
        search_results = await client.list_categories(keyword="技术", page=0, size=5)
        print(f"✓ 搜索到 {search_results['total']} 个相关分类:")
        for category in search_results['items']:
            print(f"  - {category['spec']['displayName']}")
    except Exception as e:
        print(f"✗ 搜索分类失败: {e}")
    
    # 4. 获取分类详情
    print("\n4. 获取分类详情")
    try:
        category_detail = await client.get_category(category_name)
        print(f"✓ 分类详情:")
        print(f"  名称: {category_detail['spec']['displayName']}")
        print(f"  描述: {category_detail['spec'].get('description', '无')}")
        print(f"  优先级: {category_detail['spec'].get('priority', 0)}")
        print(f"  创建时间: {category_detail['metadata']['creationTimestamp']}")
    except Exception as e:
        print(f"✗ 获取分类详情失败: {e}")
    
    # 5. 更新分类
    print("\n5. 更新分类")
    try:
        updated_category = await client.update_category(
            name=category_name,
            display_name="技术分享与交流",
            description="分享编程技术、开发经验和技术心得",
            priority=15
        )
        print(f"✓ 更新分类成功: {updated_category['spec']['displayName']}")
    except Exception as e:
        print(f"✗ 更新分类失败: {e}")
    
    # 6. 创建子分类
    print("\n6. 创建子分类")
    try:
        sub_category = await client.create_category(
            display_name="Python教程",
            description="Python编程相关教程",
            slug="python-tutorials",
            priority=5
        )
        sub_category_name = sub_category['metadata']['name']
        print(f"✓ 创建子分类成功: {sub_category_name}")
        
        # 设置父子关系
        await client.update_category(
            name=category_name,
            children=[sub_category_name]
        )
        print(f"✓ 设置父子分类关系成功")
    except Exception as e:
        print(f"✗ 创建子分类失败: {e}")
    
    # 7. 获取分类下的文章
    print("\n7. 获取分类下的文章")
    try:
        category_posts = await client.get_category_posts(
            name=category_name,
            page=0,
            size=5
        )
        print(f"✓ 分类下有 {category_posts['total']} 篇文章:")
        for post in category_posts['items']:
            print(f"  - {post['spec']['title']}")
    except Exception as e:
        print(f"✗ 获取分类文章失败: {e}")
    
    # 8. 批量操作示例
    print("\n8. 批量创建分类")
    categories_to_create = [
        {"display_name": "前端开发", "description": "前端技术和框架", "slug": "frontend"},
        {"display_name": "后端开发", "description": "后端技术和架构", "slug": "backend"},
        {"display_name": "数据库", "description": "数据库设计和优化", "slug": "database"},
        {"display_name": "DevOps", "description": "运维和部署相关", "slug": "devops"}
    ]
    
    created_categories = []
    for cat_data in categories_to_create:
        try:
            new_cat = await client.create_category(**cat_data)
            created_categories.append(new_cat['metadata']['name'])
            print(f"✓ 创建分类: {cat_data['display_name']}")
        except Exception as e:
            print(f"✗ 创建分类 {cat_data['display_name']} 失败: {e}")
    
    # 9. 分类统计
    print("\n9. 分类统计")
    try:
        all_categories = await client.list_categories(page=0, size=100)
        total_categories = all_categories['total']
        
        # 统计各分类的文章数量
        category_stats = []
        for category in all_categories['items'][:5]:  # 只统计前5个分类
            try:
                posts = await client.get_category_posts(
                    name=category['metadata']['name'],
                    page=0,
                    size=1
                )
                category_stats.append({
                    'name': category['spec']['displayName'],
                    'post_count': posts['total']
                })
            except:
                continue
        
        print(f"✓ 总分类数: {total_categories}")
        print("✓ 分类文章统计:")
        for stat in category_stats:
            print(f"  - {stat['name']}: {stat['post_count']} 篇文章")
            
    except Exception as e:
        print(f"✗ 获取分类统计失败: {e}")
    
    # 10. 清理测试数据
    print("\n10. 清理测试数据")
    cleanup_categories = [category_name] + created_categories
    if 'sub_category_name' in locals():
        cleanup_categories.append(sub_category_name)
    
    for cat_name in cleanup_categories:
        try:
            await client.delete_category(cat_name)
            print(f"✓ 删除分类: {cat_name}")
        except Exception as e:
            print(f"✗ 删除分类 {cat_name} 失败: {e}")
    
    print("\n=== 分类管理示例完成 ===")


async def advanced_category_examples():
    """高级分类管理示例"""
    
    client = HaloClient(
        base_url=os.getenv("HALO_BASE_URL"),
        token=os.getenv("HALO_TOKEN")
    )
    
    print("\n=== 高级分类管理示例 ===\n")
    
    # 1. 分层分类结构
    print("1. 创建分层分类结构")
    try:
        # 创建主分类
        main_category = await client.create_category(
            display_name="编程语言",
            description="各种编程语言相关内容",
            slug="programming-languages"
        )
        main_name = main_category['metadata']['name']
        
        # 创建子分类
        sub_categories = []
        languages = ["Python", "JavaScript", "Java", "Go", "Rust"]
        
        for lang in languages:
            sub_cat = await client.create_category(
                display_name=f"{lang}编程",
                description=f"{lang}编程语言相关内容",
                slug=f"{lang.lower()}-programming"
            )
            sub_categories.append(sub_cat['metadata']['name'])
        
        # 设置父子关系
        await client.update_category(
            name=main_name,
            children=sub_categories
        )
        
        print(f"✓ 创建分层结构: {main_name} -> {len(sub_categories)} 个子分类")
        
        # 清理
        for sub_name in sub_categories:
            await client.delete_category(sub_name)
        await client.delete_category(main_name)
        
    except Exception as e:
        print(f"✗ 创建分层结构失败: {e}")
    
    # 2. 分类模板使用
    print("\n2. 使用分类模板")
    try:
        template_category = await client.create_category(
            display_name="项目展示",
            description="个人和开源项目展示",
            slug="projects",
            template="project"  # 使用项目模板
        )
        
        print(f"✓ 使用模板创建分类: {template_category['metadata']['name']}")
        
        # 清理
        await client.delete_category(template_category['metadata']['name'])
        
    except Exception as e:
        print(f"✗ 使用模板失败: {e}")
    
    # 3. 分类可见性控制
    print("\n3. 分类可见性控制")
    try:
        hidden_category = await client.create_category(
            display_name="内部文档",
            description="仅内部可见的文档",
            slug="internal-docs",
            hide_from_list=True  # 在列表中隐藏
        )
        
        print(f"✓ 创建隐藏分类: {hidden_category['metadata']['name']}")
        
        # 清理
        await client.delete_category(hidden_category['metadata']['name'])
        
    except Exception as e:
        print(f"✗ 创建隐藏分类失败: {e}")
    
    print("\n=== 高级分类管理示例完成 ===")


if __name__ == "__main__":
    # 确保环境变量已设置
    if not os.getenv("HALO_BASE_URL") or not os.getenv("HALO_TOKEN"):
        print("请设置 HALO_BASE_URL 和 HALO_TOKEN 环境变量")
        exit(1)
    
    # 运行示例
    asyncio.run(category_management_examples())
    asyncio.run(advanced_category_examples())
#!/usr/bin/env python3
"""
Halo MCP 标签管理示例

本文件展示如何使用 Halo MCP 的标签管理功能。
"""

import asyncio
import os
from halo_mcp_server.client.halo_client import HaloClient


async def tag_management_examples():
    """标签管理功能示例"""
    
    # 初始化客户端
    client = HaloClient(
        base_url=os.getenv("HALO_BASE_URL"),
        token=os.getenv("HALO_TOKEN")
    )
    
    print("=== Halo MCP 标签管理示例 ===\n")
    
    # 1. 创建新标签
    print("1. 创建新标签")
    try:
        new_tag = await client.create_tag(
            display_name="Python",
            color="#3776ab",  # Python官方蓝色
            slug="python"
        )
        print(f"✓ 创建标签成功: {new_tag['metadata']['name']}")
        tag_name = new_tag['metadata']['name']
    except Exception as e:
        print(f"✗ 创建标签失败: {e}")
        return
    
    # 2. 列出所有标签
    print("\n2. 列出所有标签")
    try:
        tags = await client.list_tags(page=0, size=20)
        print(f"✓ 找到 {tags['total']} 个标签:")
        for tag in tags['items'][:5]:  # 只显示前5个
            color = tag['spec'].get('color', '无颜色')
            print(f"  - {tag['spec']['displayName']} ({color})")
    except Exception as e:
        print(f"✗ 列出标签失败: {e}")
    
    # 3. 搜索标签
    print("\n3. 搜索标签")
    try:
        search_results = await client.list_tags(keyword="Python", page=0, size=5)
        print(f"✓ 搜索到 {search_results['total']} 个相关标签:")
        for tag in search_results['items']:
            print(f"  - {tag['spec']['displayName']}")
    except Exception as e:
        print(f"✗ 搜索标签失败: {e}")
    
    # 4. 获取标签详情
    print("\n4. 获取标签详情")
    try:
        tag_detail = await client.get_tag(tag_name)
        print(f"✓ 标签详情:")
        print(f"  名称: {tag_detail['spec']['displayName']}")
        print(f"  颜色: {tag_detail['spec'].get('color', '无')}")
        print(f"  别名: {tag_detail['spec'].get('slug', '无')}")
        print(f"  创建时间: {tag_detail['metadata']['creationTimestamp']}")
    except Exception as e:
        print(f"✗ 获取标签详情失败: {e}")
    
    # 5. 更新标签
    print("\n5. 更新标签")
    try:
        updated_tag = await client.update_tag(
            name=tag_name,
            display_name="Python编程",
            color="#306998"  # 更深的Python蓝色
        )
        print(f"✓ 更新标签成功: {updated_tag['spec']['displayName']}")
    except Exception as e:
        print(f"✗ 更新标签失败: {e}")
    
    # 6. 批量创建标签
    print("\n6. 批量创建标签")
    tags_to_create = [
        {"display_name": "JavaScript", "color": "#f7df1e", "slug": "javascript"},
        {"display_name": "React", "color": "#61dafb", "slug": "react"},
        {"display_name": "Vue.js", "color": "#4fc08d", "slug": "vuejs"},
        {"display_name": "Node.js", "color": "#339933", "slug": "nodejs"},
        {"display_name": "TypeScript", "color": "#3178c6", "slug": "typescript"}
    ]
    
    created_tags = []
    for tag_data in tags_to_create:
        try:
            new_tag = await client.create_tag(**tag_data)
            created_tags.append(new_tag['metadata']['name'])
            print(f"✓ 创建标签: {tag_data['display_name']} ({tag_data['color']})")
        except Exception as e:
            print(f"✗ 创建标签 {tag_data['display_name']} 失败: {e}")
    
    # 7. 获取标签下的文章
    print("\n7. 获取标签下的文章")
    try:
        tag_posts = await client.get_tag_posts(
            name=tag_name,
            page=0,
            size=5
        )
        print(f"✓ 标签下有 {tag_posts['total']} 篇文章:")
        for post in tag_posts['items']:
            print(f"  - {post['spec']['title']}")
    except Exception as e:
        print(f"✗ 获取标签文章失败: {e}")
    
    # 8. 标签颜色管理
    print("\n8. 标签颜色管理")
    color_schemes = {
        "技术类": ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6"],
        "生活类": ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4", "#ffeaa7"],
        "学习类": ["#6c5ce7", "#a29bfe", "#fd79a8", "#fdcb6e", "#e17055"]
    }
    
    for category, colors in color_schemes.items():
        print(f"  {category}推荐配色: {', '.join(colors)}")
    
    # 9. 控制台标签管理
    print("\n9. 控制台标签管理")
    try:
        console_tags = await client.list_console_tags(page=0, size=10)
        print(f"✓ 控制台标签数量: {console_tags['total']}")
        for tag in console_tags['items'][:3]:  # 只显示前3个
            post_count = tag.get('postCount', 0)
            print(f"  - {tag['spec']['displayName']}: {post_count} 篇文章")
    except Exception as e:
        print(f"✗ 获取控制台标签失败: {e}")
    
    # 10. 标签统计分析
    print("\n10. 标签统计分析")
    try:
        all_tags = await client.list_tags(page=0, size=100)
        total_tags = all_tags['total']
        
        # 统计标签使用情况
        tag_stats = []
        for tag in all_tags['items'][:5]:  # 只统计前5个标签
            try:
                posts = await client.get_tag_posts(
                    name=tag['metadata']['name'],
                    page=0,
                    size=1
                )
                tag_stats.append({
                    'name': tag['spec']['displayName'],
                    'color': tag['spec'].get('color', '无'),
                    'post_count': posts['total']
                })
            except:
                continue
        
        print(f"✓ 总标签数: {total_tags}")
        print("✓ 热门标签统计:")
        for stat in sorted(tag_stats, key=lambda x: x['post_count'], reverse=True):
            print(f"  - {stat['name']} ({stat['color']}): {stat['post_count']} 篇文章")
            
    except Exception as e:
        print(f"✗ 获取标签统计失败: {e}")
    
    # 11. 清理测试数据
    print("\n11. 清理测试数据")
    cleanup_tags = [tag_name] + created_tags
    
    for tag_name_to_delete in cleanup_tags:
        try:
            await client.delete_tag(tag_name_to_delete)
            print(f"✓ 删除标签: {tag_name_to_delete}")
        except Exception as e:
            print(f"✗ 删除标签 {tag_name_to_delete} 失败: {e}")
    
    print("\n=== 标签管理示例完成 ===")


async def advanced_tag_examples():
    """高级标签管理示例"""
    
    client = HaloClient(
        base_url=os.getenv("HALO_BASE_URL"),
        token=os.getenv("HALO_TOKEN")
    )
    
    print("\n=== 高级标签管理示例 ===\n")
    
    # 1. 标签分组管理
    print("1. 标签分组管理")
    tag_groups = {
        "编程语言": [
            {"name": "Python", "color": "#3776ab"},
            {"name": "JavaScript", "color": "#f7df1e"},
            {"name": "Java", "color": "#ed8b00"},
            {"name": "Go", "color": "#00add8"},
            {"name": "Rust", "color": "#000000"}
        ],
        "前端框架": [
            {"name": "React", "color": "#61dafb"},
            {"name": "Vue", "color": "#4fc08d"},
            {"name": "Angular", "color": "#dd0031"},
            {"name": "Svelte", "color": "#ff3e00"}
        ],
        "后端技术": [
            {"name": "Django", "color": "#092e20"},
            {"name": "Flask", "color": "#000000"},
            {"name": "FastAPI", "color": "#009688"},
            {"name": "Express", "color": "#000000"}
        ]
    }
    
    created_group_tags = []
    for group_name, tags in tag_groups.items():
        print(f"\n  创建 {group_name} 标签组:")
        for tag_info in tags:
            try:
                new_tag = await client.create_tag(
                    display_name=tag_info["name"],
                    color=tag_info["color"],
                    slug=tag_info["name"].lower().replace(".", "")
                )
                created_group_tags.append(new_tag['metadata']['name'])
                print(f"    ✓ {tag_info['name']} ({tag_info['color']})")
            except Exception as e:
                print(f"    ✗ {tag_info['name']} 失败: {e}")
    
    # 2. 标签颜色主题
    print("\n2. 标签颜色主题")
    color_themes = {
        "Material Design": {
            "Red": "#f44336",
            "Pink": "#e91e63", 
            "Purple": "#9c27b0",
            "Deep Purple": "#673ab7",
            "Indigo": "#3f51b5",
            "Blue": "#2196f3",
            "Light Blue": "#03a9f4",
            "Cyan": "#00bcd4",
            "Teal": "#009688",
            "Green": "#4caf50"
        },
        "GitHub": {
            "JavaScript": "#f1e05a",
            "Python": "#3572a5",
            "Java": "#b07219",
            "TypeScript": "#2b7489",
            "C++": "#f34b7d",
            "C#": "#239120",
            "PHP": "#4f5d95",
            "Ruby": "#701516",
            "Go": "#00add8",
            "Rust": "#dea584"
        }
    }
    
    for theme_name, colors in color_themes.items():
        print(f"  {theme_name} 主题:")
        for lang, color in list(colors.items())[:3]:  # 只显示前3个
            print(f"    {lang}: {color}")
    
    # 3. 标签搜索和过滤
    print("\n3. 标签搜索和过滤")
    try:
        # 按关键词搜索
        search_keywords = ["python", "java", "react"]
        for keyword in search_keywords:
            results = await client.list_tags(keyword=keyword, size=3)
            print(f"  搜索 '{keyword}': {results['total']} 个结果")
        
        # 按颜色过滤（模拟）
        all_tags = await client.list_tags(size=50)
        blue_tags = [
            tag for tag in all_tags['items'] 
            if tag['spec'].get('color', '').lower().find('blue') != -1 or
               tag['spec'].get('color', '').startswith('#2') or
               tag['spec'].get('color', '').startswith('#3')
        ]
        print(f"  蓝色系标签: {len(blue_tags)} 个")
        
    except Exception as e:
        print(f"✗ 标签搜索失败: {e}")
    
    # 4. 标签使用分析
    print("\n4. 标签使用分析")
    try:
        # 获取所有标签的使用统计
        console_tags = await client.list_console_tags(size=20)
        
        if console_tags['items']:
            # 按使用频率排序
            usage_stats = []
            for tag in console_tags['items'][:10]:
                post_count = tag.get('postCount', 0)
                usage_stats.append({
                    'name': tag['spec']['displayName'],
                    'count': post_count
                })
            
            usage_stats.sort(key=lambda x: x['count'], reverse=True)
            
            print("  标签使用排行:")
            for i, stat in enumerate(usage_stats[:5], 1):
                print(f"    {i}. {stat['name']}: {stat['count']} 次")
        
    except Exception as e:
        print(f"✗ 标签分析失败: {e}")
    
    # 5. 清理测试数据
    print("\n5. 清理测试数据")
    for tag_name in created_group_tags:
        try:
            await client.delete_tag(tag_name)
            print(f"✓ 删除标签: {tag_name}")
        except Exception as e:
            print(f"✗ 删除标签 {tag_name} 失败: {e}")
    
    print("\n=== 高级标签管理示例完成 ===")


async def tag_best_practices():
    """标签管理最佳实践"""
    
    print("\n=== 标签管理最佳实践 ===\n")
    
    practices = {
        "命名规范": [
            "使用简洁明确的名称",
            "避免过长的标签名",
            "保持一致的命名风格",
            "使用英文或中文，避免混用"
        ],
        "颜色选择": [
            "为相关标签使用相似色系",
            "确保颜色对比度足够",
            "避免使用过于鲜艳的颜色",
            "考虑色盲用户的体验"
        ],
        "标签分类": [
            "按技术栈分组（如前端、后端）",
            "按难度级别分组（如初级、中级、高级）",
            "按内容类型分组（如教程、实战、理论）",
            "按更新频率分组（如热门、冷门）"
        ],
        "使用策略": [
            "每篇文章使用3-8个标签",
            "优先使用已有标签",
            "定期清理无用标签",
            "监控标签使用统计"
        ]
    }
    
    for category, tips in practices.items():
        print(f"{category}:")
        for tip in tips:
            print(f"  • {tip}")
        print()
    
    print("=== 最佳实践介绍完成 ===")


if __name__ == "__main__":
    # 确保环境变量已设置
    if not os.getenv("HALO_BASE_URL") or not os.getenv("HALO_TOKEN"):
        print("请设置 HALO_BASE_URL 和 HALO_TOKEN 环境变量")
        exit(1)
    
    # 运行示例
    asyncio.run(tag_management_examples())
    asyncio.run(advanced_tag_examples())
    asyncio.run(tag_best_practices())
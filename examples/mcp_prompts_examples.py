#!/usr/bin/env python3
"""
Halo MCP Prompts 使用示例

本文件展示如何使用 Halo MCP 的智能写作助手功能。
"""

import asyncio
import os
from halo_mcp_server.prompts.blog_prompts import BLOG_PROMPTS


def demonstrate_prompts():
    """演示所有可用的 MCP Prompts"""
    
    print("=== Halo MCP Prompts 使用示例 ===\n")
    
    # 1. 博客写作助手
    print("1. 博客写作助手 (halo_blog_writing_assistant)")
    print("   功能: 提供写作建议、结构规划和内容优化")
    print("   参数:")
    print("     - topic: 文章主题")
    print("     - style: 写作风格 (技术教程/经验分享/观点评论)")
    print("     - target_audience: 目标读者")
    print("   示例调用:")
    print("     topic='Python异步编程', style='技术教程', target_audience='中级开发者'")
    print()
    
    # 2. 内容优化器
    print("2. 内容优化器 (halo_content_optimizer)")
    print("   功能: 优化文章内容的可读性、结构和表达")
    print("   参数:")
    print("     - content: 原始内容")
    print("     - optimization_goals: 优化目标")
    print("   示例调用:")
    print("     content='原始文章内容...', optimization_goals='提高可读性,增强逻辑性'")
    print()
    
    # 3. SEO优化器
    print("3. SEO优化器 (halo_seo_optimizer)")
    print("   功能: 优化文章的搜索引擎友好性")
    print("   参数:")
    print("     - content: 文章内容")
    print("     - target_keywords: 目标关键词")
    print("   示例调用:")
    print("     content='文章内容...', target_keywords='Python,异步编程,asyncio'")
    print()
    
    # 4. 标题生成器
    print("4. 标题生成器 (halo_title_generator)")
    print("   功能: 根据内容生成吸引人的标题")
    print("   参数:")
    print("     - content: 文章内容")
    print("     - style: 标题风格")
    print("     - count: 生成数量")
    print("   示例调用:")
    print("     content='文章内容...', style='吸引人的', count=5")
    print()
    
    # 5. 摘要生成器
    print("5. 摘要生成器 (halo_excerpt_generator)")
    print("   功能: 生成文章摘要")
    print("   参数:")
    print("     - content: 文章内容")
    print("     - max_length: 最大长度")
    print("   示例调用:")
    print("     content='文章内容...', max_length=200")
    print()
    
    # 6. 标签建议器
    print("6. 标签建议器 (halo_tag_suggester)")
    print("   功能: 根据内容建议合适的标签")
    print("   参数:")
    print("     - content: 文章内容")
    print("     - max_tags: 最大标签数")
    print("   示例调用:")
    print("     content='文章内容...', max_tags=8")
    print()
    
    # 7. 分类建议器
    print("7. 分类建议器 (halo_category_suggester)")
    print("   功能: 建议文章分类")
    print("   参数:")
    print("     - content: 文章内容")
    print("     - existing_categories: 现有分类")
    print("   示例调用:")
    print("     content='文章内容...', existing_categories='技术分享,编程教程'")
    print()
    
    # 8. 内容翻译器
    print("8. 内容翻译器 (halo_content_translator)")
    print("   功能: 翻译文章内容")
    print("   参数:")
    print("     - content: 原始内容")
    print("     - target_language: 目标语言")
    print("   示例调用:")
    print("     content='Hello World', target_language='中文'")
    print()
    
    # 9. 内容校对器
    print("9. 内容校对器 (halo_content_proofreader)")
    print("   功能: 校对文章的语法和表达")
    print("   参数:")
    print("     - content: 文章内容")
    print("     - language: 语言")
    print("   示例调用:")
    print("     content='文章内容...', language='中文'")
    print()
    
    # 10. 系列规划器
    print("10. 系列规划器 (halo_series_planner)")
    print("    功能: 规划文章系列的结构和内容")
    print("    参数:")
    print("      - topic: 系列主题")
    print("      - target_audience: 目标读者")
    print("      - article_count: 文章数量")
    print("    示例调用:")
    print("      topic='Python进阶教程', target_audience='中高级开发者', article_count=10")
    print()


def demonstrate_writing_workflow():
    """演示完整的写作工作流程"""
    
    print("=== 完整写作工作流程示例 ===\n")
    
    # 模拟写作流程
    workflow_steps = [
        {
            "step": "1. 主题规划",
            "prompt": "halo_series_planner",
            "description": "规划整个系列的结构",
            "example": "规划'Python Web开发'系列，包含10篇文章"
        },
        {
            "step": "2. 内容创作",
            "prompt": "halo_blog_writing_assistant", 
            "description": "获取写作建议和大纲",
            "example": "为'Flask入门教程'获取写作指导"
        },
        {
            "step": "3. 标题优化",
            "prompt": "halo_title_generator",
            "description": "生成多个标题选项",
            "example": "生成5个吸引人的标题"
        },
        {
            "step": "4. 内容优化",
            "prompt": "halo_content_optimizer",
            "description": "优化文章结构和表达",
            "example": "提高可读性和逻辑性"
        },
        {
            "step": "5. SEO优化",
            "prompt": "halo_seo_optimizer",
            "description": "优化搜索引擎友好性",
            "example": "针对'Flask,Python,Web开发'关键词优化"
        },
        {
            "step": "6. 摘要生成",
            "prompt": "halo_excerpt_generator",
            "description": "生成文章摘要",
            "example": "生成200字以内的摘要"
        },
        {
            "step": "7. 标签建议",
            "prompt": "halo_tag_suggester",
            "description": "建议相关标签",
            "example": "建议8个相关标签"
        },
        {
            "step": "8. 分类建议",
            "prompt": "halo_category_suggester",
            "description": "建议文章分类",
            "example": "从现有分类中选择最合适的"
        },
        {
            "step": "9. 内容校对",
            "prompt": "halo_content_proofreader",
            "description": "检查语法和表达",
            "example": "校对中文表达和标点符号"
        },
        {
            "step": "10. 多语言版本",
            "prompt": "halo_content_translator",
            "description": "翻译为其他语言",
            "example": "翻译为英文版本"
        }
    ]
    
    for step_info in workflow_steps:
        print(f"{step_info['step']}: {step_info['description']}")
        print(f"   使用工具: {step_info['prompt']}")
        print(f"   示例: {step_info['example']}")
        print()


def demonstrate_prompt_combinations():
    """演示 Prompt 组合使用"""
    
    print("=== Prompt 组合使用示例 ===\n")
    
    # 场景1: 技术博客创作
    print("场景1: 技术博客创作")
    tech_blog_flow = [
        "halo_blog_writing_assistant → 获取技术写作建议",
        "halo_title_generator → 生成技术性标题",
        "halo_seo_optimizer → 优化技术关键词",
        "halo_tag_suggester → 建议技术标签",
        "halo_content_proofreader → 校对技术术语"
    ]
    
    for step in tech_blog_flow:
        print(f"  • {step}")
    print()
    
    # 场景2: 多语言内容
    print("场景2: 多语言内容创作")
    multilingual_flow = [
        "halo_blog_writing_assistant → 中文内容创作",
        "halo_content_optimizer → 优化中文表达",
        "halo_content_translator → 翻译为英文",
        "halo_content_proofreader → 校对英文版本",
        "halo_seo_optimizer → 分别优化中英文SEO"
    ]
    
    for step in multilingual_flow:
        print(f"  • {step}")
    print()
    
    # 场景3: 系列文章规划
    print("场景3: 系列文章规划")
    series_flow = [
        "halo_series_planner → 规划整个系列",
        "halo_blog_writing_assistant → 每篇文章的写作指导",
        "halo_category_suggester → 统一分类策略",
        "halo_tag_suggester → 系列标签体系",
        "halo_content_optimizer → 保持系列一致性"
    ]
    
    for step in series_flow:
        print(f"  • {step}")
    print()


def demonstrate_advanced_usage():
    """演示高级使用技巧"""
    
    print("=== 高级使用技巧 ===\n")
    
    # 1. 参数优化
    print("1. 参数优化技巧")
    optimization_tips = {
        "写作助手": [
            "明确目标读者群体",
            "选择合适的写作风格",
            "提供具体的主题描述"
        ],
        "标题生成": [
            "尝试不同的风格参数",
            "生成多个选项进行对比",
            "考虑SEO和吸引力平衡"
        ],
        "内容优化": [
            "设定明确的优化目标",
            "分步骤进行优化",
            "保持原文的核心观点"
        ],
        "SEO优化": [
            "研究目标关键词",
            "平衡关键词密度",
            "优化标题和摘要"
        ]
    }
    
    for category, tips in optimization_tips.items():
        print(f"  {category}:")
        for tip in tips:
            print(f"    • {tip}")
    print()
    
    # 2. 质量控制
    print("2. 质量控制策略")
    quality_strategies = [
        "使用多个Prompt交叉验证",
        "人工审核AI生成的内容",
        "保持品牌声音的一致性",
        "定期评估输出质量",
        "收集读者反馈进行改进"
    ]
    
    for strategy in quality_strategies:
        print(f"  • {strategy}")
    print()
    
    # 3. 效率提升
    print("3. 效率提升方法")
    efficiency_methods = [
        "建立标准化的工作流程",
        "创建常用参数模板",
        "批量处理相似内容",
        "自动化重复性任务",
        "建立内容质量检查清单"
    ]
    
    for method in efficiency_methods:
        print(f"  • {method}")
    print()


def show_prompt_details():
    """显示所有 Prompt 的详细信息"""
    
    print("=== Prompt 详细信息 ===\n")
    
    for prompt in BLOG_PROMPTS:
        print(f"名称: {prompt.name}")
        print(f"描述: {prompt.description}")
        print("参数:")
        
        for arg in prompt.arguments:
            required = "必填" if arg.required else "可选"
            print(f"  - {arg.name} ({required}): {arg.description}")
        
        print("-" * 50)


if __name__ == "__main__":
    # 运行所有示例
    demonstrate_prompts()
    demonstrate_writing_workflow()
    demonstrate_prompt_combinations()
    demonstrate_advanced_usage()
    show_prompt_details()
    
    print("\n=== MCP Prompts 示例完成 ===")
    print("\n💡 提示:")
    print("1. 这些Prompt可以在支持MCP的客户端中使用")
    print("2. 参数可以根据具体需求进行调整")
    print("3. 建议结合多个Prompt使用以获得最佳效果")
    print("4. 定期更新和优化Prompt参数以提高质量")
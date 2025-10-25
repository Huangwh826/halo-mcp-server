"""MCP 服务器实现。"""

from typing import Any, Dict, Optional

from loguru import logger
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Prompt, Tool

from halo_mcp_server.client import HaloClient
from halo_mcp_server.config import settings
from halo_mcp_server.prompts import BLOG_PROMPTS
from halo_mcp_server.tools.attachment_tools import ATTACHMENT_TOOLS
from halo_mcp_server.tools.category_tools import CATEGORY_TOOLS
from halo_mcp_server.tools.post_tools import (
    create_post_tool,
    delete_post_tool,
    get_post_draft_tool,
    get_post_tool,
    list_my_posts_tool,
    publish_post_tool,
    unpublish_post_tool,
    update_post_draft_tool,
    update_post_tool,
    POST_TOOLS,
)
from halo_mcp_server.tools.tag_tools import TAG_TOOLS
from halo_mcp_server.tools.site_tools import SITE_TOOLS
from halo_mcp_server.models.common import ToolResult


# Create MCP server instance
app = Server(settings.mcp_server_name)

# Global Halo client instance
halo_client: Optional[HaloClient] = None


async def get_halo_client() -> HaloClient:
    """获取或创建 Halo 客户端实例。"""
    global halo_client
    if halo_client is None:
        halo_client = HaloClient()
        await halo_client.connect()
        await halo_client.authenticate()
        logger.info("Halo 客户端已初始化")
    return halo_client


@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    """列出可用的 MCP 提示。"""
    logger.debug("正在列出提示...")
    logger.info(f"已注册 {len(BLOG_PROMPTS)} 个提示")
    return BLOG_PROMPTS


@app.get_prompt()
async def get_prompt(name: str, arguments: Dict[str, str]) -> str:
    """根据参数获取提示内容。"""
    logger.info(f"获取提示：{name}")
    logger.debug(f"参数：{arguments}")

    # Find the prompt by name
    prompt = None
    for p in BLOG_PROMPTS:
        if p.name == name:
            prompt = p
            break

    if not prompt:
        raise ValueError(f"未找到提示：'{name}'")

    # Generate prompt content based on the prompt type
    if name == "halo_blog_writing_assistant":
        return _generate_writing_assistant_prompt(arguments)
    elif name == "halo_content_optimizer":
        return _generate_content_optimizer_prompt(arguments)
    elif name == "halo_seo_optimizer":
        return _generate_seo_optimizer_prompt(arguments)
    elif name == "halo_title_generator":
        return _generate_title_generator_prompt(arguments)
    elif name == "halo_excerpt_generator":
        return _generate_excerpt_generator_prompt(arguments)
    elif name == "halo_tag_suggester":
        return _generate_tag_suggester_prompt(arguments)
    elif name == "halo_category_suggester":
        return _generate_category_suggester_prompt(arguments)
    elif name == "halo_content_translator":
        return _generate_content_translator_prompt(arguments)
    elif name == "halo_content_proofreader":
        return _generate_content_proofreader_prompt(arguments)
    elif name == "halo_series_planner":
        return _generate_series_planner_prompt(arguments)
    else:
        raise ValueError(f"未知的提示：{name}")


def _generate_writing_assistant_prompt(args: Dict[str, str]) -> str:
    """生成写作助手提示。"""
    topic = args.get("topic", "")
    target_audience = args.get("target_audience", "一般读者")
    article_type = args.get("article_type", "技术文章")
    word_count = args.get("word_count", "1500")
    tone = args.get("tone", "专业且易懂")

    return f"""你是一位专业的博客写作助手。请根据以下要求创建一篇高质量的博客文章：

**文章主题：** {topic}
**目标读者：** {target_audience}
**文章类型：** {article_type}
**期望字数：** {word_count} 字
**写作风格：** {tone}

请按照以下结构创建文章：

1. **引人入胜的开头**
   - 用一个有趣的事实、问题或故事开始
   - 明确说明读者将从这篇文章中获得什么

2. **清晰的主体内容**
   - 使用小标题组织内容
   - 提供具体的例子和实用建议
   - 确保逻辑清晰，层次分明

3. **有力的结尾**
   - 总结关键要点
   - 提供行动建议或下一步指导

**写作要求：**
- 使用 Markdown 格式
- 语言{tone}，适合{target_audience}
- 包含适当的代码示例（如果适用）
- 添加相关的图片描述或图表说明
- 确保内容原创且有价值

请开始创作这篇关于"{topic}"的文章。"""


def _generate_content_optimizer_prompt(args: Dict[str, str]) -> str:
    """生成内容优化提示。"""
    content = args.get("content", "")
    optimization_focus = args.get("optimization_focus", "整体优化")
    target_length = args.get("target_length", "保持不变")

    return f"""你是一位专业的内容优化专家。请优化以下文章内容：

**优化重点：** {optimization_focus}
**长度要求：** {target_length}

**原始内容：**
{content}

**优化指导原则：**

1. **可读性优化**
   - 简化复杂句子
   - 使用更清晰的表达
   - 改善段落结构

2. **结构优化**
   - 添加或改进小标题
   - 重新组织内容逻辑
   - 确保信息流畅

3. **吸引力提升**
   - 使用更生动的语言
   - 添加具体例子
   - 增强读者参与感

4. **专业性保持**
   - 确保技术准确性
   - 保持专业术语的正确使用
   - 维护内容的权威性

请提供优化后的内容，并简要说明主要改进点。"""


def _generate_seo_optimizer_prompt(args: Dict[str, str]) -> str:
    """生成 SEO 优化提示。"""
    title = args.get("title", "")
    content = args.get("content", "")
    target_keywords = args.get("target_keywords", "")
    meta_description_length = args.get("meta_description_length", "160")

    return f"""你是一位 SEO 优化专家。请为以下文章提供 SEO 优化建议：

**原始标题：** {title}
**目标关键词：** {target_keywords}
**元描述长度限制：** {meta_description_length} 字符

**文章内容：**
{content}

**请提供以下 SEO 优化建议：**

1. **标题优化**
   - 提供 3-5 个 SEO 友好的标题选项
   - 确保包含主要关键词
   - 保持标题吸引力和可读性

2. **元描述**
   - 创建简洁有力的元描述
   - 包含关键词但避免堆砌
   - 在 {meta_description_length} 字符内

3. **内容优化建议**
   - 关键词密度和分布建议
   - 内部链接机会
   - 图片 alt 文本建议

4. **结构化数据建议**
   - 适合的 Schema 标记
   - 标题层级优化

5. **URL 建议**
   - SEO 友好的 URL slug

请确保所有建议都符合搜索引擎最佳实践。"""


def _generate_title_generator_prompt(args: Dict[str, str]) -> str:
    """生成标题生成器提示。"""
    content_summary = args.get("content_summary", "")
    title_style = args.get("title_style", "多样化")
    title_count = args.get("title_count", "5")

    return f"""你是一位专业的标题创作专家。请为以下内容生成吸引人的标题：

**内容摘要：** {content_summary}
**标题风格：** {title_style}
**生成数量：** {title_count} 个

**标题创作要求：**

1. **吸引力**
   - 激发读者好奇心
   - 突出文章价值
   - 使用有力的词汇

2. **清晰性**
   - 准确反映内容
   - 避免误导性表述
   - 易于理解

3. **SEO 友好**
   - 包含相关关键词
   - 长度适中（50-60 字符）
   - 避免特殊符号

**不同风格的标题类型：**
- **问题式：** 以疑问句形式吸引读者
- **数字式：** 使用具体数字增加可信度
- **对比式：** 突出前后对比或优劣比较
- **悬念式：** 制造悬念激发好奇
- **实用式：** 强调实用价值和解决方案

请生成 {title_count} 个不同风格的标题选项，并简要说明每个标题的特点。"""


def _generate_excerpt_generator_prompt(args: Dict[str, str]) -> str:
    """生成摘要生成器提示。"""
    content = args.get("content", "")
    excerpt_length = args.get("excerpt_length", "中等长度")
    excerpt_style = args.get("excerpt_style", "概述式")

    return f"""你是一位专业的内容摘要专家。请为以下文章创建精彩的摘要：

**摘要长度：** {excerpt_length}
**摘要风格：** {excerpt_style}

**文章内容：**
{content}

**摘要创作要求：**

1. **准确性**
   - 准确反映文章核心内容
   - 不包含文章中没有的信息
   - 保持与原文一致的观点

2. **吸引力**
   - 激发读者阅读兴趣
   - 突出文章的独特价值
   - 使用引人入胜的语言

3. **完整性**
   - 涵盖文章主要观点
   - 体现文章结构逻辑
   - 给读者完整的预期

**不同风格的摘要：**
- **概述式：** 简洁概括文章主要内容
- **亮点式：** 突出文章最有价值的部分
- **问题式：** 以问题引导读者思考

**长度指导：**
- 短：80-120 字
- 中：120-200 字
- 长：200-300 字

请创建一个{excerpt_length}的{excerpt_style}摘要。"""


def _generate_tag_suggester_prompt(args: Dict[str, str]) -> str:
    """生成标签建议提示。"""
    title = args.get("title", "")
    content = args.get("content", "")
    existing_tags = args.get("existing_tags", "")
    tag_count = args.get("tag_count", "5-8")

    return f"""你是一位专业的内容标签专家。请为以下文章推荐合适的标签：

**文章标题：** {title}
**现有标签：** {existing_tags}
**建议数量：** {tag_count} 个

**文章内容：**
{content}

**标签推荐原则：**

1. **相关性**
   - 直接相关的技术、概念或主题
   - 反映文章核心内容
   - 帮助读者快速理解文章主题

2. **搜索价值**
   - 读者可能搜索的关键词
   - 有助于内容发现
   - 平衡热门和长尾标签

3. **分类层次**
   - 技术类标签（编程语言、框架、工具等）
   - 概念类标签（设计模式、最佳实践等）
   - 应用类标签（Web开发、移动开发等）

4. **标签质量**
   - 避免过于宽泛的标签
   - 避免重复或相似的标签
   - 使用标准化的术语

**请提供：**
1. 推荐的 {tag_count} 个标签
2. 每个标签的选择理由
3. 标签的优先级排序

注意：如果提供了现有标签列表，请优先从中选择合适的标签，必要时可以建议新标签。"""


def _generate_category_suggester_prompt(args: Dict[str, str]) -> str:
    """生成分类建议提示。"""
    title = args.get("title", "")
    content = args.get("content", "")
    existing_categories = args.get("existing_categories", "")

    return f"""你是一位专业的内容分类专家。请为以下文章推荐最合适的分类：

**文章标题：** {title}
**现有分类：** {existing_categories}

**文章内容：**
{content}

**分类推荐原则：**

1. **主题匹配**
   - 分析文章的核心主题
   - 确定文章的主要领域
   - 考虑内容的深度和广度

2. **层级结构**
   - 优先选择最具体的分类
   - 考虑分类的层级关系
   - 避免过于宽泛的分类

3. **读者期望**
   - 考虑读者的浏览习惯
   - 便于内容发现和导航
   - 保持分类的一致性

**分析步骤：**
1. 识别文章的主要技术栈或领域
2. 确定文章的类型（教程、经验分享、工具介绍等）
3. 评估内容的技术深度
4. 考虑目标读者群体

**请提供：**
1. 最推荐的主分类（1个）
2. 可选的次要分类（如果适用）
3. 分类选择的详细理由
4. 如果现有分类不合适，建议新的分类名称

注意：如果提供了现有分类列表，请优先从中选择最合适的分类。"""


def _generate_content_translator_prompt(args: Dict[str, str]) -> str:
    """生成内容翻译提示。"""
    content = args.get("content", "")
    target_language = args.get("target_language", "")
    preserve_formatting = args.get("preserve_formatting", "是")
    translation_style = args.get("translation_style", "意译")

    return f"""你是一位专业的技术内容翻译专家。请将以下内容翻译成{target_language}：

**翻译风格：** {translation_style}
**保持格式：** {preserve_formatting}

**原始内容：**
{content}

**翻译要求：**

1. **准确性**
   - 准确传达原文含义
   - 保持技术术语的准确性
   - 不遗漏重要信息

2. **流畅性**
   - 符合目标语言的表达习惯
   - 语句通顺自然
   - 避免直译造成的生硬表达

3. **专业性**
   - 使用标准的技术术语
   - 保持专业文档的风格
   - 确保术语一致性

4. **格式保持**
   {"- 保持 Markdown 格式不变" if preserve_formatting == "是" else "- 可以调整格式以适应目标语言"}
   - 保持代码块和链接
   - 维护列表和表格结构

**翻译风格说明：**
- **直译：** 尽可能保持原文结构
- **意译：** 优先考虑目标语言的表达习惯
- **本地化：** 适应目标文化和使用习惯

请提供高质量的{target_language}翻译。"""


def _generate_content_proofreader_prompt(args: Dict[str, str]) -> str:
    """生成内容校对提示。"""
    content = args.get("content", "")
    language = args.get("language", "中文")
    check_focus = args.get("check_focus", "全面检查")

    return f"""你是一位专业的{language}内容校对专家。请仔细校对以下内容：

**校对重点：** {check_focus}
**内容语言：** {language}

**待校对内容：**
{content}

**校对检查项目：**

1. **语法检查**
   - 句法结构是否正确
   - 时态和语态使用
   - 标点符号使用

2. **拼写检查**
   - 错别字识别
   - 专业术语拼写
   - 英文单词拼写

3. **表达优化**
   - 语句是否通顺
   - 表达是否清晰
   - 用词是否准确

4. **逻辑检查**
   - 内容逻辑是否清晰
   - 前后是否一致
   - 论述是否完整

5. **格式检查**
   - Markdown 格式是否正确
   - 标题层级是否合理
   - 列表格式是否统一

**请提供：**
1. 校对后的完整内容
2. 主要修改说明
3. 改进建议

注意：保持原文的风格和观点，只进行必要的语言和格式修正。"""


def _generate_series_planner_prompt(args: Dict[str, str]) -> str:
    """生成系列规划提示。"""
    series_topic = args.get("series_topic", "")
    target_audience = args.get("target_audience", "技术开发者")
    article_count = args.get("article_count", "5-8")
    difficulty_progression = args.get("difficulty_progression", "由浅入深")

    return f"""你是一位专业的技术内容规划专家。请为以下主题规划一个系列文章：

**系列主题：** {series_topic}
**目标读者：** {target_audience}
**文章数量：** {article_count} 篇
**难度递进：** {difficulty_progression}

**系列规划要求：**

1. **整体结构**
   - 设计清晰的学习路径
   - 确保内容的连贯性
   - 平衡理论和实践

2. **难度设计**
   - 根据"{difficulty_progression}"安排内容
   - 确保每篇文章都有适当的挑战性
   - 为不同水平的读者提供价值

3. **内容覆盖**
   - 涵盖主题的核心概念
   - 包含实际应用场景
   - 提供最佳实践指导

**请提供详细的系列规划：**

1. **系列概述**
   - 系列的总体目标
   - 读者将获得的技能或知识
   - 预计的学习时间

2. **文章列表**
   - 每篇文章的标题
   - 主要内容概述（100-200字）
   - 难度级别（初级/中级/高级）
   - 预计字数

3. **学习路径**
   - 文章之间的关联关系
   - 前置知识要求
   - 实践项目建议

4. **补充资源**
   - 推荐的参考资料
   - 相关工具和库
   - 社区资源

请确保整个系列对{target_audience}具有实际价值和可操作性。"""


@app.list_tools()
async def list_tools() -> list[Tool]:
    """列出可用的 MCP 工具。"""
    logger.debug("正在列出工具...")

    # Post management tools
    post_tools = [
        Tool(
            name="list_my_posts",
            description="列出当前用户的所有文章，支持按发布状态、关键词和分类筛选",
            inputSchema={
                "type": "object",
                "properties": {
                    "page": {
                        "type": "number",
                        "description": "页码（默认：0）",
                        "default": 0,
                    },
                    "size": {
                        "type": "number",
                        "description": "每页数量（默认：20）",
                        "default": 20,
                    },
                    "publish_phase": {
                        "type": "string",
                        "description": "按发布状态筛选：DRAFT（草稿）、PENDING_APPROVAL（待审核）、PUBLISHED（已发布）、FAILED（失败）",
                        "enum": ["DRAFT", "PENDING_APPROVAL", "PUBLISHED", "FAILED"],
                    },
                    "keyword": {
                        "type": "string",
                        "description": "搜索关键词",
                    },
                    "category": {
                        "type": "string",
                        "description": "按分类名称筛选（包含子分类）",
                    },
                },
            },
        ),
        Tool(
            name="get_post",
            description="获取指定文章的详细信息，包括内容、元数据和设置",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "文章名称/标识符（必填）",
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="create_post",
            description="创建一篇新的博客文章，包括标题、内容、分类、标签等设置",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "文章标题（必填）",
                    },
                    "content": {
                        "type": "string",
                        "description": "文章内容，Markdown 格式（必填）",
                    },
                    "excerpt": {
                        "type": "string",
                        "description": "文章摘要/简介",
                    },
                    "slug": {
                        "type": "string",
                        "description": "URL 别名（不提供则自动生成）",
                    },
                    "categories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "分类名称列表",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "标签名称列表",
                    },
                    "cover": {
                        "type": "string",
                        "description": "封面图片 URL",
                    },
                    "allow_comment": {
                        "type": "boolean",
                        "description": "是否允许评论（默认：true）",
                        "default": True,
                    },
                    "pinned": {
                        "type": "boolean",
                        "description": "是否置顶（默认：false）",
                        "default": False,
                    },
                    "visible": {
                        "type": "string",
                        "description": "可见性：PUBLIC（公开）或 PRIVATE（私密），默认：PUBLIC",
                        "enum": ["PUBLIC", "PRIVATE"],
                        "default": "PUBLIC",
                    },
                    "publish_immediately": {
                        "type": "boolean",
                        "description": "创建后立即发布（默认：false）",
                        "default": False,
                    },
                },
                "required": ["title", "content"],
            },
        ),
        Tool(
            name="update_post",
            description="更新现有文章的标题、内容、分类、标签或其他设置",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "文章名称/标识符（必填）",
                    },
                    "title": {
                        "type": "string",
                        "description": "新标题",
                    },
                    "content": {
                        "type": "string",
                        "description": "新内容，Markdown 格式",
                    },
                    "excerpt": {
                        "type": "string",
                        "description": "新摘要",
                    },
                    "categories": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "新分类名称列表",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "新标签名称列表",
                    },
                    "cover": {
                        "type": "string",
                        "description": "新封面图片 URL",
                    },
                    "allow_comment": {
                        "type": "boolean",
                        "description": "是否允许评论",
                    },
                    "pinned": {
                        "type": "boolean",
                        "description": "是否置顶",
                    },
                    "visible": {
                        "type": "string",
                        "description": "可见性：PUBLIC（公开）或 PRIVATE（私密）",
                        "enum": ["PUBLIC", "PRIVATE"],
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="publish_post",
            description="发布草稿文章，使其公开可见",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "文章名称/标识符（必填）",
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="unpublish_post",
            description="取消发布文章，使其转换回草稿状态",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "文章名称/标识符（必填）",
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="delete_post",
            description="删除文章（移至回收站）",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "文章名称/标识符（必填）",
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="get_post_draft",
            description="获取文章的草稿版本及可编辑内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "文章名称/标识符（必填）",
                    },
                    "include_patched": {
                        "type": "boolean",
                        "description": "是否包含补丁内容（默认：false）",
                        "default": False,
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="update_post_draft",
            description="更新文章的草稿内容，不会发布",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "文章名称/标识符（必填）",
                    },
                    "content": {
                        "type": "string",
                        "description": "草稿内容，Markdown 格式（必填）",
                    },
                },
                "required": ["name", "content"],
            },
        ),
    ]

    # Combine all tools
    all_tools = POST_TOOLS + CATEGORY_TOOLS + TAG_TOOLS + ATTACHMENT_TOOLS + SITE_TOOLS

    logger.info(f"Registered {len(all_tools)} tools")
    return all_tools


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> list[Any]:
    """处理工具执行。"""
    logger.info(f"执行工具：{name}")
    logger.debug(f"参数：{arguments}")

    try:
        client = await get_halo_client()

        # Route to appropriate tool handler
        if name == "list_my_posts":
            result = await list_my_posts_tool(client, arguments)
        elif name == "get_post":
            result = await get_post_tool(client, arguments)
        elif name == "create_post":
            result = await create_post_tool(client, arguments)
        elif name == "update_post":
            result = await update_post_tool(client, arguments)
        elif name == "publish_post":
            result = await publish_post_tool(client, arguments)
        elif name == "unpublish_post":
            result = await unpublish_post_tool(client, arguments)
        elif name == "delete_post":
            result = await delete_post_tool(client, arguments)
        elif name == "get_post_draft":
            result = await get_post_draft_tool(client, arguments)
        elif name == "update_post_draft":
            result = await update_post_draft_tool(client, arguments)
        # Category tools
        elif name == "list_categories":
            from .tools.category_tools import list_categories_tool

            result = await list_categories_tool(client, arguments)
        elif name == "get_category":
            from .tools.category_tools import get_category_tool

            result = await get_category_tool(client, arguments)
        elif name == "create_category":
            from .tools.category_tools import create_category_tool

            result = await create_category_tool(client, arguments)
        elif name == "update_category":
            from .tools.category_tools import update_category_tool

            result = await update_category_tool(client, arguments)
        elif name == "delete_category":
            from .tools.category_tools import delete_category_tool

            result = await delete_category_tool(client, arguments)
        elif name == "get_category_posts":
            from .tools.category_tools import get_posts_under_category_tool

            result = await get_posts_under_category_tool(client, arguments)
        # Tag tools
        elif name == "list_tags":
            from .tools.tag_tools import list_tags_tool

            result = await list_tags_tool(client, arguments)
        elif name == "get_tag":
            from .tools.tag_tools import get_tag_tool

            result = await get_tag_tool(client, arguments)
        elif name == "create_tag":
            from .tools.tag_tools import create_tag_tool

            result = await create_tag_tool(client, arguments)
        elif name == "update_tag":
            from .tools.tag_tools import update_tag_tool

            result = await update_tag_tool(client, arguments)
        elif name == "delete_tag":
            from .tools.tag_tools import delete_tag_tool

            result = await delete_tag_tool(client, arguments)
        elif name == "get_tag_posts":
            from .tools.tag_tools import get_posts_under_tag_tool

            result = await get_posts_under_tag_tool(client, arguments)
        elif name == "list_console_tags":
            from .tools.tag_tools import list_console_tags_tool

            result = await list_console_tags_tool(client, arguments)
        # Attachment tools
        elif name == "list_attachments":
            from .tools.attachment_tools import list_attachments_tool

            result = await list_attachments_tool(client, arguments)
        elif name == "get_attachment":
            from .tools.attachment_tools import get_attachment_tool

            result = await get_attachment_tool(client, arguments)
        elif name == "upload_attachment":
            from .tools.attachment_tools import upload_attachment_tool

            result = await upload_attachment_tool(client, arguments)
        elif name == "upload_attachment_from_url":
            from .tools.attachment_tools import upload_attachment_from_url_tool

            result = await upload_attachment_from_url_tool(client, arguments)
        elif name == "delete_attachment":
            from .tools.attachment_tools import delete_attachment_tool

            result = await delete_attachment_tool(client, arguments)
        elif name == "list_attachment_groups":
            from .tools.attachment_tools import list_attachment_groups_tool

            result = await list_attachment_groups_tool(client, arguments)
        elif name == "create_attachment_group":
            from .tools.attachment_tools import create_attachment_group_tool

            result = await create_attachment_group_tool(client, arguments)
        elif name == "get_attachment_policies":
            from .tools.attachment_tools import list_storage_policies_tool

            result = await list_storage_policies_tool(client, arguments)
        # Site tools
        elif name == "get_halo_base_url":
            from .tools.site_tools import get_halo_base_url_tool

            result = await get_halo_base_url_tool(client, arguments)
        else:
            return [{"type": "text", "text": f"Unknown tool: {name}"}]

        logger.info(f"Tool {name} executed successfully")
        return [{"type": "text", "text": result}]

    except Exception as e:
        logger.error(f"Error executing {name}: {e}", exc_info=True)
        error_result = ToolResult.error_result(f"Error executing {name}: {str(e)}")
        return [{"type": "text", "text": error_result.model_dump_json()}]


async def run_server() -> None:
    """使用 stdio 传输运行 MCP 服务器。"""
    logger.info("使用 stdio 传输启动 MCP 服务器...")

    async with stdio_server() as (read_stream, write_stream):
        logger.info("服务器已就绪，正在等待请求...")
        await app.run(read_stream, write_stream, app.create_initialization_options())


# 导出 server 实例供测试使用
server = app


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_server())

# Claude Code 模型切换配置

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
dotenv_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path)

# 供应商列表
# base_url 必须与 Claude Code 兼容
PROVIDERS = [
    {
        "id": "anthropic",
        "name": "Anthropic (官方)",
        "base_url": "https://api.anthropic.com",
        "api_key": os.getenv("ANTHROPIC_API_KEY", ""),
        "icon": "anthropic",
        "icon_color": "#d4a574",
        "models": [
            {"id": "claude-opus-4-5-20251101", "name": "Claude Opus 4", "description": "最强大"},
            {"id": "claude-sonnet-4-20250514", "name": "Claude Sonnet 4", "description": "均衡"},
            {"id": "claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet", "description": "上代旗舰"},
            {"id": "claude-3-5-haiku-20241022", "name": "Claude 3.5 Haiku", "description": "快速高效"},
        ]
    },
    {
        "id": "deepseek",
        "name": "DeepSeek",
        "base_url": "https://api.deepseek.com/anthropic",
        "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
        "icon": "deepseek",
        "icon_color": "#3b82f6",
        "models": [
            {"id": "deepseek-chat", "name": "DeepSeek Chat", "description": "通用对话"},
            {"id": "deepseek-coder", "name": "DeepSeek Coder", "description": "编程专用"},
        ]
    },
    {
        "id": "minimax",
        "name": "MiniMax",
        "base_url": "https://api.minimaxi.com/anthropic",
        "api_key": os.getenv("MINIMAX_API_KEY", ""),
        "icon": "minimax",
        "icon_color": "#22c55e",
        "models": [
            {"id": "MiniMax-M2.7", "name": "MiniMax M2.7", "description": "最新模型"},
            {"id": "MiniMax-M2", "name": "MiniMax M2", "description": "上代模型"},
        ]
    },
]

# 默认供应商
DEFAULT_PROVIDER = "minimax"  # 根据你当前的配置
DEFAULT_MODEL = "MiniMax-M2.7"  # 根据你当前的配置

# Claude Code 配置路径
CLAUDE_CONFIG_PATH = "~/.claude/settings.json"

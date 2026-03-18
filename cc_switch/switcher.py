"""
Claude Code 模型切换器
严格匹配 ~/.claude/settings.json 的实际结构
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

# Claude Code 配置路径
def get_claude_config_path() -> Path:
    """获取 Claude Code 配置目录"""
    home = Path.home()
    return home / ".claude" / "settings.json"


def get_claude_config_dir() -> Path:
    """获取 Claude Code 配置目录"""
    home = Path.home()
    return home / ".claude"


def read_settings() -> dict:
    """读取 Claude Code 设置"""
    config_path = get_claude_config_path()

    if not config_path.exists():
        raise FileNotFoundError(f"Claude Code 配置文件未找到: {config_path}")

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_settings(settings: dict) -> None:
    """写入 Claude Code 设置"""
    config_path = get_claude_config_path()
    config_dir = get_claude_config_dir()

    # 确保目录存在
    config_dir.mkdir(parents=True, exist_ok=True)

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)


def get_current_config(settings: Optional[dict] = None) -> Dict[str, Any]:
    """
    获取当前配置（从 env 中提取）

    Returns:
        包含 provider_id, model_id, base_url 等信息的字典
    """
    if settings is None:
        settings = read_settings()

    env = settings.get('env', {})

    # 从 ANTHROPIC_BASE_URL 推断供应商
    base_url = env.get('ANTHROPIC_BASE_URL', '')
    if 'minimaxi' in base_url.lower():
        provider_id = 'minimax'
    elif 'deepseek' in base_url.lower():
        provider_id = 'deepseek'
    elif 'anthropic.com' in base_url.lower():
        provider_id = 'anthropic'
    else:
        provider_id = 'unknown'

    return {
        'provider_id': provider_id,
        'model_id': env.get('ANTHROPIC_MODEL', 'unknown'),
        'base_url': base_url,
        'api_key': env.get('ANTHROPIC_AUTH_TOKEN', ''),
    }


def get_current_model(settings: Optional[dict] = None) -> str:
    """获取当前使用的模型"""
    config = get_current_config(settings)
    return config.get('model_id', 'unknown')


def get_current_provider(settings: Optional[dict] = None) -> str:
    """获取当前供应商 ID"""
    config = get_current_config(settings)
    return config.get('provider_id', 'unknown')


def set_provider_and_model(
    provider_id: str,
    model_id: str,
    base_url: str = "",
    api_key: str = "",
    settings: Optional[dict] = None
) -> dict:
    """
    设置供应商和模型

    Args:
        provider_id: 供应商 ID
        model_id: 模型 ID
        base_url: API 端点
        api_key: API Key
        settings: 现有设置（可选）

    Returns:
        更新后的设置字典
    """
    if settings is None:
        settings = read_settings()

    # 确保 env 存在
    if 'env' not in settings:
        settings['env'] = {}

    env = settings['env']

    # 设置模型
    env['ANTHROPIC_MODEL'] = model_id

    # 设置供应商相关的环境变量
    if provider_id == 'minimax':
        env['ANTHROPIC_BASE_URL'] = 'https://api.minimaxi.com/anthropic'
        env['ANTHROPIC_DEFAULT_HAIKU_MODEL'] = model_id
        env['ANTHROPIC_DEFAULT_OPUS_MODEL'] = model_id
        env['ANTHROPIC_DEFAULT_SONNET_MODEL'] = model_id
        env['ANTHROPIC_REASONING_MODEL'] = model_id
    elif provider_id == 'deepseek':
        env['ANTHROPIC_BASE_URL'] = 'https://api.deepseek.com/anthropic'
    elif provider_id == 'anthropic':
        env['ANTHROPIC_BASE_URL'] = 'https://api.anthropic.com'
    else:
        # 如果是自定义 base_url
        if base_url:
            env['ANTHROPIC_BASE_URL'] = base_url

    # 设置 API Key（如果有）
    if api_key:
        env['ANTHROPIC_AUTH_TOKEN'] = api_key

    return settings


def set_model_only(model_id: str, settings: Optional[dict] = None) -> dict:
    """
    仅设置模型（不改变供应商）

    Args:
        model_id: 模型 ID
        settings: 现有设置（可选）

    Returns:
        更新后的设置字典
    """
    if settings is None:
        settings = read_settings()

    if 'env' not in settings:
        settings['env'] = {}

    settings['env']['ANTHROPIC_MODEL'] = model_id

    # 同时更新其他模型相关的默认设置
    settings['env']['ANTHROPIC_DEFAULT_HAIKU_MODEL'] = model_id
    settings['env']['ANTHROPIC_DEFAULT_OPUS_MODEL'] = model_id
    settings['env']['ANTHROPIC_DEFAULT_SONNET_MODEL'] = model_id
    settings['env']['ANTHROPIC_REASONING_MODEL'] = model_id

    return settings


def is_config_exists() -> bool:
    """检查 Claude Code 配置是否存在"""
    config_path = get_claude_config_path()
    return config_path.exists()
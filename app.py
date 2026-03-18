"""
WSL2 Claude Code 模型切换 GUI - Flask 后端
支持多供应商切换
"""

import argparse
from flask import Flask, jsonify, render_template, request
from cc_switch.switcher import (
    get_current_model,
    get_current_provider,
    get_current_config,
    set_provider_and_model,
    set_model_only,
    is_config_exists,
    read_settings,
    write_settings,
    get_claude_config_path,
)
from config import PROVIDERS, DEFAULT_PROVIDER, DEFAULT_MODEL

app = Flask(__name__)


@app.route('/')
def index():
    """渲染主页面"""
    return render_template('index.html')


@app.route('/health')
def health():
    """健康检查"""
    return jsonify({"status": "ok"})


@app.route('/api/providers', methods=['GET'])
def get_providers():
    """获取供应商列表（不包含 API Key）"""
    # 移除 API Key 后再返回
    safe_providers = []
    for p in PROVIDERS:
        safe_providers.append({
            "id": p["id"],
            "name": p["name"],
            "base_url": p.get("base_url", ""),
            "icon": p.get("icon", ""),
            "icon_color": p.get("icon_color", ""),
            "models": p.get("models", []),
            "has_api_key": bool(p.get("api_key", "")),
        })
    return jsonify({
        "providers": safe_providers
    })


@app.route('/api/current', methods=['GET'])
def get_current():
    """获取当前供应商和模型"""
    try:
        if not is_config_exists():
            return jsonify({
                "error": "Claude Code 配置文件未找到",
                "config_path": str(get_claude_config_path()),
                "provider_id": None,
                "model_id": None
            }), 404

        current = get_current_config()
        return jsonify({
            "provider_id": current.get('provider_id'),
            "model_id": current.get('model_id'),
            "base_url": current.get('base_url'),
            "config_path": str(get_claude_config_path())
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "provider_id": None,
            "model_id": None
        }), 500


@app.route('/api/switch', methods=['POST'])
def switch_model():
    """切换供应商和/或模型"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "请求体不能为空"}), 400

    provider_id = data.get('provider_id')
    model_id = data.get('model_id')

    if not provider_id and not model_id:
        return jsonify({"error": "至少需要提供 provider_id 或 model_id"}), 400

    try:
        if not is_config_exists():
            return jsonify({
                "error": "Claude Code 配置文件未找到",
                "config_path": str(get_claude_config_path())
            }), 404

        # 验证供应商
        provider_info = None
        if provider_id:
            provider_info = next((p for p in PROVIDERS if p['id'] == provider_id), None)
            if not provider_info:
                return jsonify({
                    "error": f"无效的供应商 ID: {provider_id}",
                    "valid_providers": [p['id'] for p in PROVIDERS]
                }), 400

        # 验证模型
        if model_id and provider_info:
            valid_models = [m['id'] for m in provider_info['models']]
            if model_id not in valid_models:
                return jsonify({
                    "error": f"无效的模型 ID: {model_id}",
                    "valid_models": valid_models
                }), 400

        # 读取当前配置
        settings = read_settings()

        if provider_id and model_id:
            # 完整切换供应商+模型
            base_url = provider_info.get('base_url', '')
            api_key = provider_info.get('api_key', '')
            settings = set_provider_and_model(
                provider_id, model_id, base_url=base_url, api_key=api_key, settings=settings
            )
        elif model_id:
            # 仅切换模型
            settings = set_model_only(model_id, settings)
        elif provider_id:
            # 仅切换供应商（保留当前模型或用默认）
            current_model = get_current_model(settings)
            # 检查当前模型是否在新供应商的模型列表中
            if provider_info:
                valid_models = [m['id'] for m in provider_info['models']]
                if current_model not in valid_models:
                    current_model = provider_info['models'][0]['id']
            base_url = provider_info.get('base_url', '') if provider_info else ''
            api_key = provider_info.get('api_key', '') if provider_info else ''
            settings = set_provider_and_model(
                provider_id, current_model, base_url=base_url, api_key=api_key, settings=settings
            )

        # 写入配置
        write_settings(settings)

        return jsonify({
            "success": True,
            "provider_id": provider_id,
            "model_id": model_id,
            "message": f"已切换到 {provider_id}/{model_id}"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route('/api/config_status', methods=['GET'])
def config_status():
    """获取配置状态"""
    return jsonify({
        "exists": is_config_exists(),
        "config_path": str(get_claude_config_path())
    })


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Claude Code Model Switch GUI')
    parser.add_argument('-H', '--host', default='127.0.0.1',
                        help='监听地址 (默认: 127.0.0.1)')
    parser.add_argument('-p', '--port', type=int, default=5000,
                        help='监听端口 (默认: 5000)')
    args = parser.parse_args()

    print(f"启动 Claude Code 模型切换 GUI...")
    print(f"访问 http://{args.host}:{args.port} 使用界面")
    print(f"按 Ctrl+C 停止服务器")

    app.run(host=args.host, port=args.port, debug=True)
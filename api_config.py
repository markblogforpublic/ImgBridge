"""
API 配置共享模块 - 自动检测 OpenAI / Anthropic 格式
====================================================
所有识别脚本共用此模块，配置保存在 config.json 中。
"""

import json, os, base64, re
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.json"

DEFAULT_CONFIG = {
    "api_endpoint": "",
    "api_key": "",
    "model": ""
}

MIME_MAP = {'.jpg':'image/jpeg','.jpeg':'image/jpeg','.jfif':'image/jpeg','.jpe':'image/jpeg','.png':'image/png','.webp':'image/webp','.gif':'image/gif','.bmp':'image/bmp'}


def detect_format(endpoint):
    """自动判断 API 格式（openai / anthropic）"""
    ep = endpoint.lower()
    if '/compatible-mode/' in ep or '/chat/completions' in ep:
        return "openai"
    elif 'anthropic' in ep or '/messages' in ep:
        return "anthropic"
    return "openai"


def load_config():
    """加载配置，不存在则用默认值自动创建"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
            # 补全缺失字段
            for k, v in DEFAULT_CONFIG.items():
                cfg.setdefault(k, v)
            return cfg
    # 自动创建默认配置
    cfg = dict(DEFAULT_CONFIG)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    print(f"  📝 已创建默认配置: {CONFIG_FILE}")
    return cfg


def call_vision_api(image_path, prompt=None, config=None):
    """
    调用视觉 API，自动尝试 OpenAI → Anthropic 两种格式
    """
    import requests
    if config is None:
        config = load_config()
    if not prompt:
        prompt = "请详细描述这张图片的内容，包括物体、人物、场景、文字、颜色、布局等所有可见信息。如果是文档或截图，请提取其中的文字内容。"

    ext = os.path.splitext(image_path)[1].lower()
    mime = MIME_MAP.get(ext, 'image/png')
    with open(image_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()

    headers = {"Authorization": f"Bearer {config['api_key']}", "Content-Type": "application/json"}
    base_ep = config['api_endpoint'].rstrip('/')

    # OpenAI 格式（首选）
    openai_ep = base_ep
    if not openai_ep.endswith('/chat/completions'):
        openai_ep = openai_ep.rstrip('/v1') + '/v1/chat/completions'

    openai_payload = {
        "model": config['model'],
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}
        ]}],
        "max_tokens": 4096, "temperature": 0.7
    }

    try:
        resp = requests.post(openai_ep, headers=headers, json=openai_payload, timeout=120)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
    except Exception:
        pass

    # Anthropic 格式（备选）
    anth_ep = base_ep
    if not anth_ep.endswith('/messages'):
        anth_ep = anth_ep.rstrip('/v1') + '/v1/messages'

    anth_headers = {**headers, "x-api-key": config['api_key'], "anthropic-version": "2023-06-01"}
    anth_payload = {
        "model": config['model'], "max_tokens": 4096,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image", "source": {"type": "base64", "media_type": mime, "data": b64}}
        ]}]
    }

    try:
        resp = requests.post(anth_ep, headers=anth_headers, json=anth_payload, timeout=120)
        if resp.status_code == 200:
            texts = [b.get("text","") for b in resp.json().get("content",[]) if b.get("type")=="text"]
            return "\n".join(texts) if texts else str(resp.json())
    except Exception:
        pass

    return f"❌ API 调用失败，已尝试 OpenAI 和 Anthropic 两种格式"

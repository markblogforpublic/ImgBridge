"""
Vision MCP Server - 为 Claude 提供图片识别能力
==============================================
让 Claude 直接调用视觉 API 识别图片，无需打开浏览器。

安装依赖: pip install mcp requests
配置: 首次使用会自动创建 config.json，填写 API 信息即可

启动方式:
  python vision_mcp_server.py

然后 Claude Code 连接:
  claude --mcp vision_mcp_server.py
  或在 CLAUDE.md 中配置 mcpServers
"""

import sys
import os
import json
import threading
import base64
import http.server
import re
import time
from pathlib import Path

# 确保能找到同目录的 api_config
sys.path.insert(0, str(Path(__file__).parent))
import api_config

from mcp.server.fastmcp import FastMCP

# 创建 MCP Server
mcp = FastMCP("Vision Recognizer", instructions="图片识别工具 - 调用视觉 API 分析图片内容")

CONFIG = api_config.load_config()
SAVE_DIR = Path(__file__).parent
UPLOAD_PORT = 8766


@mcp.tool(
    name="analyze_image",
    description="分析一张图片的内容，返回详细的文字描述。支持 JPG/PNG/WebP/GIF/BMP 等格式。"
)
def analyze_image(image_path: str, prompt: str = None) -> str:
    """
    分析指定路径的图片，返回视觉模型识别结果。

    Args:
        image_path: 图片文件的完整路径（支持绝对路径）
        prompt: 可选，自定义分析提示词，默认详细描述图片内容

    Returns:
        图片的详细文字描述
    """
    img_file = Path(image_path)
    if not img_file.exists():
        return f"❌ 找不到图片文件: {image_path}"

    # 检查格式
    SUPPORTED = {'.jpg','.jpeg','.jfif','.jpe','.png','.webp','.gif','.bmp'}
    if img_file.suffix.lower() not in SUPPORTED:
        return f"❌ 不支持的格式: {img_file.suffix}\n支持: {', '.join(sorted(SUPPORTED))}"

    # 检查大小
    size_mb = img_file.stat().st_size / (1024 * 1024)
    if size_mb > 20:
        return f"❌ 图片过大 ({size_mb:.1f}MB)，请压缩至 20MB 以下"

    print(f"  🔍 识别: {img_file.name} ({size_mb:.1f}MB)", file=sys.stderr)

    # 详细诊断信息
    print(f"  [debug] CONFIG keys: {list(CONFIG.keys())}", file=sys.stderr)
    print(f"  [debug] model: {CONFIG.get('model','?')}", file=sys.stderr)
    print(f"  [debug] endpoint: {CONFIG.get('api_endpoint','?')[:60]}...", file=sys.stderr)

    try:
        result = api_config.call_vision_api(str(img_file), prompt, config=CONFIG)
    except Exception as e:
        import traceback
        result = f"❌ 代码异常: {e}\n{traceback.format_exc()}"

    print(f"  ✅ 识别完成", file=sys.stderr)
    return result


@mcp.tool(
    name="batch_analyze_images",
    description="批量分析多张图片，每张返回详细的文字描述。传入图片路径数组。"
)
def batch_analyze_images(image_paths: list) -> str:
    """
    批量分析多张图片。

    Args:
        image_paths: 图片文件路径列表，如 ["/path/to/img1.jpg", "/path/to/img2.png"]

    Returns:
        每张图片的分析结果汇总
    """
    results = []
    for i, path in enumerate(image_paths, 1):
        print(f"  📸 [{i}/{len(image_paths)}] 识别中...", file=sys.stderr)
        result = analyze_image(path)
        results.append(f"=== 图片 {i}: {Path(path).name} ===\n{result}")

    return "\n\n".join(results)


@mcp.tool(
    name="check_config",
    description="查看当前的 API 配置状态（不会暴露完整 Key）"
)
def check_config() -> str:
    """查看 API 配置是否就绪"""
    cfg = api_config.load_config()
    key = cfg.get('api_key', '')
    endpoint = cfg.get('api_endpoint', '')
    model = cfg.get('model', '')

    if not key or not endpoint or not model:
        return ("⚠️ API 未配置！请在项目文件夹的 config.json 中填写：\n"
                "  - api_endpoint: API 地址\n"
                "  - api_key: API Key\n"
                "  - model: 模型名称\n"
                "或在浏览器中打开 http://localhost:8765 配置")

    key_masked = key[:6] + '...' + key[-4:] if len(key) > 12 else key[:4] + '...'
    return (f"✅ API 已配置\n"
            f"  端点: {endpoint}\n"
            f"  模型: {model}\n"
            f"  Key:  {key_masked}")


# ===== HTTP 上传服务（供对话附件使用） =====
_uploaded_file = threading.Event()
_upload_data = {}

class UploadHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        html = """<!DOCTYPE html><html><meta charset="utf-8"><title>上传图片到MCP</title>
<style>body{font-family:sans-serif;max-width:600px;margin:50px auto;padding:20px;text-align:center}
.z{border:3px dashed #4A90D9;border-radius:12px;padding:40px;margin:20px 0;cursor:pointer;background:#f8faff}
.z.dragover{background:#e0eeff}img{max-width:100%;max-height:300px;margin-top:15px;display:none}
button{padding:12px 30px;background:#4A90D9;color:#fff;border:none;border-radius:6px;font-size:16px;cursor:pointer}
.s{display:none;padding:10px;border-radius:6px;margin:10px 0}
.s.ok{display:block;background:#d4edda;color:#155724}
.s.err{display:block;background:#f8d7da;color:#721c24}
</style><body><h1>🖼️ 上传图片到 MCP</h1>
<div class="z" id="z"><div style="font-size:48px">📁</div><p style="font-size:18px">拖拽或点击选择图片</p>
<input type="file" id="f" accept="image/*"hidden></div><img id="p"><br>
<button onclick="up()">🚀 上传并识别</button><div id="s" class="s"></div>
<script>
const z=document.getElementById('z'),f=document.getElementById('f'),p=document.getElementById('p'),st=document.getElementById('s');let sel=null
z.onclick=()=>f.click();z.ondragover=e=>{e.preventDefault();z.classList.add('dragover')}
z.ondragleave=()=>z.classList.remove('dragover')
z.ondrop=e=>{e.preventDefault();z.classList.remove('dragover');h(e.dataTransfer.files[0])}
f.onchange=()=>h(f.files[0])
function h(fi){if(!fi||!fi.type.startsWith('image/'))return;sel=fi
const r=new FileReader();r.onload=e=>{p.src=e.target.result;p.style.display='block'}
r.readAsDataURL(fi);z.querySelector('p').textContent=fi.name;st.className='s'}
async function up(){if(!sel)return
const b=document.querySelector('button');b.disabled=true;b.textContent='⏳'
st.className='s';const fd=new FormData();fd.append('image',sel)
try{const r=await fetch('/upload',{method:'POST',body:fd});const j=await r.json()
if(j.success){st.className='s ok';st.innerHTML='✅ 成功！回到 Claude 查看结果'}
else{st.className='s err';st.textContent='❌ '+j.error}}
catch(e){st.className='s err';st.textContent='❌ '+e.message}
finally{b.disabled=false;b.textContent='🚀 上传'}}
</script></body></html>"""
        self.send_response(200)
        self.send_header('Content-Type','text/html;charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode())

    def _parse_multipart(self):
        """手动解析 multipart/form-data，兼容 Python 3.13+（cgi 已移除）"""
        ct = self.headers.get('Content-Type', '')
        m = re.search(r'boundary=([^;\s]+)', ct)
        if not m: return {}
        boundary = m.group(1).encode()
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        result = {}
        for part in body.split(b'--' + boundary):
            if part.strip() in (b'', b'--', b'\r\n--'): continue
            header_end = part.find(b'\r\n\r\n')
            if header_end == -1: continue
            headers_raw = part[:header_end].decode('utf-8', errors='replace')
            content = part[header_end + 4:]
            if content.endswith(b'\r\n'): content = content[:-2]
            name_m = re.search(r'name="([^"]*)"', headers_raw)
            fn_m = re.search(r'filename="([^"]*)"', headers_raw)
            name = name_m.group(1) if name_m else None
            if fn_m and name:
                result[name] = {'filename': fn_m.group(1), 'data': content}
            elif name:
                result[name] = content.decode('utf-8', errors='replace')
        return result

    def do_POST(self):
        try:
            form = self._parse_multipart()
            item = form.get('image')
            if not item:
                self._r(False, error='未找到图片文件'); return
            fn = item['filename'] or 'uploaded.png'
            data = item['data']
            ext = os.path.splitext(fn)[1].lower()
            sup = {'.jpg','.jpeg','.jfif','.jpe','.png','.webp','.gif','.bmp'}
            if ext not in sup:
                self._r(False,error='不支持格式'); return
            dst = SAVE_DIR / fn
            c = 1
            while dst.exists():
                s = Path(fn).stem; dst = SAVE_DIR / f"{s}_{c}{ext}"; c += 1
            with open(dst,'wb') as f: f.write(data)
            _upload_data['path'] = str(dst); _upload_data['name'] = dst.name
            _uploaded_file.set()
            self._r(True,filename=dst.name)
        except Exception as e:
            self._r(False,error=str(e))

    def _r(self,s,**kw):
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps({'success':s,**kw}).encode())

    def log_message(self,f,*a): pass


@mcp.tool(
    name="analyze_uploaded_image",
    description="启动一个临时网页让用户上传图片，上传后自动识别。适用于用户想在对话中上传图片的场景。"
)
def analyze_uploaded_image(timeout_seconds: int = 60) -> str:
    """
    启动临时上传页面，用户通过浏览器上传图片后自动识别。

    Args:
        timeout_seconds: 等待上传的超时时间（秒），默认60秒

    Returns:
        上传状态和识别结果
    """
    global _uploaded_file, _upload_data
    _uploaded_file.clear()
    _upload_data.clear()

    # 启动 HTTP 服务
    server = http.server.HTTPServer(('0.0.0.0', UPLOAD_PORT), UploadHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()

    url = f"http://localhost:{UPLOAD_PORT}"
    result = f"📸 请在浏览器中打开此地址上传图片：\n{url}\n\n等待上传中..."

    if _uploaded_file.wait(timeout=timeout_seconds):
        path = _upload_data['path']
        name = _upload_data['name']
        size_kb = os.path.getsize(path) / 1024
        result = f"✅ 已收到图片: {name} ({size_kb:.1f}KB)\n⏳ 正在识别..."
        analysis = api_config.call_vision_api(path, config=CONFIG)
        result += f"\n\n📋 识别结果：\n\n{analysis}"
    else:
        result = "⏰ 等待超时，用户未上传图片"

    server.shutdown()
    return result


@mcp.tool(
    name="analyze_image_dialog",
    description="打开 Windows 文件选择对话框，用户选图后自动识别。Cowork 模式下传图的最佳方式。"
)
def analyze_image_dialog() -> str:
    """
    弹出文件选择对话框，用户选择图片后自动识别。
    无需手动输入路径，Cowork 模式下最方便。
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        path = filedialog.askopenfilename(
            title="选择要识别的图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.webp *.gif *.bmp"),
                       ("所有文件", "*.*")]
        )
        root.destroy()

        if not path:
            return "❌ 已取消选择"

        from pathlib import Path
        p = Path(path)
        if not p.exists():
            return f"❌ 找不到文件: {path}"

        print(f"  📸 用户选择了: {p.name}", file=sys.stderr)
        result = api_config.call_vision_api(str(p), config=CONFIG)
        return f"✅ 图片: {p.name}\n\n📋 识别结果：\n\n{result}"

    except ImportError:
        return "❌ 需要 tkinter 支持（Windows Python 自带）"
    except Exception as e:
        return f"❌ 出错: {str(e)}"


if __name__ == "__main__":
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"  👁️  Vision MCP Server", file=sys.stderr)
    print(f"  📁 工作目录: {SAVE_DIR}", file=sys.stderr)
    print(f"  🔌 使用 stdio 传输", file=sys.stderr)
    print(f"{'='*50}\n", file=sys.stderr)

    # 检查配置
    cfg = api_config.load_config()
    if not cfg.get('api_key') or not cfg.get('api_endpoint'):
        print(f"  ⚠️  首次使用请先配置 API", file=sys.stderr)
        print(f"  📝 编辑 {SAVE_DIR}/config.json 填写后重启", file=sys.stderr)
        print(f"", file=sys.stderr)

    mcp.run(transport="stdio")

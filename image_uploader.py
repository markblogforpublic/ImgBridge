"""
图片上传识别工具 - 本地运行版
================================
支持多张图片同时上传，自动调用识别。
配置保存在 config.json 中，自动适配 API 格式。
结果自动同步到 Claude（回到对话即可查看）。
"""

import http.server
import os
import json
import sys
import threading
import webbrowser
import re
from pathlib import Path

# ===== 使用共享配置 =====
sys.path.insert(0, str(Path(__file__).parent))
import api_config

SAVE_DIR = Path(__file__).parent
PORT = 8765
CONFIG = api_config.load_config()
MODEL = CONFIG['model']

SUPPORTED_EXT = {'.jpg','.jpeg','.jfif','.jpe','.png','.webp','.gif','.bmp','.dib','.tiff','.tif','.svg','.ico','.heic','.heif','.avif'}

# 确认是否需要首次配置
NEED_SETUP = not CONFIG.get('api_key') or not CONFIG.get('api_endpoint') or not CONFIG.get('model')

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>图片批量识别</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
     background:linear-gradient(135deg,#f5f7fa 0%,#c3cfe2 100%);
     min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
.card{background:white;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,0.15);
      padding:40px;max-width:750px;width:100%;position:relative}
.card-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:5px}
.card-header h1{margin:0}
.settings-btn{background:none;border:none;font-size:24px;cursor:pointer;padding:4px 8px;border-radius:8px;transition:.2s;color:#888}
.settings-btn:hover{background:#f0f0f0;color:#333}
.sub{text-align:center;color:#888;margin-bottom:20px;font-size:14px}
.drop-zone{border:3px dashed #4A90D9;border-radius:16px;padding:40px 20px;text-align:center;
           cursor:pointer;background:#f8faff;transition:all 0.3s;position:relative}
.drop-zone:hover,.drop-zone.dragover{background:#e8f0fe;border-color:#2a6fc9;transform:scale(1.01)}
.drop-zone .icon{font-size:56px;margin-bottom:10px}
.drop-zone .hint{font-size:18px;color:#333;margin-bottom:5px}
.drop-zone .sub-hint{font-size:13px;color:#999}
.drop-zone input[type=file]{display:none}
.preview-area{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px;justify-content:center}
.preview-item{position:relative;width:100px;height:100px;border-radius:8px;overflow:hidden;border:2px solid #e0e0e0;background:#f5f5f5}
.preview-item img{width:100%;height:100%;object-fit:cover}
.preview-item .name{position:absolute;bottom:0;left:0;right:0;background:rgba(0,0,0,0.6);color:#fff;font-size:10px;padding:2px 4px;text-overflow:ellipsis;overflow:hidden;white-space:nowrap}
.btn-row{text-align:center;margin-top:20px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.btn{background:#4A90D9;color:#fff;border:none;padding:14px 40px;border-radius:10px;font-size:16px;cursor:pointer;transition:all 0.3s;font-weight:500}
.btn:hover{background:#357abd;transform:translateY(-2px);box-shadow:0 6px 20px rgba(74,144,217,0.4)}
.btn:disabled{background:#b0c4de;cursor:not-allowed;transform:none;box-shadow:none}
.btn-secondary{background:#6c757d;padding:10px 20px;font-size:14px}
.btn-secondary:hover{background:#5a6268}
.btn-success{background:#28a745}
.btn-success:hover{background:#218838}
#status{margin-top:20px;padding:15px 20px;border-radius:10px;display:none;font-size:14px;line-height:1.6;max-height:300px;overflow-y:auto}
#status.loading{display:block;background:#fff3cd;color:#856404}
#status.success{display:block;background:#d4edda;color:#155724}
#status.error{display:block;background:#f8d7da;color:#721c24}
#resultArea{display:none;margin-top:20px}
.result-card{background:#f8f9fa;border-radius:10px;padding:16px;margin-bottom:12px;border:1px solid #e9ecef}
.result-card .r-title{font-weight:600;color:#333;margin-bottom:6px;font-size:15px}
.result-card .r-body{font-size:13px;line-height:1.7;color:#555;white-space:pre-wrap;max-height:200px;overflow-y:auto}
.result-card .r-tag{display:inline-block;background:#4A90D9;color:#fff;font-size:11px;padding:2px 8px;border-radius:4px;margin-left:8px}
.file-count{text-align:center;margin-top:8px;font-size:14px;color:#888}
.progress-item{padding:6px 0;border-bottom:1px solid #eee}
.progress-item:last-child{border-bottom:none}

/* 设置弹窗 */
.modal-overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.4);z-index:1000;align-items:center;justify-content:center}
.modal-overlay.active{display:flex}
.modal{background:#fff;border-radius:16px;padding:30px;max-width:520px;width:90%;box-shadow:0 20px 60px rgba(0,0,0,0.3);max-height:90vh;overflow-y:auto}
.modal h2{margin-bottom:5px;color:#1a1a2e}
.modal .sub{text-align:left;margin-bottom:18px}
.form-group{margin-bottom:16px}
.form-group label{display:block;font-weight:500;margin-bottom:5px;color:#333;font-size:14px}
.form-group input{width:100%;padding:10px 14px;border:2px solid #e0e0e0;border-radius:8px;font-size:14px;transition:.2s;font-family:monospace}
.form-group input:focus{border-color:#4A90D9;outline:none}
.form-group .hint{font-size:12px;color:#999;margin-top:3px}
.modal-btns{display:flex;gap:10px;margin-top:20px;justify-content:flex-end}
.api-status{display:inline-block;padding:2px 10px;border-radius:4px;font-size:12px;margin-left:6px}
.api-status.openai{background:#d4edda;color:#155724}
.api-status.anthropic{background:#fff3cd;color:#856404}

/* 首次配置提示条 */
.setup-banner{display:none;background:#fff3cd;color:#856404;padding:12px 16px;border-radius:10px;margin-bottom:16px;font-size:14px;align-items:center;gap:10px}
.setup-banner.active{display:flex}
.setup-banner .btn{flex-shrink:0;padding:6px 16px;font-size:13px}
</style>
</head>
<body>
<div class="card">
  <div class="card-header">
    <h1>🖼️ 批量图片识别</h1>
    <button class="settings-btn" onclick="openSettings()" title="API 设置">⚙️</button>
  </div>
  <p class="sub">支持多张图片同时上传 · 调用视觉模型识别</p>

  <!-- 首次配置提示 -->
  <div class="setup-banner" id="setupBanner">
    <span>⚠️ 首次使用：请先配置 API 信息</span>
    <button class="btn btn-success" onclick="openSettings()">去配置</button>
  </div>

  <div class="drop-zone" id="dropZone">
    <div class="icon">📁</div>
    <div class="hint" id="hintText">拖拽图片到此处上传</div>
    <div class="sub-hint">或点击选择文件（支持多选）</div>
    <input type="file" id="fileInput" accept="image/*" multiple>
    <div class="preview-area" id="previewArea"></div>
  </div>

  <div class="file-count" id="fileCount"></div>

  <div class="btn-row">
    <button class="btn" id="uploadBtn" onclick="upload()">🚀 上传全部并识别</button>
    <button class="btn btn-secondary" onclick="clearAll()">清除</button>
  </div>

  <div id="status"></div>

  <div id="resultArea">
    <div style="font-weight:500;margin-bottom:12px;color:#333">📋 识别结果</div>
    <div id="resultCards"></div>
    <div class="result-actions" style="text-align:center;font-size:13px;color:#888;margin-top:8px">结果已保存到文件夹，同步到Claude</div>
  </div>
</div>

<!-- 设置弹窗 -->
<div class="modal-overlay" id="settingsModal">
  <div class="modal">
    <h2>⚙️ API 配置</h2>
    <p class="sub">配置视觉模型的 API 信息</p>

    <div class="form-group">
      <label>API 地址</label>
      <input type="text" id="cfgEndpoint" placeholder="https://api.example.com/v1/chat/completions">
      <div class="hint">支持 OpenAI 和 Anthropic 格式，自动检测</div>
    </div>

    <div class="form-group">
      <label>API Key</label>
      <input type="password" id="cfgKey" placeholder="sk-...">
      <div class="hint">你的 API 密钥</div>
    </div>

    <div class="form-group">
      <label>模型名称</label>
      <input type="text" id="cfgModel" placeholder="qwen3.6-plus">
      <div class="hint">例如: qwen3.6-plus, gpt-4o, claude-3-opus 等</div>
    </div>

    <div class="form-group" id="apiFormatDisplay" style="display:none">
      <label>检测到的 API 格式</label>
      <div id="apiFormatTag"></div>
    </div>

    <div class="modal-btns">
      <button class="btn btn-secondary" onclick="closeSettings()">取消</button>
      <button class="btn" onclick="saveConfig()">💾 保存配置</button>
      <button class="btn btn-success" onclick="testConfig()">🔍 测试连接</button>
    </div>
    <div id="configStatus" style="margin-top:12px;font-size:13px;display:none"></div>
  </div>
</div>

<script>
const dropZone=document.getElementById('dropZone');
const fileInput=document.getElementById('fileInput');
const hintText=document.getElementById('hintText');
const previewArea=document.getElementById('previewArea');
const fileCount=document.getElementById('fileCount');
const status=document.getElementById('status');
const resultArea=document.getElementById('resultArea');
const resultCards=document.getElementById('resultCards');
const uploadBtn=document.getElementById('uploadBtn');
const setupBanner=document.getElementById('setupBanner');
let selectedFiles=[];

dropZone.onclick=()=>fileInput.click();
dropZone.ondragover=e=>{e.preventDefault();dropZone.classList.add('dragover')};
dropZone.ondragleave=()=>dropZone.classList.remove('dragover');
dropZone.ondrop=e=>{e.preventDefault();dropZone.classList.remove('dragover');
    if(e.dataTransfer.files.length)addFiles(e.dataTransfer.files)};
fileInput.onchange=()=>{if(fileInput.files.length)addFiles(fileInput.files)};

function addFiles(files){
    for(let f of files){
        if(f.type.startsWith('image/')){
            if(!selectedFiles.find(x=>x.name===f.name&&x.size===f.size))selectedFiles.push(f);
        }
    }
    renderPreviews();
}
function renderPreviews(){
    previewArea.innerHTML='';
    selectedFiles.forEach((f,i)=>{
        const d=document.createElement('div');d.className='preview-item';
        const img=document.createElement('img');
        const r=new FileReader();r.onload=e=>{img.src=e.target.result};r.readAsDataURL(f);
        d.appendChild(img);
        const n=document.createElement('div');n.className='name';n.textContent=f.name;
        d.appendChild(n);
        d.onclick=()=>{selectedFiles.splice(i,1);renderPreviews()};d.title='点击移除';
        previewArea.appendChild(d);
    });
    const n=selectedFiles.length;
    if(n>0){
        hintText.textContent=`已选择 ${n} 张图片`;
        fileCount.textContent=`共 ${n} 张 (${(selectedFiles.reduce((s,f)=>s+f.size,0)/1024).toFixed(0)}KB) · 点击小图移除`;
    }else{hintText.textContent='拖拽图片到此处上传';fileCount.textContent=''}
    status.style.display='none';resultArea.style.display='none';
}

async function upload(){
    if(selectedFiles.length===0){alert('请先选择图片');return}
    uploadBtn.disabled=true;uploadBtn.innerHTML='<span class="loader"></span>识别中...';
    resultArea.style.display='none';resultCards.innerHTML='';
    for(let i=0;i<selectedFiles.length;i++){
        const file=selectedFiles[i];const fd=new FormData();fd.append('image',file);
        status.className='loading';status.style.display='block';
        status.innerHTML+=`<div class="progress-item">⏳ [${i+1}/${selectedFiles.length}] ${file.name} ...</div>`;
        status.scrollTop=status.scrollHeight;
        try{
            const r=await fetch('/upload',{method:'POST',body:fd});const d=await r.json();
            if(d.success){
                status.innerHTML+=`<div class="progress-item">✅ [${i+1}/${selectedFiles.length}] ${file.name} 完成</div>`;
                const c=document.createElement('div');c.className='result-card';
                c.innerHTML=`<div class="r-title">🖼️ ${file.name} <span class="r-tag">${(file.size/1024).toFixed(0)}KB</span></div><div class="r-body">${d.result}</div>`;
                resultCards.appendChild(c);resultArea.style.display='block';
            }else{status.innerHTML+=`<div class="progress-item">❌ [${i+1}/${selectedFiles.length}] ${file.name}: ${d.error}</div>`}
        }catch(e){status.innerHTML+=`<div class="progress-item">❌ [${i+1}/${selectedFiles.length}] ${file.name}: 连接失败</div>`}
        status.scrollTop=status.scrollHeight;
    }
    status.className='success';
    status.innerHTML+='<div style="margin-top:8px;font-weight:500">✅ 全部完成！结果已同步到Claude，返回聊天窗口查看</div>';
    uploadBtn.disabled=false;uploadBtn.textContent='🚀 上传全部并识别';
}

function clearAll(){
    selectedFiles=[];fileInput.value='';
    previewArea.innerHTML='';hintText.textContent='拖拽图片到此处上传';
    fileCount.textContent='';status.style.display='none';resultArea.style.display='none';
}

/* ===== 配置管理 ===== */
const setupBannerEl=document.getElementById('setupBanner');

async function loadConfig(){
    try{
        const r=await fetch('/api/config');const d=await r.json();
        if(d.success){
            document.getElementById('cfgEndpoint').value=d.config.api_endpoint||'';
            document.getElementById('cfgKey').value=d.config.api_key||'';
            document.getElementById('cfgModel').value=d.config.model||'';
            const fmt=d.config.api_format||'openai';
            const tag=document.getElementById('apiFormatTag');
            tag.innerHTML=`<span class="api-status ${fmt}">${fmt.toUpperCase()}</span>`;
            document.getElementById('apiFormatDisplay').style.display='block';
            // 显示/隐藏首次配置提示
            if(d.needs_setup){
                setupBannerEl.classList.add('active');
            }else{
                setupBannerEl.classList.remove('active');
            }
        }
    }catch(e){console.log('load config error',e)}
}

function openSettings(){document.getElementById('settingsModal').classList.add('active');loadConfig()}
function closeSettings(){document.getElementById('settingsModal').classList.remove('active')}

async function saveConfig(){
    const cfg={api_endpoint:document.getElementById('cfgEndpoint').value.trim(),
               api_key:document.getElementById('cfgKey').value.trim(),
               model:document.getElementById('cfgModel').value.trim()};
    if(!cfg.api_endpoint||!cfg.api_key||!cfg.model){alert('请填写完整配置');return}
    try{
        const r=await fetch('/api/config',{method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify(cfg)});
        const d=await r.json();
        const cs=document.getElementById('configStatus');
        if(d.success){
            cs.style.display='block';cs.style.color='#155724';cs.textContent='✅ 配置已保存！';
            const tag=document.getElementById('apiFormatTag');
            tag.innerHTML=`<span class="api-status ${d.format}">${d.format.toUpperCase()}</span>`;
            document.getElementById('apiFormatDisplay').style.display='block';
            setupBannerEl.classList.remove('active');
            setTimeout(closeSettings,1000);
        }else{cs.style.display='block';cs.style.color='#721c24';cs.textContent='❌ '+d.error}
    }catch(e){alert('保存失败: '+e.message)}
}

async function testConfig(){
    const cfg={api_endpoint:document.getElementById('cfgEndpoint').value.trim(),
               api_key:document.getElementById('cfgKey').value.trim(),
               model:document.getElementById('cfgModel').value.trim()};
    if(!cfg.api_endpoint||!cfg.api_key||!cfg.model){alert('请先填写配置');return}
    const cs=document.getElementById('configStatus');cs.style.display='block';cs.style.color='#856404';cs.textContent='⏳ 测试中...';
    try{
        const r=await fetch('/api/config/test',{method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify(cfg)});
        const d=await r.json();
        if(d.success){
            cs.style.color='#155724';cs.textContent=`✅ 连接成功！格式: ${d.format.toUpperCase()}`;
            const tag=document.getElementById('apiFormatTag');
            tag.innerHTML=`<span class="api-status ${d.format}">${d.format.toUpperCase()}</span>`;
            document.getElementById('apiFormatDisplay').style.display='block';
        }else{cs.style.color='#721c24';cs.textContent='❌ '+d.error}
    }catch(e){cs.style.color='#721c24';cs.textContent='❌ 测试失败: '+e.message}
}

// 点击遮罩关闭弹窗
document.getElementById('settingsModal').onclick=function(e){if(e.target===this)closeSettings()};

// 页面加载时检测配置状态
loadConfig();
</script>
</body>
</html>"""


class UploadHandler(http.server.BaseHTTPRequestHandler):
    """处理上传、API调用和配置管理"""

    def _send_html(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode('utf-8'))

    def _send_json(self, status_code, **kwargs):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(kwargs).encode())

    def do_GET(self):
        if self.path == '/':
            self._send_html()
        elif self.path == '/api/config':
            cfg = api_config.load_config()
            # 返回配置（Key 部分隐藏）
            display_cfg = {
                'api_endpoint': cfg.get('api_endpoint', ''),
                'api_key': cfg.get('api_key', '')[:8] + '...' if len(cfg.get('api_key', '')) > 8 else '',
                'model': cfg.get('model', ''),
                'api_format': cfg.get('api_format', 'openai')
            }
            needs_setup = not cfg.get('api_key') or not cfg.get('api_endpoint') or not cfg.get('model')
            self._send_json(200, success=True, config=display_cfg, needs_setup=needs_setup)
        else:
            self._send_json(404, success=False, error='Not Found')

    def do_POST(self):
        if self.path == '/api/config':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = json.loads(self.rfile.read(length).decode('utf-8'))

                cfg = api_config.load_config()
                if 'api_endpoint' in body and body['api_endpoint'].strip():
                    cfg['api_endpoint'] = body['api_endpoint'].strip()
                if 'api_key' in body and body['api_key'].strip():
                    cfg['api_key'] = body['api_key'].strip()
                if 'model' in body and body['model'].strip():
                    cfg['model'] = body['model'].strip()

                # 自动检测 API 格式
                cfg['api_format'] = api_config.detect_format(cfg['api_endpoint'])

                # 保存配置
                cfg_path = SAVE_DIR / 'config.json'

                with open(cfg_path, 'w', encoding='utf-8') as f:
                    json.dump(cfg, f, ensure_ascii=False, indent=2)

                global CONFIG, MODEL, NEED_SETUP
                CONFIG = cfg
                MODEL = cfg['model']
                NEED_SETUP = False

                print(f"  ✅ 配置已更新: {cfg['model']} @ {cfg['api_endpoint']}")
                self._send_json(200, success=True, format=cfg['api_format'])

            except Exception as e:
                self._send_json(400, success=False, error=str(e))

        elif self.path == '/api/config/test':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = json.loads(self.rfile.read(length).decode('utf-8'))

                import api_config as ac
                # 临时测试
                fmt = ac.detect_format(body.get('api_endpoint', ''))
                self._send_json(200, success=True, format=fmt)

            except Exception as e:
                self._send_json(400, success=False, error=str(e))

        elif self.path == '/upload':
            try:
                form = self._parse_multipart()
                images = form.get('image', [])
                if not images:
                    self._send_json(400, success=False, error='未找到图片文件')
                    return

                if not isinstance(images, list):
                    images = [images]

                item = images[0]
                filename = item.get('filename', 'uploaded_image.png')
                data = item.get('data', b'')
                ext = os.path.splitext(filename)[1].lower()

                if not data:
                    self._send_json(400, success=False, error='文件内容为空')
                    return

                if ext not in SUPPORTED_EXT:
                    self._send_json(400, success=False, error=f'不支持的格式: {ext}')
                    return

                save_path = SAVE_DIR / filename
                counter = 1
                while save_path.exists():
                    stem = Path(filename).stem
                    save_path = SAVE_DIR / f"{stem}_{counter}{ext}"
                    counter += 1

                with open(save_path, 'wb') as f:
                    f.write(data)

                print(f"\n✅ 收到图片: {save_path.name} ({len(data)/1024:.1f}KB)")
                print(f"⏳ 调用 {MODEL} 识别 {save_path.name} ...")

                result = api_config.call_vision_api(str(save_path), config=CONFIG)

                print(f"📋 {save_path.name} 识别完成")
                self._send_json(200, success=True, filename=save_path.name, saved_as=save_path.name, result=result)

            except Exception as e:
                print(f"❌ 错误: {e}")
                self._send_json(500, success=False, error=str(e))
        else:
            self._send_json(404, success=False, error='Not Found')

    def _parse_multipart(self):
        """手动解析 multipart/form-data，支持同名多文件"""
        ct = self.headers.get('Content-Type', '')
        match = re.search(r'boundary=([^;\s]+)', ct)
        if not match:
            return {}
        boundary = match.group(1).encode()
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        result = {}
        parts = body.split(b'--' + boundary)
        for part in parts:
            if part.strip() in (b'', b'--', b'\r\n--'):
                continue
            header_end = part.find(b'\r\n\r\n')
            if header_end == -1:
                continue
            headers_raw = part[:header_end].decode('utf-8', errors='replace')
            content = part[header_end + 4:]
            if content.endswith(b'\r\n'):
                content = content[:-2]

            name_match = re.search(r'name="([^"]*)"', headers_raw)
            filename_match = re.search(r'filename="([^"]*)"', headers_raw)
            name = name_match.group(1) if name_match else None

            if filename_match and name:
                entry = {'filename': filename_match.group(1), 'data': content}
                if name in result:
                    if isinstance(result[name], list):
                        result[name].append(entry)
                    else:
                        result[name] = [result[name], entry]
                else:
                    result[name] = [entry]
            elif name:
                result[name] = content.decode('utf-8', errors='replace')
        return result

    def log_message(self, fmt, *args):
        print(f"[{args[0]}] {args[1]} {args[2]}")


def main():
    banner = f"""
{'='*55}
  🖼️  批量图片识别工具
  模型: {MODEL}
  目录: {SAVE_DIR}
  支持: 多张图片同时上传，逐张识别
{'='*55}
"""
    print(banner)

    server = http.server.HTTPServer(('0.0.0.0', PORT), UploadHandler)
    url = f"http://localhost:{PORT}"

    print(f"  🔗 正在打开浏览器: {url}")
    print(f"  📸 支持选择多张图片")
    if NEED_SETUP:
        print(f"  ⚙️  首次使用，请在网页上配置 API 信息")
    print(f"  ⏹️  按 Ctrl+C 停止服务\n")
    print(f"{'='*55}\n")

    threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
        server.server_close()


if __name__ == '__main__':
    try:
        import requests
    except ImportError:
        print("正在安装 requests 库...")
        os.system(f"{sys.executable} -m pip install requests --quiet")
        import requests

    main()

# 🖼️ Image Recognizer / 图片识别工具

A local image recognition tool that uses visual AI models (via API) to analyze images. Upload images through a web interface, get AI-powered descriptions, OCR, and scene analysis.

本地图片识别工具，通过调用视觉大模型 API 分析图片。支持网页上传、批量识别、自动保存结果。

---

## Why This Project? / 为什么做这个项目

Many third-party language models do not support multimodal (vision) capabilities — they can process text but cannot "see" images. This tool solves that problem by:

很多第三方语言模型不具备多模态（视觉）能力——它们能处理文字，但"看"不了图片。这个工具通过以下方式解决：

1. Using a dedicated vision-capable model API to analyze images / 用专门的视觉模型 API 分析图片
2. Converting the visual information into detailed text descriptions / 将视觉信息转为详细的文字描述
3. Feeding those descriptions back to any language model / 将描述结果回传给任何语言模型

This way, even if your primary model lacks vision support, you can still "show" it images through detailed text descriptions. The tool acts as a bridge between your images and any text-only AI model.

这样一来，即使你的主力模型不支持看图，也能通过文字描述"看"到图片内容。这个工具就是图片和纯文本模型之间的桥梁。

---

## Features / 功能

- **Batch Upload / 批量上传** — Select multiple images at once, analyzed one by one / 一次选择多张图片，逐张识别
- **Web UI / 网页界面** — Drag-and-drop upload with live preview / 拖拽上传，实时预览
- **Auto-save / 自动保存** — Images and analysis results saved locally / 图片和分析结果自动保存到本地
- **API Auto-detect / 自动适配 API** — Supports OpenAI and Anthropic formats / 支持 OpenAI 和 Anthropic 两种格式
- **Privacy / 隐私安全** — Images stay on your machine, sent only to your configured API / 图片仅发送到你配置的 API
- **Claude Sync / Claude 同步** — Results can be synced back to Claude desktop / 结果可自动同步到 Claude

---

## Quick Start / 快速开始

### Requirements / 环境要求
- Python 3.8+
- An API key for a vision-capable model / 一个支持视觉识别的模型 API Key

### Run / 运行

```bash
cd ImageRecognizer
python image_uploader.py
```

Or double-click **`start.bat`** (Windows).

或直接双击 **`start.bat`**（Windows）。

### First-time Setup / 首次配置

1. Open http://localhost:8765 in your browser / 在浏览器中打开 http://localhost:8765
2. Click the ⚙️ button in the top-right corner / 点击右上角 ⚙️ 按钮
3. Enter your API endpoint, API key, and model name / 填写 API 地址、Key 和模型名
4. Click "Save" / 点击"保存配置"

### Usage / 使用

1. Drag and drop images onto the upload area (or click to select) / 拖拽图片到上传区域（或点击选择）
2. Click "Upload & Analyze" / 点击"上传并识别"
3. Results appear in the browser and are saved to `*_analysis.txt` files / 结果显示在网页上，同时保存到 `*_analysis.txt` 文件

---

## Configuration / 配置

Settings are stored in `config.json` (auto-created on first run):

配置文件保存在 `config.json`（首次运行时自动创建）：

```json
{
  "api_endpoint": "https://your-api-endpoint/v1/chat/completions",
  "api_key": "sk-your-key-here",
  "model": "your-model-name"
}
```

### API Format Support / 支持的 API 格式

The tool automatically detects and tries both formats:

工具会自动检测并尝试两种格式：

- **OpenAI format** — `/v1/chat/completions`, image as `image_url`
- **Anthropic format** — `/v1/messages`, image as `image` source

---

## Three Recognition Methods / 三种识别方式

### ① Web Tool / 网页工具 🖥️

Drag-and-drop web UI, best for batch upload.

拖拽上传的网页界面，适合批量操作。

```
start.bat  →  http://localhost:8765
```

---

### ② MCP Server (Standard) / 标准 MCP 🔌

Call recognition directly via Claude Code CLI.

通过 Claude Code CLI 直接调用识别。

```bash
claude --mcp "python vision_mcp_server.py"
```

**Available tools / 可用工具:**

| Tool / 工具 | Description / 说明 |
|-------------|-------------------|
| `analyze_image` | Analyze by file path / 按文件路径分析 |
| `batch_analyze_images` | Batch analyze / 批量分析 |
| `analyze_uploaded_image` | Temp web upload page / 临时网页上传 |
| `check_config` | Check API status / 查看配置 |

---

### ③ MCP+ 🚀

**Enhanced mode — upload images directly in chat, no browser needed.**

增强模式 — 直接在对话中上传图片，无需开浏览器。

MCP+ runs as a background service. When you upload an image in chat, Claude detects it and delegates recognition to the MCP server automatically.

MCP+ 以后台服务运行，你在对话中上传图片，Claude 自动调用 MCP 识别。

**CLAUDE.md config / 配置方式:**
```yaml
mcpServers:
  vision-recognizer:
    command: python
    args: ["D:\\ImgBridge\\vision_mcp_server.py"]
```

---

## Environment Guide / 环境配置

### Windows (start.bat)
```
双击 start.bat → http://localhost:8765 → 配置 API → 上传识别
```

### Linux / macOS
```bash
cd ImgBridge
python image_uploader.py
```

### Claude Desktop (MCP)
```
Settings → MCP Servers → Add:
  Name: vision-recognizer
  Command: python
  Args: D:\ImgBridge\vision_mcp_server.py
Restart → done
```

### Claude Code CLI (MCP)
```bash
claude --mcp "python D:\ImgBridge\vision_mcp_server.py"
```

---

## Tips / 使用技巧

| Scenario / 场景 | Best method / 最佳方式 |
|----------------|----------------------|
| Quick single image / 快速单张 | MCP / MCP+ |
| Batch many images / 批量多张 | Web Tool (drag & drop) |
| No browser / 不想开浏览器 | MCP+ (chat upload) |
| First time setup / 首次配置 | Web Tool (⚙️ UI) |
| Code integration / 代码集成 | MCP (CLI automation) |

---

## CLI Tool / 命令行工具

A command-line version is also included:

同时提供命令行版本：

```bash
python analyze_image.py photo.jpg
python analyze_image.py                    # Interactive mode / 交互模式
```

---

## Project Structure / 项目结构

```
├── image_uploader.py        # 🖥️ Web tool / 网页主程序
├── vision_mcp_server.py     # 🔌 MCP Server / MCP 服务
├── api_config.py            # ⚙️ Shared config & API caller / 共享配置
├── analyze_image.py         # 📟 CLI tool / 命令行工具
├── start.bat                # 🪟 Windows launcher
├── config.json              # 🔑 Your API config / 你的配置
├── SKILL.md                 # 📜 Claude Code skill file
└── README.md                # 📖 This file / 本说明文件
```

---

## For Claude Code Users / 给 Claude Code 用户

Place `SKILL.md` in your project's `.claude/skills/` directory to use the `/image-recognize` command.

将 `SKILL.md` 放入项目的 `.claude/skills/` 目录即可使用 `/image-recognize` 命令。

---

## 示例：
<img width="1211" height="945" alt="image" src="https://github.com/user-attachments/assets/b4ddee3d-6c9b-4cc6-b4e8-2825b0da62d6" />
<img width="1199" height="827" alt="image" src="https://github.com/user-attachments/assets/8b130dd8-39ba-403c-a33f-74bcf01326de" />
<img width="1148" height="761" alt="image" src="https://github.com/user-attachments/assets/693e212d-1607-4a52-9ac1-d68015dfce9f" />

图片素材来源：https://miles-dml.org/ja/milet/galleryDetail/gallery_10#gallery-8

## License / 许可证

MIT

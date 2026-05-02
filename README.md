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
├── image_uploader.py      # Main web UI tool / 网页版主程序
├── analyze_image.py       # CLI tool / 命令行工具
├── api_config.py          # Shared config & API caller / 配置与 API 调用模块
├── start.bat              # Windows launcher / Windows 启动器
├── config.json            # Your API config (auto-created) / 你的 API 配置 (自动生成)
├── SKILL.md               # Claude Code skill file / Claude Code 技能文件
└── README.md              # This file / 本说明文件
```

---

## For Claude Code Users / 给 Claude Code 用户

Place `SKILL.md` in your project's `.claude/skills/` directory to use the `/image-recognize` command.

将 `SKILL.md` 放入项目的 `.claude/skills/` 目录即可使用 `/image-recognize` 命令。

---

## License / 许可证

MIT

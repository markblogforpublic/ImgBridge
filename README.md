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
## 示例：Claude Code Desktop 接入Deepseek 截止至2026.5.2并不支持多模态，所以通过千问实现图片理解并将结果自动同步在Claude Code Desktop
<img width="1211" height="945" alt="image" src="https://github.com/user-attachments/assets/b4ddee3d-6c9b-4cc6-b4e8-2825b0da62d6" />
<img width="1199" height="827" alt="image" src="https://github.com/user-attachments/assets/8b130dd8-39ba-403c-a33f-74bcf01326de" />
<img width="1148" height="761" alt="image" src="https://github.com/user-attachments/assets/693e212d-1607-4a52-9ac1-d68015dfcef9" />

图片素材来源：https://miles-dml.org/ja/milet/galleryDetail/gallery_10#gallery-8

### 同时我也展示网页上此时什么情况 

这是配置：
<img width="756" height="823" alt="image" src="https://github.com/user-attachments/assets/30fc4218-f98e-4eb3-94d6-7554fe95bb31" />

这是输出：
<img width="1177" height="1210" alt="image" src="https://github.com/user-attachments/assets/a00a6dd0-6adb-4931-bf93-c4ee51a82872" />
<img width="1080" height="546" alt="image" src="https://github.com/user-attachments/assets/62335b54-a0c8-49b8-8710-3231643640b7" />





## License / 许可证

MIT
---

## Disclaimer / 免责声明

This software is provided "as is", without warranty of any kind, express or implied. The authors assume no responsibility for any damages or losses arising from the use of this software.

本软件按"原样"提供，不附带任何明示或暗示的保证。作者不对因使用本软件而产生的任何损害或损失承担责任。

Users are solely responsible for:
- Compliance with the terms of service of any third-party API they connect to
- The content they upload and process through this tool
- Ensuring they have the right to analyze any images they submit
- Protecting their own API keys and configuration data

使用者需自行承担以下责任：
- 遵守所接入的第三方 API 的服务条款
- 上传和处理的内容的合规性
- 确保拥有所提交图片的分析权限
- 保护自己的 API Key 和配置信息

## Non-Infringement Statement / 不侵权声明

This project is an independent local tool that provides a technical interface for calling visual AI APIs. It does not:

本项目是一个独立的本地工具，提供调用视觉 AI API 的技术接口，不涉及以下行为：

- **Not a substitute** — This tool does not replace, replicate, or distribute any third-party model. It simply provides a local interface to call APIs that users configure themselves.
  **非替代品** — 本工具不替代、不复制、不分发任何第三方模型，仅提供本地界面让用户调用自己配置的 API。

- **No bundled models** — No model weights, model binaries, or proprietary algorithms are included in this repository. All AI processing is done remotely through the user's own API configuration.
  **不包含模型** — 本仓库不包含任何模型权重、模型二进制文件或专有算法，所有 AI 处理均通过用户自配的 API 远程完成。

- **No data collection** — This tool does not collect, store, or transmit any user data to any third party beyond the API endpoints explicitly configured by the user.
  **不收集数据** — 本工具不收集、不存储、不向任何第三方传输用户数据（除用户明确配置的 API 端点外）。

- **User responsibility** — Users are responsible for ensuring their use of this tool and any connected APIs complies with applicable laws and terms of service.
  **用户责任** — 用户需确保使用本工具及所连接的 API 符合相关法律和服务条款。


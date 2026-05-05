# 🖼️ Image Recognizer / 图片识别工具 [![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

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

**Enhanced mode for Claude Code CLI only — pop up a file picker dialog, no path typing needed.**

增强模式（仅 **Claude Code CLI**，Cowork 模式不支持）— 弹出文件选择框，无需输入路径。

MCP+ adds the `analyze_image_dialog` tool, which opens a native Windows file picker dialog when called. Select the image with a click — no browser, no manual path input.

MCP+ 增加了 `analyze_image_dialog` 工具，调用时弹出 Windows 文件选择框，点选图片即可识别。

**CLAUDE.md config / 配置方式:**
```yaml
mcpServers:
  vision-recognizer:
    command: python
    args: ["D:\\ImgBridge\\vision_mcp_server.py"]
```

**Extra tool in MCP+ / MCP+ 专属工具:**

| Tool / 工具 | Description / 说明 |
|-------------|-------------------|
| `analyze_image_dialog` | 🆕 **Open file picker dialog (CLI only)** / 弹出文件选择框（仅 CLI） |

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

### Claude Code CLI (MCP / MCP+)
```bash
claude --mcp "python D:\ImgBridge\vision_mcp_server.py"
```

---

## Tips / 使用技巧

| Scenario / 场景 | Best method / 最佳方式 |
|----------------|----------------------|
| Quick single image / 快速单张 | MCP / MCP+ (CLI) |
| Batch many images / 批量多张 | Web Tool (drag & drop) |
| No browser / 不想开浏览器 | MCP+ file dialog (CLI only) |
| Cowork mode / Cowork 模式 | Web Tool or direct file path |
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

## 示例： ① Web Tool / 网页工具 🖥️
<img width="1211" height="945" alt="image" src="https://github.com/user-attachments/assets/b4ddee3d-6c9b-4cc6-b4e8-2825b0da62d6" />
<img width="1199" height="827" alt="image" src="https://github.com/user-attachments/assets/8b130dd8-39ba-403c-a33f-74bcf01326de" />
<img width="1148" height="761" alt="屏幕截图 2026-05-02 173043" src="https://github.com/user-attachments/assets/00228021-3a49-40d8-9945-ed639fb4d78e" />

---
<img width="756" height="823" alt="屏幕截图 2026-05-02 173835" src="https://github.com/user-attachments/assets/28c8cbd0-2ed4-429c-8ad0-7419e88d3453" />
<img width="1177" height="1210" alt="屏幕截图 2026-05-02 173645" src="https://github.com/user-attachments/assets/25d58212-b1b6-42e7-88df-d50b549c7668" />
---

## 示例：  ② MCP Server (Standard) / 标准 MCP 🔌

<img width="1136" height="883" alt="屏幕截图 2026-05-03 224824" src="https://github.com/user-attachments/assets/9d08513b-87ad-499b-9cf9-0293a095412a" />
---

## 示例：   ③ MCP+ 🚀
<img width="1216" height="968" alt="屏幕截图 2026-05-03 230709" src="https://github.com/user-attachments/assets/c6fa423c-81ff-4562-8554-c2f20652e814" />
---

图片素材来源：https://miles-dml.org/ja/milet/galleryDetail/gallery_10#gallery-8

## License / 许可证 

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## Disclaimer / 免责声明
This software is provided "as is", without warranty of any kind, express or implied. The authors assume no responsibility for any damages or losses arising from the use of this software.
本软件按"原样"提供，不附带任何明示或暗示的保证。作者不对因使用本软件而产生的任何损害或损失承担责任。
Users are solely responsible for:

Compliance with the terms of service of any third-party API they connect to
The content they upload and process through this tool
Ensuring they have the right to analyze any images they submit
Protecting their own API keys and configuration data

使用者需自行承担以下责任：

遵守所接入的第三方 API 的服务条款
上传和处理的内容的合规性
确保拥有所提交图片的分析权限
保护自己的 API Key 和配置信息

## Non-Infringement Statement / 不侵权声明
This project is an independent local tool that provides a technical interface for calling visual AI APIs. It does not:
本项目是一个独立的本地工具，提供调用视觉 AI API 的技术接口，不涉及以下行为：

Not a substitute — This tool does not replace, replicate, or distribute any third-party model. It simply provides a local interface to call APIs that users configure themselves.
非替代品 — 本工具不替代、不复制、不分发任何第三方模型，仅提供本地界面让用户调用自己配置的 API。
No bundled models — No model weights, model binaries, or proprietary algorithms are included in this repository. All AI processing is done remotely through the user's own API configuration.
不包含模型 — 本仓库不包含任何模型权重、模型二进制文件或专有算法，所有 AI 处理均通过用户自配的 API 远程完成。
No data collection — This tool does not collect, store, or transmit any user data to any third party beyond the API endpoints explicitly configured by the user.
不收集数据 — 本工具不收集、不存储、不向任何第三方传输用户数据（除用户明确配置的 API 端点外）。
User responsibility — Users are responsible for ensuring their use of this tool and any connected APIs complies with applicable laws and terms of service.
用户责任 — 用户需确保使用本工具及所连接的 API 符合相关法律和服务条款。

## Example Image Notice / 示例图片不侵权声明
The example image of the female portrait used in this project's demonstration is sourced from a public figure's publicly available gallery and is used solely for the purpose of showcasing the tool's functionality. We believe this constitutes fair use. If you are the rights holder and believe this infringes upon your rights, please contact us to have it removed immediately.
本项目演示中使用的女性肖像示例图片来源于公众人物的公开图库，仅用于展示工具功能。我们坚信此举符合合理使用原则。如您是版权持有人并认为构成侵权，请联系我们立即删除。

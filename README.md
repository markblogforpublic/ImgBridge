# 🖼️ ImgBridge

**ImgBridge** — 给纯文本 AI 模型装上"眼睛"。通过视觉 API 识别图片，让任何语言模型都能"看懂"图片内容。

A local image recognition tool that bridges images and text-only AI models via visual API calls.

---

## Why / 为什么

Many third-party language models do not support multimodal (vision) capabilities — they process text but cannot "see" images. **ImgBridge** solves this:

很多第三方语言模型不具备多模态能力。ImgBridge 作为桥梁，让纯文本模型也能"看"图：

1. Use a vision-capable API to analyze images / 用视觉 API 分析图片
2. Convert visual content into detailed text / 将视觉内容转为详细文字
3. Feed descriptions to any text-only model / 将描述回传给任何语言模型

---

## Three Recognition Methods / 三种识别方式

### ① Web Tool / 网页工具 🖥️

Drag-and-drop web UI, best for batch upload.

拖拽上传的网页界面，适合批量操作。

```
start.bat  →  http://localhost:8765
```

**Features:**
- Batch upload, analyze one by one / 批量上传逐张识别
- Live preview / 实时预览
- Auto-save results / 自动保存结果
- Config management UI (⚙️ button) / 网页配置管理
- Sync results back to Claude / 结果同步到 Claude

---

### ② MCP Server (Standard) / 标准 MCP 🔌

Call recognition directly via Claude Code CLI.

通过 Claude Code CLI 直接调用识别。

```bash
claude --mcp "python vision_mcp_server.py"
```

**Available tools:**

| Tool / 工具 | Description / 说明 |
|-------------|-------------------|
| `analyze_image` | Analyze by file path / 按文件路径分析 |
| `batch_analyze_images` | Batch analyze / 批量分析 |
| `analyze_uploaded_image` | Temp web upload page / 临时网页上传 |
| `check_config` | Check API status / 查看配置 |

**Usage / 使用方式:**
```
用户: 帮我看下 D:\photo.jpg
Claude: → 调用 analyze_image → 返回识别结果
```

---

### ③ MCP+ 🚀

**Enhanced mode — upload images directly in the chat dialog, no browser needed.**

增强模式 — 直接在对话中上传图片，无需开浏览器。

**How it works / 工作原理:**

MCP+ runs as a background service. When you upload an image in chat, Claude detects it and delegates recognition to the MCP server automatically.

MCP+ 以后台服务运行。你在对话中上传图片，Claude 自动调用 MCP 识别。

```bash
# Start MCP+ service / 启动 MCP+ 服务
python vision_mcp_server.py
```

**CLAUDE.md config / 配置方式:**
```yaml
mcpServers:
  vision-recognizer:
    command: python
    args: ["D:\\ImgBridge\\vision_mcp_server.py"]
```

**Workflow / 流程:**
```
用户: [上传图片] 帮我看这张图
Claude: → 自动调用 MCP+ analyze_image → 返回识别结果
       ✅ 这是...
```

---

## Quick Start / 快速开始

### Requirements / 环境要求

| Dependency | Install |
|-----------|---------|
| Python ≥ 3.8 | [python.org](https://www.python.org/downloads/) |
| requests | `pip install requests` |
| mcp (optional, for MCP mode) | `pip install mcp` |

### Setup / 首次配置

```bash
# 1. Clone or download / 下载项目
# 2. Install dependencies / 安装依赖
pip install requests

# 3. Configure API in config.json / 配置 API
#    Or use the web UI (http://localhost:8765 → ⚙️)
```

### config.json

```json
{
  "api_endpoint": "https://your-api/v1/chat/completions",
  "api_key": "sk-your-key",
  "model": "your-vision-model"
}
```

**API format auto-detected / 自动检测格式:**
- OpenAI: `/v1/chat/completions`, `image_url`
- Anthropic: `/v1/messages`, `image` source

---

## Example / 示例演示

Below is a real recognition result from **ImgBridge**. The image used is a portrait from a public platform, used solely for demonstration.

以下为 ImgBridge 的实测识别结果。示例图片来源于公共平台，仅用于展示：

**Input / 输入:** `test.jpg` — 年轻女性自拍特写

**Output / 输出 (qwen3.6-plus):**

> 这是一张年轻女性的自拍特写照片，画面充满了梦幻和精致的氛围，看起来像是舞台妆造或Cosplay的定妆照。
>
> **人物**：皮肤白皙的年轻女性，面带微笑，右手比"V"字手势在右眼下。妆容精致，眼头贴有水钻亮片。
>
> **服饰**：头戴水晶珠链发箍，额前横跨细链垂挂珠子（精灵/人鱼风）。佩戴珍珠贝壳项链。服装右肩深蓝紫渐变薄纱镶亮片（星空感），左肩白色蕾丝密集珍珠串珠（花朵簇拥立体装饰）。
>
> **背景**：棕褐色斑驳墙面，光线柔和。

This demonstrates how visual content is converted into detailed text that any text-only model can understand.

这展示了图片内容如何被转为详细文字描述，供任何纯文本模型理解。

---

## Environment Guide / 环境配置

### Windows (start.bat)
```
双击 start.bat
→ 自动打开 http://localhost:8765
→ 配置 API → 上传识别
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
Restart → upload image → done
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
| No browser allowed / 不想开浏览器 | MCP+ (chat upload) |
| First time setup / 首次配置 | Web Tool (⚙️ UI) |
| Integration with code / 代码集成 | MCP (CLI automation) |

---

## Project Structure / 项目结构

```
D:\ImgBridge\
├── image_uploader.py        # 🖥️ Web tool / 网页主程序
├── vision_mcp_server.py     # 🔌 MCP Server / MCP 服务
├── api_config.py            # ⚙️ Shared config & API caller / 共享配置
├── analyze_image.py         # 📟 CLI tool / 命令行工具
├── start.bat                # 🪟 Windows launcher
├── config.json              # 🔑 Your API config (edit this) / 你的配置
├── SKILL.md                 # 📜 Claude Code skill / 技能文件
└── README.md                # 📖 This file / 本说明文件
```

---

## For Claude Code Users / 给 Claude Code 用户

Place `SKILL.md` in `.claude/skills/` to use `/image-recognize` and `/image-recognize-mcp` commands.

---

## Example Image Notice / 示例图片说明

The example image used in this project's demonstration is sourced from a public platform and is used solely for the purpose of showcasing the tool's functionality. We believe this constitutes fair use. If you are the rights holder and believe this infringes upon your rights, please contact us to have it removed immediately.

本项目演示中使用的示例图片来源于公共平台，仅用于展示工具功能。如您是版权持有人并认为构成侵权，请联系我们立即删除。

---

## Disclaimer / 免责声明

This software is provided "as is", without warranty of any kind. Users are solely responsible for compliance with third-party API terms of service and the content they process.

本软件按"原样"提供。使用者需自行承担 API 合规和内容合规责任。

## Non-Infringement Statement / 不侵权声明

- **Not a substitute** — Does not replace, replicate, or distribute any third-party model
- **No bundled models** — No model weights or proprietary algorithms included
- **No data collection** — Does not collect or store user data
- **User responsibility** — Users ensure compliance with applicable laws

---

## License / 许可证

MIT

---
name: "image-recognize"
description: "图片识别：用户说'开始'→选文件夹→配置API→启动识别工具→说'结果'展示"
---

# 图片识别技能 (Image Recognition)

## 完整工作流程

### 第一步：用户说 "开始"
用户调用 skill 时输入 `Start` 或 `开始`，Claude 执行：

1. **检查/请求文件夹**
   - 检查 `/sessions/*/mnt/` 下是否有用户已挂载的文件夹
   - 如果没有，调用 `request_cowork_directory` 让用户选择

2. **提示用户配置 API**
   - 告知用户首次使用需在网页上点击右上角 ⚙️ 配置 API

3. **提示用户启动识别工具**
   > "请双击项目文件夹中的 `start.bat`"
   > "首次使用先点击右上角⚙️配置API信息"
   > "上传图片后结果会自动同步到文件夹"
   > "完成后告诉我「结果」"

### 第二步：用户说 "结果"
用户上传识别完成后说 `结果` 或 `result`，Claude 执行：

```bash
# 检查最新结果
cat /sessions/*/mnt/Claude_code_image_idtification/.latest_analysis.json 2>/dev/null
```

- 如果有结果 → 逐张展示识别内容 → 删除 `.latest_analysis.json`
- 如果没结果 → 提示用户先运行识别工具上传图片

## 交互示例

```
用户: /image-recognize 开始
Claude: 请先选择一个文件夹用来保存识别结果
       [用户选择文件夹]
       好的！现在请双击文件夹中的「start.bat」
       首次使用先在网页右上角⚙️配置API信息
       上传图片识别后结果会自动同步
       完成后告诉我「结果」即可

用户: 结果
Claude: ✅ 识别到 X 张图片的结果：
       [逐张展示...]
```

## 注意事项
- 代码中不包含任何 API Key，首次使用需在网页界面上配置
- 配置保存在 `config.json` 中，请勿分享此文件
- 支持批量上传，逐张识别

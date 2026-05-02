"""
图片识别工具 - 使用视觉大模型
================================
用法:
    1. 把图片放到本文件夹中
    2. 在命令行运行: python analyze_image.py <图片文件名>
    3. 或直接输入: python analyze_image.py

配置保存在 config.json 中，自动适配 API 格式。
"""

import json
import os
import sys
from pathlib import Path

# 使用共享配置
sys.path.insert(0, str(Path(__file__).parent))
import api_config

CONFIG = api_config.load_config()
MODEL = CONFIG['model']

# 当前脚本所在目录（即图片存放目录）
IMAGE_DIR = Path(__file__).parent

# 支持的图片格式
SUPPORTED_FORMATS = {
    '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.jfif': 'image/jpeg', '.jpe': 'image/jpeg',
    '.png': 'image/png',
    '.webp': 'image/webp',
    '.gif': 'image/gif',
    '.bmp': 'image/bmp', '.dib': 'image/bmp',
    '.tiff': 'image/tiff', '.tif': 'image/tiff',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.heic': 'image/heic', '.heif': 'image/heif',
    '.avif': 'image/avif',
}


def list_images():
    """列出文件夹中所有支持的图片文件"""
    images = []
    for f in IMAGE_DIR.iterdir():
        if f.is_file() and f.suffix.lower() in SUPPORTED_FORMATS:
            size_mb = f.stat().st_size / (1024 * 1024)
            images.append((f.name, size_mb))
    return sorted(images, key=lambda x: x[0])


def call_vision_api(image_path: str, prompt: str = None) -> str:
    """调用视觉大模型识别图片（使用共享配置）"""
    if not prompt:
        prompt = "请详细描述这张图片的内容，包括但不限于：图中有什么物体、人物、场景、文字、颜色、布局、风格等所有可见信息。如果是文档或截图，请提取其中的文字内容。"

    img_file = Path(image_path)
    if not img_file.exists():
        return f"❌ 找不到图片文件: {image_path}"

    file_size_mb = img_file.stat().st_size / (1024 * 1024)
    if file_size_mb > 20:
        print(f"⚠️  图片较大 ({file_size_mb:.1f}MB)，可能需要较长时间...")

    return api_config.call_vision_api(str(img_file), prompt, config=CONFIG)


def save_result(filename: str, result: str):
    """保存分析结果到同目录"""
    result_file = IMAGE_DIR / f"{Path(filename).stem}_analysis.txt"
    with open(result_file, 'w', encoding='utf-8') as f:
        f.write(f"图片: {filename}\n")
        f.write(f"模型: {MODEL}\n")
        f.write(f"{'='*50}\n\n")
        f.write(result)
    return result_file


def show_help():
    """显示帮助信息"""
    print(f"""
{'='*60}
  🖼️  图片识别工具 - {MODEL}
{'='*60}

用法: python analyze_image.py [图片文件名] [提示词]

示例:
  python analyze_image.py                    # 列出图片并选择
  python analyze_image.py photo.jpg          # 分析指定图片
  python analyze_image.py scan.png "提取文字" # 提取图片中的文字

支持的格式: {', '.join(sorted(SUPPORTED_FORMATS.keys()))}
当前位置: {IMAGE_DIR}
""")


def main():
    print(f"\n{'='*60}")
    print(f"  🖼️  图片识别工具")
    print(f"  模型: {MODEL}")
    print(f"  目录: {IMAGE_DIR}")
    print(f"{'='*60}\n")

    # 如果传了图片文件名
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        prompt = sys.argv[2] if len(sys.argv) >= 3 else None
        image_path = IMAGE_DIR / filename
    else:
        # 列出图片让用户选择
        images = list_images()
        if not images:
            print("📂 当前文件夹中没有找到图片文件")
            print(f"支持的格式: {', '.join(sorted(SUPPORTED_FORMATS.keys()))}")
            print(f"\n请把图片放到: {IMAGE_DIR}")
            return

        print("📂 当前文件夹中的图片:")
        for i, (name, size) in enumerate(images, 1):
            print(f"  [{i}] {name} ({size:.1f}MB)")

        try:
            choice = input("\n请选择编号 (或输入文件名): ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(images):
                    filename = images[idx][0]
                else:
                    print("❌ 无效选择")
                    return
            else:
                filename = choice
        except (EOFError, KeyboardInterrupt):
            print("\n已取消")
            return

        image_path = IMAGE_DIR / filename
        prompt = None

    if not image_path.exists():
        print(f"❌ 找不到文件: {image_path}")
        return

    ext = image_path.suffix.lower()
    if ext not in SUPPORTED_FORMATS:
        print(f"❌ 不支持的格式: {ext}")
        print(f"支持的格式: {', '.join(sorted(SUPPORTED_FORMATS.keys()))}")
        return

    print(f"\n🔍 开始分析: {filename} ({image_path.stat().st_size / 1024:.1f}KB)")
    print(f"{'='*60}\n")

    result = call_vision_api(str(image_path), prompt)

    print(f"\n{'='*60}")
    print(f"  📋 识别结果")
    print(f"{'='*60}\n")
    print(result)

    # 保存结果
    result_file = save_result(filename, result)
    print(f"\n📁 结果已保存: {result_file}")


if __name__ == "__main__":
    main()

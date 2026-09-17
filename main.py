import os
from PIL import Image, ImageDraw, ImageFont

# 1. 基本設定
width, height = 500, 300
png_filename = "number_image.png"
text_to_show = "1位:____\n2位:______\n3位:______"

# 2. 色設定
bg_color = (20, 20, 20)
text_color = (255, 215, 0)

# 3. 画像の作成
img = Image.new("RGB", (width, height), color=bg_color)
draw = ImageDraw.Draw(img)

# 4. アップロードしたカスタムフォント（.woff2）を読み込む
font_size = 40
font_path = "my-font.ttf"  # 📌 ここにあなたのフォントファイル名を入れてください

try:
    # 自前の woff2 フォントを読み込む
    font = ImageFont.truetype(font_path, font_size)
    print(f"Success: {font_path} を読み込みました。")
except IOError:
    # 万が一読み込めなかった場合のバックアップ（Linux標準フォント）
    print(f"Warning: {font_path} の読み込みに失敗したため、代替フォントを探します。")
    fallback_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    ]
    font = None
    for path in fallback_paths:
        if os.path.exists(path):
            font = ImageFont.truetype(path, font_size)
            break
    if font is None:
        font = ImageFont.load_default()

# 5. テキストを中央揃えで描画
bbox = draw.multiline_textbbox((0, 0), text_to_show, font=font, spacing=15)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]

x = (width - text_w) // 2
y = (height - text_h) // 2

draw.multiline_text((x, y), text_to_show, fill=text_color, font=font, align="center", spacing=15)

# 6. 保存
img.save(png_filename, "PNG")
print(f"{png_filename} を作成しました！")

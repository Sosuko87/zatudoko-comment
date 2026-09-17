import os
from PIL import Image, ImageDraw, ImageFont

# 1. 基本設定（複数行になるため縦幅を広めに設定）
width, height = 500, 300
png_filename = "number_image.png"

# 表示したいランキングのテキスト（\n で改行）
text_to_show = "1位:____\n2位:______\n3位:______"

# 2. 色設定
bg_color = (20, 20, 20)      # 背景: 濃いグレー
text_color = (255, 215, 0)   # 文字: ゴールド

# 3. 画像の作成
img = Image.new("RGB", (width, height), color=bg_color)
draw = ImageDraw.Draw(img)

# 4. フォントの読み込み（GitHub ActionsのLinux環境対策）
font_size = 40
font = None

# Linux環境でよく使われるフォントパスの候補
font_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "arial.ttf" # ローカル（Windows/Mac）テスト用
]

for path in font_paths:
    if os.path.exists(path) or path == "arial.ttf":
        try:
            font = ImageFont.truetype(path, font_size)
            break
        except IOError:
            continue

if font is None:
    font = ImageFont.load_default()
    print("Warning: 標準フォントが見つからなかったため、デフォルトフォントを使用します。")

# 5. 複数行テキストを綺麗に中央揃えで描画
# multiline_textbbox を使うことで全体のサイズを取得
bbox = draw.multiline_textbbox((0, 0), text_to_show, font=font, spacing=15)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]

x = (width - text_w) // 2
y = (height - text_h) // 2

# 描画（align="center" で中央揃え、spacing で行間を調整）
draw.multiline_text((x, y), text_to_show, fill=text_color, font=font, align="center", spacing=15)

# 6. 保存
img.save(png_filename, "PNG")
print(f"{png_filename} を作成しました！")

from PIL import Image, ImageDraw, ImageFont

# 1. 基本設定
width, height = 400, 200
png_filename = "number_image.png"  # 拡張子を .png に変更
number_to_show = "777"

# 2. 色設定
bg_color = (20, 20, 20)      # 背景: 濃いグレー
text_color = (255, 215, 0)   # 文字: ゴールド

# 3. 画像の作成
img = Image.new("RGB", (width, height), color=bg_color)
draw = ImageDraw.Draw(img)

# フォントの設定
try:
    font = ImageFont.truetype("arial.ttf", 80)
except IOError:
    font = ImageFont.load_default()
    
# 文字を中央に配置するための計算
bbox = draw.textbbox((0, 0), number_to_show, font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]
x = (width - text_w) // 2
y = (height - text_h) // 2

# 画像に数字を書き込む
draw.text((x, y), number_to_show, fill=text_color, font=font)

# 4. PNGとして保存
img.save(png_filename, "PNG")
print(f"{png_filename} を作成しました！")

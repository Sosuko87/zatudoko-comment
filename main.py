from PIL import Image, ImageDraw, ImageFont

# 1. 基本設定（画像のサイズや表示する数字）
width, height = 400, 200
gif_filename = "pikopiko_number.gif"
number_to_show = "777"  # ここに出したい数字を入れます

# 2. フレーム（コマ）ごとの色設定（点滅させるために2パターン用意）
# コマ1: 明るい状態、コマ2: 暗い（消えかかった）状態
colors = [
    {"bg": (20, 20, 20), "text": (255, 215, 0)},     # 背景:濃いグレー、文字:金（明るい）
    {"bg": (20, 20, 20), "text": (60, 50, 10)}       # 背景:濃いグレー、文字:くすんだ色（暗い）
]

frames = []

# 3. 画像をプログラムで自動的に作成
for color in colors:
    # 新しい画像を作成
    img = Image.new("RGB", (width, height), color=color["bg"])
    draw = ImageDraw.Draw(img)
    
    # フォントの設定（サイズは80）
    try:
        # WindowsやMacにある標準フォントを試す
        font = ImageFont.truetype("arial.ttf", 80)
    except IOError:
        # フォントが見つからない場合はデフォルトのフォントを使用
        font = ImageFont.load_default()
        
    # 文字を中央に配置するための計算
    bbox = draw.textbbox((0, 0), number_to_show, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (width - text_w) // 2
    y = (height - text_h) // 2
    
    # 画像に数字を書き込む
    draw.text((x, y), number_to_show, fill=color["text"], font=font)
    frames.append(img)

# 4. アニメーションGIFとして保存
frames[0].save(
    gif_filename,
    save_all=True,
    append_images=frames[1:],
    duration=150,  # 1コマの表示時間（ミリ秒）。小さくするとより高速にピコピコします
    loop=0         # 0を指定すると無限ループになります
)

print(f"{gif_filename} を作成しました！")

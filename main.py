import os
from PIL import Image, ImageDraw, ImageFont
import scratchattach as sa
from collections import Counter
import urllib.request
import time
from datetime import datetime, timezone

USERNAME = os.environ.get("SCRATCH_USERNAME")
PASSWORD = os.environ.get("SCRATCH_PASSWORD")
PROJECT_ID = 1382320367
SECOND_PROJECT_ID = 1383178970

session = sa.login(USERNAME, PASSWORD)
project = session.connect_project(PROJECT_ID)


#------------------Scratchattachフェーズ-----------------------

# 1. 設定
STUDIO_ID = "51864038"
TARGET_PARENT_COUNT = 1000  # 取得する親コメントの目標数

print(f"スタジオ {STUDIO_ID} のデータを取得中...")
studio = sa.get_studio(STUDIO_ID)

# --- ここに「時速計算処理」を差し込む ---
jisoku = 0
try:
    # 最初の50件をテスト用に1回だけ取得
    speed_comments = studio.comments(limit=10, offset=0)
    
    if len(speed_comments) >= 2:
        target_comment = speed_comments[-1] # 50個前のコメント
        
        # 1. コメントの時間を「文字列」として取得
        time_str = target_comment.datetime_created  # 例: "2026-09-18T16:20:00.000Z"
        
        # 2. datetimeオブジェクトに変換（一番安全なISOフォーマット読み込み）
        # ※ 末尾の 'Z' をPythonが読める形式に置き換えます
        comment_datetime = datetime.fromisoformat(time_str.replace('Z', '+00:00')).replace(tzinfo=None)
        
        comment_num = comment_datetime.timestamp()
        
        now_num = datetime.utcnow().timestamp() 

        minutes_passed = (now_num - comment_num) / 60

        
        # 5. 時速を計算（50コメ ÷ 経過した分 × 60分）
        if minutes_passed > 0:
            jisoku = (len(speed_comments) / minutes_passed) * 60
            jisoku = round(jisoku, 1)  # 四捨五入してきれいな数字に
            print(f"【成功】現在の時速は 【{jisoku} コメ/時間】 です！")
        else:
            print("時間の経過が正常に計算できませんでした。")
except Exception as e:
    print(f"時速計算でエラーが発生しました: {e}")
# ------------------------------------

all_commenters = []
parent_count = 0
offset = 0
limit = 50  # 1回あたりの取得件数

while parent_count < TARGET_PARENT_COUNT:
    # 親コメントの取得
    comments = studio.comments(limit=limit, offset=offset)
    if not comments:
        break
    
    for c in comments:
        all_commenters.append(c.author().username)
        parent_count += 1
        
        
        # 目標の親コメント数に達したらループを抜ける
        if parent_count >= TARGET_PARENT_COUNT:
            break
            
    offset += limit
    print(f"進捗: 親コメント {parent_count}/{TARGET_PARENT_COUNT} 個スキャン完了 (総取得ユーザー名: {len(all_commenters)}件)")
    
    # 取得したコメントがlimit未満なら、これ以上古いコメントはありません
    if len(comments) < limit:
        break
    
    # APIの負荷軽減のための小さなウェイト
    time.sleep(0.5)

# 2. ランキングの集計
counter = Counter(all_commenters)
ranking = counter.most_common()

# 3. 結果の表示
print("\n=== コメント数ランキング（直近の親コメント500個＋その返信） ===")
print(f"合計解析件数: {len(all_commenters)} コメント\n")

if not ranking:
    print("コメントが見つかりませんでした。")
else:
    # 上位20名を表示（必要に応じて数値を変更してください）
    for rank, (user, count) in enumerate(ranking[:20], 1):
        print(f"{rank}位: {user} ({count}回)")


# --- ここから変数の代入処理 ---

# 上位3位の変数を初期化（コメントが3人未満だった場合の対策）
rank1_user, rank1_count = None, 0
rank2_user, rank2_count = None, 0
rank3_user, rank3_count = None, 0

# 集計結果が存在する場合のみ、変数に代入
if len(ranking) >= 1:
    rank1_user, rank1_count = ranking[0]
if len(ranking) >= 2:
    rank2_user, rank2_count = ranking[1]
if len(ranking) >= 3:
    rank3_user, rank3_count = ranking[2]

# 3. 変数の中身を確認（プリント出力）
print("\n=== 変数に格納された上位3位データ ===")
print(f"1位の変数 -> ユーザー名: {rank1_user}, 回数: {rank1_count}回")
print(f"2位の変数 -> ユーザー名: {rank2_user}, 回数: {rank2_count}回")
print(f"3位の変数 -> ユーザー名: {rank3_user}, 回数: {rank3_count}回")







#------------------画像作成フェーズ-----------------------

# 1. 基本設定
width, height = 480, 360
png_filename = "number_image.png"
text_to_show = f"1位:{rank1_user}　コメント数:{rank1_count}回\n2位:{rank2_user}　コメント数:{rank2_count}回\n3位:{rank3_user}　コメント数:{rank3_count}回\n\n総合スピード:　{jisoku}コメント/時"

# 2. 色設定
bg_color = (20, 20, 20)
text_color = (255, 215, 0)

# 3. 画像の作成
img = Image.new("RGB", (width, height), color=bg_color)
draw = ImageDraw.Draw(img)

font_size = 20
font_path = "my-font.ttf" 


font = ImageFont.truetype(font_path, font_size)
print(f"Success: {font_path} を読み込みました。")

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
project.set_thumbnail(file="number_image.png")


# 【修正ポイント】Counterをきれいなテキストに変換する
instructions_text = "【ランキング（多い順）】\n"
for rank, (user, count) in enumerate(ranking[:20], 1):
    instructions_text += f"・{rank}位:  {user} {count}回\n"

project.set_instructions(f"20位までの発表...\n\n{instructions_text}\n\nこれらの情報は全て自動で更新されています。\n\nバグ等がございましたら @ZZZBanana のコメント欄でお伝えください。")





utc_now = datetime.now(timezone.utc)

# 2. 「分」を10の倍数に切り捨てる計算
# （例：23分 // 10 = 2  ->  2 * 10 = 20分）
rounded_minute = (utc_now.minute // 10) * 10

# 3. 分を置き換えて、秒とマイクロ秒を0にする
new_utc = utc_now.replace(minute=rounded_minute, second=0, microsecond=0)
use_utc = new_utc.strftime("%H%M")
print(use_utc)
image_url = f"https://www.data.jma.go.jp/mscweb/data/himawari/img/jpn/jpn_trm_{use_utc}.jpg"

# 5. 一時的にパソコンに画像を保存する（ファイル名は temporary_thumb.jpg）
jpg_filename = "temporary_thumb.jpg"
png_filename = "temporary_thumb.png"

try:
    print("気象庁から画像をダウンロード中...")
    urllib.request.urlretrieve(image_url, jpg_filename)
    with Image.open(jpg_filename) as img:
        img.save(png_filename, "PNG")
    
    # 6. Scratchのプロジェクトに接続してサムネイルを設定
    project = session.connect_project(SECOND_PROJECT_ID)
    
    # 引数は元の「file=」に戻し、保存した画像ファイルを指定します
    project.set_thumbnail(file=png_filename)
    print("サムネイルの変更が完了しました！")

except Exception as e:
    print(f"エラーが発生しました: {e}")
    print("※気象庁の画像がまだサーバーにアップロードされていない（配信遅延）可能性があります。")

import os
import sys
import requests
import html
from datetime import datetime, timezone, timedelta

# API設定（環境変数から取得。GitHub Actions では Secrets から渡される）
API_ID = os.environ.get("FANZA_API_ID")
AFFILIATE_ID = os.environ.get("FANZA_AFFILIATE_ID")

API_URL = "https://api.dmm.com/affiliate/v3/ItemList"
HITS = 5

params = {
    "api_id": API_ID,
    "affiliate_id": AFFILIATE_ID,
    "site": "FANZA",
    "service": "doujin",
    "floor_id": "digital_doujin",
    "sort": "rank",
    "hits": HITS,
    "output": "json",
}

# API呼び出し
response = requests.get(API_URL, params=params)
if response.status_code != 200:
    print(f"APIエラー: ステータスコード {response.status_code}")
    sys.exit(1)

data = response.json()
items = data.get("result", {}).get("items", [])

if not items:
    print("ランキングデータが取得できませんでした")
    sys.exit(1)

# 日本時間で更新日時を取得
jst = timezone(timedelta(hours=9))
now = datetime.now(jst).strftime("%Y/%m/%d %H:%M")

# 順位バッジの色
BADGE_COLORS = {
    1: "#DAA520",  # 金
    2: "#A0A0A0",  # 銀
    3: "#CD7F32",  # 銅
    4: "#888888",
    5: "#888888",
}

# HTMLの各アイテムを生成
items_html = ""
for i, item in enumerate(items, 1):
    title = html.escape(item.get("title", ""))
    image_url = item.get("imageURL", {}).get("large", "")
    link_url = item.get("affiliateURL", "")
    badge_color = BADGE_COLORS.get(i, "#888888")

    items_html += f"""
    <div class="ranking-item">
      <a href="{link_url}" target="_blank" rel="noopener" class="item-link">
        <div class="thumb-wrap">
          <div class="rank-badge" style="background:{badge_color};">{i}</div>
          <img src="{image_url}" alt="{title}" class="thumb" loading="lazy">
        </div>
        <span class="title">{title}</span>
      </a>
    </div>"""

# 完成HTML
html_output = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=280">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, "Hiragino Sans", "Meiryo", sans-serif;
      width: 280px;
      background: transparent;
      overflow: hidden;
    }}
    .header {{
      background: linear-gradient(135deg, #e83e8c, #ff6b6b);
      color: #fff;
      text-align: center;
      padding: 8px 0;
      font-size: 14px;
      font-weight: bold;
      letter-spacing: 1px;
    }}
    .ranking-item {{
      padding: 8px;
      border-bottom: 1px solid #eee;
    }}
    .ranking-item:last-child {{
      border-bottom: none;
    }}
    .item-link {{
      display: block;
      text-decoration: none;
      color: inherit;
    }}
    .item-link:hover .title {{
      color: #e83e8c;
    }}
    .thumb-wrap {{
      position: relative;
    }}
    .rank-badge {{
      position: absolute;
      top: 4px;
      left: 4px;
      width: 26px;
      height: 26px;
      border-radius: 50%;
      color: #fff;
      font-size: 13px;
      font-weight: bold;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1;
      box-shadow: 0 1px 3px rgba(0,0,0,0.3);
    }}
    .thumb {{
      width: 100%;
      height: auto;
      border-radius: 4px;
      display: block;
    }}
    .title {{
      font-size: 12px;
      line-height: 1.4;
      color: #333;
      margin-top: 4px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      word-break: break-all;
    }}
    .footer {{
      text-align: center;
      font-size: 10px;
      color: #999;
      padding: 6px 0;
      border-top: 1px solid #eee;
    }}
  </style>
</head>
<body>
  <div class="header">FANZA 同人ランキング</div>
{items_html}
  <div class="footer">最終更新: {now}</div>
</body>
</html>
"""

# 出力
os.makedirs("docs", exist_ok=True)
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"docs/index.html を生成しました（{len(items)}件）")

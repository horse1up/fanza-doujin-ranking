
import requests
import html

# ✅ API設定
API_ID = "CpCkdgrGhNRr6gpUxVU3"
AFFILIATE_ID = "uphorse-990"
SITE = "FANZA"
SERVICE = "doujin"
FLOOR_ID = "digital_doujin"
SORT = "rank"
HITS = 20
OUTPUT = "json"

API_URL = "https://api.dmm.com/affiliate/v3/ItemList"

params = {
    "api_id": API_ID,
    "affiliate_id": AFFILIATE_ID,
    "site": SITE,
    "service": SERVICE,
    "floor_id": FLOOR_ID,
    "sort": SORT,
    "hits": HITS,
    "output": OUTPUT
}

response = requests.get(API_URL, params=params)
data = response.json()

html_output = """
<!DOCTYPE html>
<html lang='ja'>
<head>
  <meta charset='UTF-8'>
  <style>
    .ranking-list { display: flex; flex-wrap: wrap; gap: 10px; }
    .ranking-item { width: 200px; text-align: center; }
    .ranking-item img { width: 160px; height: auto; }
    .ranking-item .title { margin-top: 1px; font-size: 10px; color: #333; text-decoration: none; display: block; }
  </style>
</head>
<body>
  <div class='ranking-list'>
"""

for item in data.get("result", {}).get("items", []):
    title = html.escape(item.get("title", ""))
    image_url = item.get("imageURL", {}).get("large", "")
    link_url = item.get("affiliateURL", "")
    html_output += f"""
    <div class='ranking-item'>
      <a href='{link_url}' target='_blank'>
        <img src='{image_url}' alt='{title}'>
      </a>
      <a class='title' href='{link_url}' target='_blank'>{title}</a>
    </div>
    """

html_output += """
  </div>
</body>
</html>
"""

with open("fanza_doujin_ranking.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("✅ HTMLファイルを生成しました： fanza_doujin_ranking.html")

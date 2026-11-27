import json

# ---- edit these 3 lines for each new mock test ----
MOCK_NUM = "__MOCK_NUM__"
SOURCE = "__SOURCE__"          # e.g. "College Board Official Question Bank" or "2024 March, Form D"
JSON_FILE = "__JSON_FILE__"    # e.g. "merged_words_mt56.json"
# -----------------------------------------------------

with open(JSON_FILE, encoding="utf-8") as f:
    words = json.load(f)

rows_html = []
for i, w in enumerate(words, start=1):
    rows_html.append(f"""
    <tr>
      <td class="num">{i}</td>
      <td class="word">{w['word']}</td>
      <td class="edef">{w['edef']}</td>
      <td class="kdef">{w['kdef']} ({w['ensyn']})</td>
    </tr>""")

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page {{ margin: 0; size: 816px 1056px; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: Georgia, serif; background: white; color: #222; }}

.cover-bar {{
  background: #1B2A4A; color: white; padding: 18px 28px;
  display: flex; justify-content: space-between; align-items: center;
}}
.cover-bar .logo {{ font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 15px; font-weight: 700; letter-spacing: 1px; }}
.cover-bar .logo .nobel {{ color: #FFFFFF; }}
.cover-bar .logo .prep {{ color: #C9A84C; }}
.cover-bar .meta {{ font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 10px; color: rgba(255,255,255,0.75); text-align: right; }}

.title-block {{ padding: 18px 28px 10px; border-bottom: 2px solid #C9A84C; }}
.title-block h1 {{ font-size: 20px; color: #1B2A4A; margin-bottom: 4px; }}
.title-block p {{ font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 10.5px; color: #666; }}

table {{ border-collapse: collapse; margin: 14px 28px; width: calc(100% - 56px); }}
thead th {{
  background: #1B2A4A; color: white; font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: 9.5px; font-weight: 700; text-align: left; padding: 6px 8px;
}}
tbody td {{
  font-size: 10.5px; padding: 5px 8px; vertical-align: top;
  border-bottom: 1px solid #e5e5e5;
}}
tbody tr:nth-child(even) {{ background: #FAFAFA; }}
td.num {{ color: #999; font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 9px; width: 24px; }}
td.word {{ font-weight: 700; color: #1B2A4A; width: 110px; }}
td.edef {{ color: #333; width: 42%; font-style: italic; }}
td.kdef {{ color: #333; }}
thead {{ display: table-header-group; }}
tr {{ page-break-inside: avoid; }}

.footer {{
  font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 8.5px; color: #aaa;
  text-align: center; padding: 10px 0;
}}
</style>
</head>
<body>

<div class="cover-bar">
  <div class="logo"><span class="nobel">Nobel</span> <span class="prep">Prep</span></div>
  <div class="meta">Mock Test {MOCK_NUM} &middot; {SOURCE} &middot; Reading and Writing</div>
</div>
<div class="title-block">
  <h1>Vocabulary List &mdash; Mock Test {MOCK_NUM} (R&amp;W)</h1>
  <p>500점대 학생 대상 어휘 {len(words)}개 &middot; 영영 정의(English Definition) + 영한 뜻(Korean Meaning)</p>
</div>

<table>
  <thead>
    <tr>
      <th style="width:24px;">#</th>
      <th style="width:110px;">Word</th>
      <th style="width:42%;">English Definition</th>
      <th>한글 뜻</th>
    </tr>
  </thead>
  <tbody>
    {''.join(rows_html)}
  </tbody>
</table>

<div class="footer">Nobel Prep &middot; Mock Test {MOCK_NUM} Vocabulary List</div>

</body>
</html>
"""

with open("vocab_list.html", "w", encoding="utf-8") as f:
    f.write(html)

print("html written,", len(words), "words")

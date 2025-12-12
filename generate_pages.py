from __future__ import annotations
import csv
import html
import re
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "google-2025-12-12.csv"
DOCS_DIR = ROOT / "docs"
ASSETS_DIR = DOCS_DIR / "assets"


def slugify(name: str) -> str:
    base = re.sub(r"[^\w]+", "-", name.lower(), flags=re.UNICODE).strip("-")
    return base or "location"


def load_rows() -> List[Dict[str, str]]:
    with DATA_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows: List[Dict[str, str]] = []
        for row in reader:
            name = (row.get("qBF1Pd") or "").strip()
            if not name:
                continue
            rows.append({k: (v or "").strip() for k, v in row.items()})
    return rows


def first_non_empty(*values: str) -> str:
    for value in values:
        if value:
            return value
    return ""


def build_entry(row: Dict[str, str]) -> Dict[str, str]:
    notes_fields = [
        row.get("ah5Ghc", ""),
        row.get("ah5Ghc (2)", ""),
        row.get("ah5Ghc (3)", ""),
        row.get("ah5Ghc (4)", ""),
        row.get("ah5Ghc (5)", ""),
    ]
    notes = [note for note in notes_fields if note]

    description = " ".join(notes).strip()

    address = first_non_empty(row.get("W4Efsd (3)", ""), row.get("W4Efsd (6)", ""))
    price = first_non_empty(row.get("AJB7ye (2)", ""), row.get("AJB7ye", ""))

    return {
        "name": row.get("qBF1Pd", ""),
        "slug": slugify(row.get("qBF1Pd", "")),
        "rating": row.get("MW4etd", ""),
        "reviews": row.get("UY7F9", "").strip("()"),
        "category": row.get("W4Efsd", ""),
        "address": address,
        "status": row.get("W4Efsd (4)", ""),
        "hours": row.get("W4Efsd (5)", ""),
        "map_url": row.get("hfpxzc href", ""),
        "hero": row.get("FQ2IWe src", ""),
        "phone": row.get("UsdlK", ""),
        "menu_url": row.get("A1zNzb href", ""),
        "price": price,
        "description": description,
    }


def ensure_assets():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    style_path = ASSETS_DIR / "style.css"
    if not style_path.exists():
        style_path.write_text(
            """
:root {
  --bg: #f9f6f1;
  --card: #ffffff;
  --primary: #8c4a3b;
  --secondary: #d6bfa8;
  --text: #2d1c0f;
  --muted: #6b5c52;
  font-family: 'Inter', 'Noto Sans TC', system-ui, -apple-system, sans-serif;
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
}

a { color: var(--primary); text-decoration: none; }
a:hover { text-decoration: underline; }

.header {
  background: linear-gradient(120deg, var(--secondary), var(--primary));
  color: #fff;
  padding: 2.5rem 1.5rem;
  text-align: center;
}

.container { max-width: 960px; margin: 0 auto; padding: 1.5rem; }

.grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

.card {
  background: var(--card);
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.08);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.card img { width: 100%; height: 160px; object-fit: cover; background: #f0e8df; }

.card .content { padding: 1rem 1rem 1.25rem; flex: 1; display: flex; flex-direction: column; gap: 0.35rem; }

.badge { display: inline-block; background: var(--secondary); color: var(--text); padding: 0.2rem 0.55rem; border-radius: 999px; font-size: 0.85rem; }

.meta { color: var(--muted); font-size: 0.95rem; }

.button {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: var(--primary);
  color: #fff;
  padding: 0.6rem 0.9rem;
  border-radius: 10px;
  font-weight: 600;
}

.details { list-style: none; padding: 0; margin: 0.5rem 0 0; color: var(--muted); }
.details li { margin: 0.25rem 0; }

.hero {
  width: 100%;
  max-height: 320px;
  object-fit: cover;
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.12);
}

.lead { color: var(--muted); line-height: 1.6; }

.cta-row { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.75rem; }
            """,
            encoding="utf-8",
        )


def write_index(entries: List[Dict[str, str]]):
    cards_html = []
    for entry in entries:
        hero = html.escape(entry["hero"]) if entry["hero"] else ""
        details = []
        if entry["category"]:
            details.append(f"<span class='badge'>{html.escape(entry['category'])}</span>")
        info_bits = [
            f"⭐ {html.escape(entry['rating'])}" if entry["rating"] else "",
            f"{html.escape(entry['reviews'])} 則評論" if entry["reviews"] else "",
            html.escape(entry["address"]) if entry["address"] else "",
        ]
        info = " · ".join(filter(None, info_bits))
        description = html.escape(entry["description"] or "這裡有好吃的肉桂捲，快來看看！")
        cards_html.append(
            f"""
            <article class="card">
              {'<img src="'+hero+'" alt="'+html.escape(entry['name'])+'" loading="lazy">' if hero else ''}
              <div class="content">
                <h3><a href="{entry['slug']}/">{html.escape(entry['name'])}</a></h3>
                <div class="meta">{info}</div>
                <p class="lead">{description}</p>
                <a class="button" href="{entry['slug']}/">查看肉桂捲</a>
              </div>
            </article>
            """
        )

    html_doc = f"""
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>肉桂捲地圖 | Cinnamon Roll Finder</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <header class="header">
    <h1>肉桂捲地圖</h1>
    <p>把每一顆肉桂捲都做成獨立小網站，方便你收藏、分享與安排行程。</p>
  </header>
  <main class="container">
    <section class="grid">
      {''.join(cards_html)}
    </section>
  </main>
</body>
</html>
    """

    (DOCS_DIR / "index.html").write_text(html_doc, encoding="utf-8")


def write_entry(entry: Dict[str, str]):
    page_dir = DOCS_DIR / entry["slug"]
    page_dir.mkdir(parents=True, exist_ok=True)
    hero_tag = (
        f"<img class=\"hero\" src=\"{html.escape(entry['hero'])}\" alt=\"{html.escape(entry['name'])}\" loading=\"lazy\">"
        if entry["hero"]
        else ""
    )

    details = []
    if entry["address"]:
        details.append(("地址", entry["address"]))
    if entry["status"]:
        details.append(("營業狀態", entry["status"]))
    if entry["hours"]:
        details.append(("營業資訊", entry["hours"]))
    if entry["phone"]:
        details.append(("電話", entry["phone"]))
    if entry["price"]:
        details.append(("價格", entry["price"]))

    details_list = "\n".join(
        f"<li><strong>{html.escape(label)}：</strong> {html.escape(value)}</li>" for label, value in details
    )

    description = html.escape(entry["description"] or "這裡的肉桂捲值得一試！")

    cta_links = []
    if entry["map_url"]:
        cta_links.append(f"<a class=\"button\" href=\"{html.escape(entry['map_url'])}\">開啟地圖</a>")
    if entry["menu_url"]:
        cta_links.append(f"<a class=\"button\" href=\"{html.escape(entry['menu_url'])}\">線上點餐 / 菜單</a>")

    html_doc = f"""
<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(entry['name'])} | 肉桂捲地圖</title>
  <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
  <header class="header">
    <div class="container">
      <p><a href="../">← 返回列表</a></p>
      <h1>{html.escape(entry['name'])}</h1>
      <p class="lead">{description}</p>
      <div class="meta">
        {'⭐ ' + html.escape(entry['rating']) if entry['rating'] else ''}
        {' · ' + html.escape(entry['reviews']) + ' 則評論' if entry['reviews'] else ''}
        {' · ' + html.escape(entry['category']) if entry['category'] else ''}
      </div>
      <div class="cta-row">{''.join(cta_links)}</div>
    </div>
  </header>
  <main class="container">
    {hero_tag}
    <ul class="details">{details_list}</ul>
  </main>
</body>
</html>
    """

    (page_dir / "index.html").write_text(html_doc, encoding="utf-8")


def main():
    ensure_assets()
    rows = load_rows()
    entries = [build_entry(row) for row in rows]
    write_index(entries)
    for entry in entries:
        write_entry(entry)


if __name__ == "__main__":
    main()

from __future__ import annotations
import csv
import html
import pathlib
import re
from typing import Dict, List

REPO_ROOT = pathlib.Path(__file__).parent
DATA_PATH = REPO_ROOT / "google-2025-12-12.csv"
OUTPUT_DIR = REPO_ROOT / "docs"
ASSETS_DIR = OUTPUT_DIR / "assets"

PLACEHOLDER_IMAGE = "https://via.placeholder.com/640x360?text=Cinnamon+Roll"


def clean_text(value: str) -> str:
    """Normalize the scraped text to make it displayable."""
    if not value:
        return ""
    text = value.replace("\\n", " ").strip().strip("\"")
    text = re.sub(r"^[\uE000-\uF8FF]+", "", text)  # trim private-use icons
    text = text.strip("· ")
    return text


def slugify(name: str, used: set[str]) -> str:
    base = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower() or "roll"
    slug = base
    counter = 2
    while slug in used:
        slug = f"{base}-{counter}"
        counter += 1
    used.add(slug)
    return slug


def gather_highlights(row: Dict[str, str]) -> List[str]:
    keys = [
        "ah5Ghc",
        "ah5Ghc (2)",
        "ah5Ghc (3)",
        "ah5Ghc (4)",
        "ah5Ghc (5)",
        "J8zHNe",
        "AJB7ye",
        "AJB7ye (2)",
        "W4Efsd (6)",
        "W4Efsd (7)",
        "W4Efsd (8)",
        "doJOZc",
    ]
    highlights: List[str] = []
    seen: set[str] = set()
    for key in keys:
        text = clean_text(row.get(key, ""))
        if text and text not in seen and text != "·":
            highlights.append(text)
            seen.add(text)
    return highlights


def load_rolls() -> List[Dict[str, str]]:
    with DATA_PATH.open(encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


def build_assets() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "styles.css").write_text(
        """
:root {
  --bg: #fdf7f2;
  --card: #ffffff;
  --accent: #c97941;
  --text: #2d1f18;
  --muted: #6d5547;
}

* { box-sizing: border-box; }
body {
  font-family: "Inter", "Noto Sans TC", system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  margin: 0;
  padding: 0;
}

a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

header {
  padding: 32px 24px 8px;
  text-align: center;
}

header h1 { margin: 0; font-size: 2.5rem; }
header p { margin: 8px 0 0; color: var(--muted); }

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  padding: 24px;
}

.card {
  background: var(--card);
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.card img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  background: #f2e4da;
}

.card .content {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.meta { color: var(--muted); font-size: 0.95rem; }
.chip {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  background: #f0dfd5;
  color: var(--accent);
  font-weight: 600;
  margin-right: 6px;
}

.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.button {
  padding: 10px 14px;
  border-radius: 12px;
  background: var(--accent);
  color: white;
  font-weight: 700;
  text-decoration: none;
  transition: transform 0.1s ease, box-shadow 0.1s ease;
}

.button.secondary {
  background: #f0dfd5;
  color: var(--accent);
}

.button:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(0,0,0,0.12); }

.page {
  max-width: 960px;
  margin: 0 auto;
  padding: 32px 24px 64px;
}

.hero-image {
  width: 100%;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.08);
  background: #f2e4da;
}

.hero-image img {
  width: 100%;
  height: 360px;
  object-fit: cover;
}

.facts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
  margin: 16px 0;
}

.fact {
  padding: 12px 14px;
  border-radius: 12px;
  background: #fff7f1;
}

.fact strong { display: block; color: var(--muted); margin-bottom: 4px; font-size: 0.9rem; }

.list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 8px;
}

.list li {
  padding: 12px 14px;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}

.back-link { margin-top: 24px; display: inline-block; }

.footer { text-align: center; color: var(--muted); padding: 16px 0 32px; font-size: 0.95rem; }
""",
        encoding="utf-8",
    )


def render_index(rolls: List[Dict[str, str]]) -> None:
    cards = []
    for roll in rolls:
        card = f"""
      <article class=\"card\">
        <img src=\"{html.escape(roll['image'])}\" alt=\"{html.escape(roll['name'])}\" />
        <div class=\"content\">
          <div>
            <div class=\"chip\">{html.escape(roll['rating'])} ★</div>
            <div class=\"chip\">{html.escape(roll['category'])}</div>
          </div>
          <h2><a href=\"{roll['slug']}.html\">{html.escape(roll['name'])}</a></h2>
          <p class=\"meta\">{html.escape(roll['address'])}</p>
        </div>
      </article>
    """
        cards.append(card)

    html_content = f"""
<!DOCTYPE html>
<html lang=\"zh-Hant\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Cinnamon Rolls · GitHub Pages</title>
  <link rel=\"stylesheet\" href=\"assets/styles.css\" />
</head>
<body>
  <header>
    <h1>肉桂捲地圖</h1>
    <p>在 GitHub Pages 上快速瀏覽每一款肉桂捲資訊。</p>
  </header>
  <main class=\"grid\">
    {''.join(cards)}
  </main>
  <div class=\"footer\">共 {len(rolls)} 間店家 · 依名稱排序</div>
</body>
</html>
"""
    (OUTPUT_DIR / "index.html").write_text(html_content, encoding="utf-8")


def render_roll_page(roll: Dict[str, str]) -> None:
    highlights_html = "".join(
        f"<li>{html.escape(item)}</li>" for item in roll["highlights"]
    ) or "<li>還沒有額外的重點資訊。</li>"

    buttons = []
    if roll.get("map_url"):
        buttons.append(f"<a class='button' href='{html.escape(roll['map_url'])}' target='_blank' rel='noopener'>地圖 / 導航</a>")
    if roll.get("order_url"):
        buttons.append(f"<a class='button secondary' href='{html.escape(roll['order_url'])}' target='_blank' rel='noopener'>線上點餐 / 連結</a>")

    html_content = f"""
<!DOCTYPE html>
<html lang=\"zh-Hant\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{html.escape(roll['name'])} · 肉桂捲</title>
  <link rel=\"stylesheet\" href=\"assets/styles.css\" />
</head>
<body>
  <div class=\"page\">
    <div class=\"hero-image\"><img src=\"{html.escape(roll['image'])}\" alt=\"{html.escape(roll['name'])}\" /></div>
    <h1>{html.escape(roll['name'])}</h1>
    <div class=\"button-row\">{''.join(buttons)}</div>

    <section class=\"facts\">
      <div class=\"fact\"><strong>評分</strong>{html.escape(roll['rating'])} / 5 · {html.escape(roll['reviews'])}</div>
      <div class=\"fact\"><strong>分類</strong>{html.escape(roll['category'])}</div>
      <div class=\"fact\"><strong>地址</strong>{html.escape(roll['address'])}</div>
      <div class=\"fact\"><strong>電話</strong>{html.escape(roll['phone'])}</div>
      <div class=\"fact\"><strong>營業狀態</strong>{html.escape(roll['status'])}</div>
      <div class=\"fact\"><strong>價位 / 備註</strong>{html.escape(roll['price'])}</div>
    </section>

    <h2>重點與留言</h2>
    <ul class=\"list\">{highlights_html}</ul>

    <a class=\"back-link\" href=\"index.html\">← 回到列表</a>
  </div>
</body>
</html>
"""
    (OUTPUT_DIR / f"{roll['slug']}.html").write_text(html_content, encoding="utf-8")


def main() -> None:
    rolls_raw = load_rolls()
    used_slugs: set[str] = set()
    processed: List[Dict[str, str]] = []

    for row in sorted(rolls_raw, key=lambda r: clean_text(r.get("qBF1Pd", ""))):
        name = clean_text(row.get("qBF1Pd", "")) or "未命名肉桂捲"
        slug = slugify(name, used_slugs)
        rating = clean_text(row.get("MW4etd", "")) or "N/A"
        reviews = clean_text(row.get("UY7F9", "")).strip("() ") or "尚無評論"
        category = clean_text(row.get("W4Efsd", "")) or "未分類"
        address = clean_text(row.get("W4Efsd (3)", "")) or "地址未提供"
        status = clean_text(row.get("W4Efsd (4)", ""))
        hours = clean_text(row.get("W4Efsd (5)", ""))
        status_text = " · ".join([part for part in (status, hours) if part]) or "尚未提供營業資訊"
        phone = clean_text(row.get("UsdlK", "")) or "—"
        price = clean_text(row.get("AJB7ye (2)", "")) or clean_text(row.get("AJB7ye", "")) or "—"
        image = clean_text(row.get("FQ2IWe src", "")) or clean_text(row.get("Jn12ke src", "")) or PLACEHOLDER_IMAGE
        map_url = clean_text(row.get("hfpxzc href", ""))
        order_url = clean_text(row.get("A1zNzb href", "")) or clean_text(row.get("A1zNzb href (2)", ""))
        highlights = gather_highlights(row)

        processed.append(
            {
                "slug": slug,
                "name": name,
                "rating": rating,
                "reviews": reviews,
                "category": category,
                "address": address,
                "status": status_text,
                "phone": phone,
                "price": price,
                "image": image or PLACEHOLDER_IMAGE,
                "map_url": map_url,
                "order_url": order_url,
                "highlights": highlights,
            }
        )

    OUTPUT_DIR.mkdir(exist_ok=True)
    build_assets()
    render_index(processed)
    for roll in processed:
        render_roll_page(roll)


if __name__ == "__main__":
    main()

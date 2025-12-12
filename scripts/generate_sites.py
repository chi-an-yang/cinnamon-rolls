import csv
import html
import re
from pathlib import Path

DATA_FILE = Path('google-2025-12-12.csv')
OUTPUT_ROOT = Path('docs')
ROLLS_DIR = OUTPUT_ROOT / 'rolls'


def slugify(name: str, existing: set[str]) -> str:
    base = re.sub(r'[^a-zA-Z0-9]+', '-', name.strip().lower()).strip('-') or 'roll'
    slug = base
    counter = 2
    while slug in existing:
        slug = f"{base}-{counter}"
        counter += 1
    existing.add(slug)
    return slug


def clean_text(value: str) -> str:
    if value is None:
        return ''
    cleaned = value.replace('\n', ' ').replace('\uea74', '').strip()
    return cleaned.strip('·').strip()


def normalize_services(row: dict) -> list[str]:
    candidates = [
        row.get('ah5Ghc'),
        row.get('ah5Ghc (2)'),
        row.get('J8zHNe'),
        row.get('bbPy1'),
        row.get('AJB7ye'),
        row.get('AJB7ye (2)'),
    ]
    services = []
    for item in candidates:
        text = clean_text(item)
        if text and text not in {'', '·'}:
            services.append(text)
    return services


def build_review_snippet(row: dict) -> str:
    parts = [row.get('ah5Ghc (3)', ''), row.get('ah5Ghc (4)', ''), row.get('ah5Ghc (5)', '')]
    snippet = ' '.join(clean_text(p) for p in parts if p)
    return snippet.strip()


def select_image(row: dict) -> str:
    primary = clean_text(row.get('FQ2IWe src', ''))
    fallback = clean_text(row.get('Jn12ke src', ''))
    placeholder = 'https://placehold.co/600x400?text=Cinnamon+Roll'
    return primary or fallback or placeholder


def parse_rows() -> list[dict]:
    with DATA_FILE.open(encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def render_roll_page(roll: dict, slug: str):
    roll_dir = ROLLS_DIR / slug
    roll_dir.mkdir(parents=True, exist_ok=True)
    map_link = clean_text(roll.get('hfpxzc href', ''))
    menu_link = clean_text(roll.get('A1zNzb href', '')) or clean_text(roll.get('A1zNzb href (2)', ''))
    review_snippet = build_review_snippet(roll)
    services = normalize_services(roll)
    image = select_image(roll)

    html_content = f"""<!DOCTYPE html>
<html lang=\"zh-Hant\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{html.escape(clean_text(roll['qBF1Pd']))}</title>
  <link rel=\"stylesheet\" href=\"../style.css\" />
</head>
<body>
  <header class=\"site-header\">
    <div class=\"container header-inner\">
      <a href=\"../index.html\" class=\"logo\">肉桂捲地圖</a>
      <span class=\"breadcrumb\">{html.escape(clean_text(roll['qBF1Pd']))}</span>
    </div>
  </header>

  <main class=\"container\">
    <section class=\"hero\">
      <img src=\"{html.escape(image)}\" alt=\"{html.escape(clean_text(roll['qBF1Pd']))}\" />
      <div>
        <h1>{html.escape(clean_text(roll['qBF1Pd']))}</h1>
        <p class=\"meta\">{html.escape(clean_text(roll.get('W4Efsd', '')))} · {html.escape(clean_text(roll.get('W4Efsd (3)', '')))} </p>
        <p class=\"rating\">評分 {html.escape(clean_text(roll.get('MW4etd', 'N/A')))} <span class=\"muted\">{html.escape(clean_text(roll.get('UY7F9', '')))}</span></p>
        <p class=\"status\">{html.escape(clean_text(roll.get('W4Efsd (4)', '')))} {html.escape(clean_text(roll.get('W4Efsd (5)', '')))}</p>
        <p class=\"contact\">{html.escape(clean_text(roll.get('UsdlK', '')))}</p>
        <div class=\"actions\">
          {f"<a class='button' href='{html.escape(map_link)}' target='_blank' rel='noreferrer'>查看地圖</a>" if map_link else ''}
          {f"<a class='button secondary' href='{html.escape(menu_link)}' target='_blank' rel='noreferrer'>線上點餐 / 菜單</a>" if menu_link else ''}
        </div>
      </div>
    </section>

    <section class=\"card\">
      <h2>服務與特色</h2>
        <div class=\"chips\">
          {''.join(f"<span class='chip'>{html.escape(item)}</span>" for item in services) or "<p class='muted'>沒有提供額外資訊。</p>"}
        </div>
    </section>

    <section class=\"card\">
      <h2>最近評論摘錄</h2>
      <p>{html.escape(review_snippet) or '尚無評論摘錄'}</p>
    </section>
  </main>

  <footer class=\"site-footer\">
    <div class=\"container\">
      <p>以 Google 地圖資料建立的肉桂捲列表，透過 GitHub Pages 提供靜態網站。</p>
    </div>
  </footer>
</body>
</html>
"""

    (roll_dir / 'index.html').write_text(html_content, encoding='utf-8')


def render_index(rolls: list[dict], slugs: dict[str, str]):
    cards_html = []
    for roll in rolls:
        name = clean_text(roll['qBF1Pd'])
        slug = slugs[name]
        image = select_image(roll)
        rating = clean_text(roll.get('MW4etd', ''))
        reviews = clean_text(roll.get('UY7F9', ''))
        category = clean_text(roll.get('W4Efsd', ''))
        address = clean_text(roll.get('W4Efsd (3)', ''))
        badge = clean_text(roll.get('W4Efsd (4)', ''))
        snippet = build_review_snippet(roll)
        services = normalize_services(roll)[:3]

        cards_html.append(f"""
        <article class=\"card\">
          <img class=\"thumb\" src=\"{html.escape(image)}\" alt=\"{html.escape(name)}\" />
          <div class=\"card-body\">
            <header class=\"card-header\">
              <h2><a href=\"rolls/{slug}/index.html\">{html.escape(name)}</a></h2>
              <p class=\"rating\">{html.escape(rating)} <span class=\"muted\">{html.escape(reviews)}</span></p>
            </header>
            <p class=\"meta\">{html.escape(category)}</p>
            <p class=\"meta\">{html.escape(address)}</p>
            <p class=\"status\">{html.escape(badge)}</p>
            <p class=\"snippet\">{html.escape(snippet) or '尚無評論摘錄'}</p>
            <div class=\"chips\">{''.join(f"<span class='chip'>{html.escape(s)}</span>" for s in services)}</div>
          </div>
        </article>
        """)

    index_html = f"""<!DOCTYPE html>
<html lang=\"zh-Hant\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>肉桂捲地圖 · GitHub Pages</title>
  <link rel=\"stylesheet\" href=\"style.css\" />
</head>
<body>
  <header class=\"site-header\">
    <div class=\"container header-inner\">
      <h1 class=\"logo\">肉桂捲地圖</h1>
      <p class=\"subtitle\">利用 GitHub Pages 建立的靜態網站，每家肉桂捲都有自己的頁面。</p>
    </div>
  </header>
  <main class=\"container grid\">
    {''.join(cards_html)}
  </main>
  <footer class=\"site-footer\">
    <div class=\"container\">
      <p>資料來源自 google-2025-12-12.csv · 由自動產生腳本輸出</p>
    </div>
  </footer>
</body>
</html>
"""

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUTPUT_ROOT / 'index.html').write_text(index_html, encoding='utf-8')


def main():
    OUTPUT_ROOT.mkdir(exist_ok=True)
    ROLLS_DIR.mkdir(parents=True, exist_ok=True)

    rows = parse_rows()
    slugs: dict[str, str] = {}
    existing_slugs: set[str] = set()

    for row in rows:
        name = clean_text(row.get('qBF1Pd', ''))
        if not name:
            continue
        slug = slugify(name, existing_slugs)
        slugs[name] = slug
        render_roll_page(row, slug)

    render_index(rows, slugs)


if __name__ == '__main__':
    main()

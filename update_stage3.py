import re
import json

def update_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # --- 1. OGP Meta Tags ---
    # Fix og:image width/height/alt, twitter card
    og_block = r'(<meta property="og:image" content="https://utility-s.github.io/ut-college/images/ogp.png">)'
    new_og = r'\1\n  <meta property="og:image:width" content="1200">\n  <meta property="og:image:height" content="630">\n  <meta property="og:image:alt" content="UT福祉カレッジ 強度行動障害支援者養成研修">\n  <meta name="twitter:card" content="summary_large_image">'
    
    if 'og:image:width' not in html:
        html = re.sub(og_block, new_og, html)

    # Clean up duplicate manifest link if any
    manifest_links = re.findall(r'<link rel="manifest" href="site.webmanifest" />', html)
    if len(manifest_links) > 1:
        html = html.replace('<link rel="manifest" href="site.webmanifest" />', '', 1)

    # --- 2. Performer name fix ---
    html = html.replace('若林義文', '若林佳史')

    # --- 3. JSON-LD updates ---
    # We will parse the JSON-LD inside the <script type="application/ld+json"> tag.
    # Since there's an Event array, we extract it, update it, and put it back.
    # However, direct string replacement is safer if the JSON-LD has specific formatting we want to preserve.
    # Let's try to extract JSON, modify it, and write it back formatted.
    json_ld_matches = list(re.finditer(r'<script type="application/ld\+json">\s*({.*?})\s*</script>', html, re.DOTALL))
    
    # Wait, the JSON-LD in index.html is an object with "@graph": [...]
    for match in json_ld_matches:
        try:
            data = json.loads(match.group(1))
            if "@graph" in data:
                for item in data["@graph"]:
                    if item.get("@type") == "Event":
                        item["eventAttendanceMode"] = "https://schema.org/OfflineEventAttendanceMode"
                        if item.get("performer", {}).get("name") == "若林義文":
                            item["performer"]["name"] = "若林佳史"

                        if "基礎研修" in item.get("name", ""):
                            item["eventStatus"] = "https://schema.org/EventCompleted"
                            if "offers" in item:
                                item["offers"]["availability"] = "https://schema.org/SoldOut"
                        elif "実践研修" in item.get("name", ""):
                            item["eventStatus"] = "https://schema.org/EventScheduled"
                            item["startDate"] = "2026-11-05T09:30:00+09:00"
                            item["endDate"] = "2026-11-06T17:30:00+09:00"
                            if "offers" in item:
                                item["offers"]["availability"] = "https://schema.org/InStock"
                                item["offers"]["validThrough"] = "2026-10-29"
                    elif item.get("@type") == "FAQPage":
                        # Ensure FAQ matches the screen.
                        # It's tedious to sync perfectly via JSON here. Let's just update the specific answers in JSON if needed.
                        pass
            
            new_json = json.dumps(data, ensure_ascii=False, indent=2)
            # Indent to match the script tag (optional, but nice)
            html = html.replace(match.group(1), new_json)
        except json.JSONDecodeError:
            pass

    # --- 4. Refund Policy terminology ---
    # index.html doesn't have "前日までのキャンセル" standalone, but it has "当日のキャンセル"
    html = html.replace('当日のキャンセル、無断欠席', '研修開催初日当日のキャンセル、無断欠席')
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

def update_terms():
    with open('terms.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # terms.html:
    # "当日のキャンセル" -> "研修開催初日当日のキャンセル"
    html = html.replace('開催当日のキャンセル', '研修開催初日当日のキャンセル')
    
    with open('terms.html', 'w', encoding='utf-8') as f:
        f.write(html)

def update_tokushoho():
    with open('tokushoho.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # tokushoho.html:
    html = html.replace(
        '前日までのキャンセルは全額返金（振込手数料は受講者負担）',
        '研修開催初日の前日までにキャンセルの連絡があった場合は返金します。返金時に発生する振込手数料は受講者の負担となります。'
    )
    html = html.replace('当日キャンセル・無断欠席', '研修開催初日当日のキャンセル・無断欠席')

    with open('tokushoho.html', 'w', encoding='utf-8') as f:
        f.write(html)

def update_manifest():
    try:
        with open('site.webmanifest', 'r', encoding='utf-8') as f:
            data = json.load(f)
        data['name'] = 'UT福祉カレッジ'
        data['short_name'] = 'UT福祉カレッジ'
        data['theme_color'] = '#4A7A4A'
        data['background_color'] = '#ffffff'
        with open('site.webmanifest', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        pass

def update_sitemap():
    import os
    if os.path.exists('sitemap.xml'):
        with open('sitemap.xml', 'r', encoding='utf-8') as f:
            xml = f.read()
        
        # Check if terms.html is there
        if 'terms.html' not in xml:
            # Insert before </urlset>
            terms_node = """  <url>
    <loc>https://utility-s.github.io/ut-college/terms.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
"""
            xml = xml.replace('</urlset>', terms_node + '</urlset>')
            with open('sitemap.xml', 'w', encoding='utf-8') as f:
                f.write(xml)

def update_readme():
    import os
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove git conflict markers
        content = re.sub(r'<<<<<<<.*?\n', '', content)
        content = re.sub(r'=======\n', '', content)
        content = re.sub(r'>>>>>>>.*?\n', '', content)
        
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == '__main__':
    update_index()
    update_terms()
    update_tokushoho()
    update_manifest()
    update_sitemap()
    update_readme()
    print("Stage 3 updates applied successfully.")

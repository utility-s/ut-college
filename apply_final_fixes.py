import re
import os
import glob

# 1. Update index.html dates and add new event to JSON-LD
index_file = 'index.html'
with open(index_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Update hero schedule dates
html = html.replace('基礎研修：2026年2月5日(木)〜6日(金)', '基礎研修：2026年8月6日(木)〜7日(金)')
html = html.replace('実践研修：2026年3月12日(木)〜13日(金)', '実践研修：2026年11月5日(木)〜6日(金)')

# Update JSON-LD for 基礎研修
html = html.replace('"startDate": "2026-02-05"', '"startDate": "2026-08-06"')
html = html.replace('"endDate": "2026-02-06"', '"endDate": "2026-08-07"')

# Check if 実践研修 is in JSON-LD, if not, add it
if '"name": "東京都強度行動障害支援者養成研修（実践研修）"' not in html:
    new_event = '''      {
        "@type": "Event",
        "name": "東京都強度行動障害支援者養成研修（実践研修）",
        "startDate": "2026-11-05",
        "endDate": "2026-11-06",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "eventStatus": "https://schema.org/EventScheduled",
        "location": {
          "@type": "Place",
          "name": "山本ビル3F",
          "address": {
            "@type": "PostalAddress",
            "streetAddress": "熊川1708-1 山本ビル3F",
            "addressLocality": "福生市",
            "addressRegion": "東京都",
            "addressCountry": "JP"
          }
        }
      },'''
    # Insert it right after the first event
    insert_pattern = re.compile(r'("name": "東京都強度行動障害支援者養成研修（基礎研修）".*?\},)', re.DOTALL)
    html = insert_pattern.sub(r'\1\n' + new_event, html)

# Insert new texts in HERO section
# 1. 受講料 21,500円 below hero-schedule
schedule_insert = '''        <div class="hero-schedule">
          <p>【次回開催日程】 ※対面（会場）開催のみとなります</p>
          <p><span class="date">基礎研修：2026年8月6日(木)〜7日(金)</span></p>
          <p><span class="date">実践研修：2026年11月5日(木)〜6日(金)</span></p>
        </div>
        <p style="margin-top:10px; font-weight:700;">受講料 21,500円（税込・テキスト代込）</p>'''

# Currently it looks like:
#         <div class="hero-schedule">
#           <p>【次回開催日程】 ※対面（会場）開催のみとなります</p>
#           <p><span class="date">基礎研修：2026年8月6日(木)〜7日(金)</span></p>
#           <p><span class="date">実践研修：2026年11月5日(木)〜6日(金)</span></p>
#         </div>
html = re.sub(r'<div class="hero-schedule">.*?</div>', schedule_insert, html, flags=re.DOTALL)

# 2. 定員バッジ near HERO CTA
cta_insert = '''<a href="https://docs.google.com/forms/d/e/1FAIpQLSePDVOsYhIBRIPuHGyegQP8HumM7EN6QQeE5Xfd3BGoet1c9A/viewform" target="_blank" rel="noopener" class="btn btn-cta" style="font-size: 1.3rem; padding: 20px 60px;">受講をお申し込む</a>
          <p class="note mt-20" style="color:#fff; font-weight:700;">各回 定員15名（最大16名）｜定員に達し次第締切</p>'''
html = html.replace('<a href="https://docs.google.com/forms/d/e/1FAIpQLSePDVOsYhIBRIPuHGyegQP8HumM7EN6QQeE5Xfd3BGoet1c9A/viewform" target="_blank" rel="noopener" class="btn btn-cta" style="font-size: 1.3rem; padding: 20px 60px;">受講をお申し込む</a>', cta_insert)

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Logo height and Hamburger update in all HTML files
html_files = glob.glob('*.html')
for f_path in html_files:
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Logo height
    content = content.replace('<img src="images/logo.png" alt="UT福祉カレッジ" width="200" height="40">',
                              '<img src="images/logo.png" alt="UT福祉カレッジ" width="260" height="52" style="width: auto; height: 52px;">')
    
    # Add Hamburger
    hamburger_html = '''<button class="hamburger" id="hamburger" aria-label="メニューを開く" aria-expanded="false">
  <span></span><span></span><span></span>
</button>
      <nav class="header-nav">'''
    if 'id="hamburger"' not in content:
        content = content.replace('<nav class="header-nav">', hamburger_html)

    # Add Script
    script_html = '''<script>
  const ham = document.getElementById('hamburger');
  const nav = document.querySelector('.header-nav');
  if (ham && nav) {
    ham.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      ham.setAttribute('aria-expanded', open);
    });
    nav.querySelectorAll('a').forEach(a =>
      a.addEventListener('click', () => nav.classList.remove('is-open'))
    );
  }
</script>
</body>'''
    if "const ham = document.getElementById('hamburger');" not in content:
        content = content.replace('</body>', script_html)

    with open(f_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 3. Update CSS
css_file = 'css/style.css'
with open(css_file, 'r', encoding='utf-8') as f:
    css_content = f.read()

css_content = css_content.replace('--header-height: 70px;', '--header-height: 80px;')
css_content = css_content.replace('.header .logo img {\n  height: 40px;\n}', '.header .logo img {\n  height: 52px;\n}')
css_content = css_content.replace('.header .logo img { height: 40px; }', '.header .logo img { height: 52px; }')

# Fix btn-cta color and override
if '.btn-cta { color: #3a2f00 !important; font-weight: 700; }' not in css_content:
    css_content += '\n.btn-cta { color: #3a2f00 !important; font-weight: 700; }\n'

new_responsive_css = '''
/* ========== スクロール時にヘッダーへ隠れない ========== */
section[id], [id] { scroll-margin-top: 90px; }

/* ========== レスポンシブ対応 ========== */
@media (max-width: 1024px) {
  .section { padding: 60px 0; }
  .hero-title { font-size: 2.1rem; }
  .header-nav-list { gap: 14px; }
  .header-nav-list a { font-size: 0.88rem; }
}
@media (max-width: 768px) {
  :root { --header-height: 64px; }
  .section { padding: 48px 0; }
  .container { padding: 0 16px; }
  body { line-height: 1.7; }
  .empathy-list, .benefit-cols, .reason-grid, .course-compare,
  .service-cards { grid-template-columns: 1fr; gap: 16px; }
  .hero-title { font-size: 1.7rem; line-height: 1.45; }
  .hero-subtitle { font-size: 1rem; }
  .hero-schedule { display: block; padding: 16px; }
  .hero .btn { width: 100%; padding: 16px 20px !important; font-size: 1.1rem !important; }
  .teacher-profile { flex-direction: column; gap: 20px; padding: 24px; }
  .teacher-img { flex: none; max-width: 220px; margin: 0 auto; }
  .section-title { font-size: 1.4rem; }
  .header-nav { display: none; }
  .hamburger { display: flex; }
  .header-nav.is-open {
    display: flex; flex-direction: column; align-items: stretch;
    position: fixed; top: var(--header-height); left: 0; width: 100%;
    background: #fff; padding: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.1); gap: 0;
  }
  .header-nav.is-open .header-nav-list { flex-direction: column; gap: 0; }
  .header-nav.is-open .header-nav-list li { border-bottom: 1px solid var(--color-border); }
  .header-nav.is-open .header-nav-list a { display: block; padding: 14px 8px; }
  .header-nav.is-open .header-cta { margin-top: 12px; text-align: center; }
}
@media (max-width: 380px) {
  .hero-title { font-size: 1.45rem; }
  .btn { padding: 13px 24px; font-size: 1rem; }
}

/* ハンバーガーボタン（PCでは非表示） */
.hamburger {
  display: none; flex-direction: column; justify-content: center; gap: 5px;
  width: 44px; height: 44px; background: none; border: none; cursor: pointer; padding: 0;
}
.hamburger span {
  display: block; width: 26px; height: 3px;
  background: var(--color-main); border-radius: 2px; transition: 0.3s;
}
'''
if '/* ========== レスポンシブ対応 ========== */' not in css_content:
    css_content += new_responsive_css

with open(css_file, 'w', encoding='utf-8') as f:
    f.write(css_content)

print("Applied responsive styles and UI fixes.")

import os
import re

html_files = ['index.html', 'services.html', 'privacy.html', 'terms.html', 'tokushoho.html']

new_header = '''<nav class="header-nav">
        <ul class="header-nav-list">
          <li><a href="index.html">ホーム</a></li>
          <li><a href="index.html#about">研修について</a></li>
          <li><a href="index.html#teacher">講師紹介</a></li>
          <li><a href="index.html#access">会場・アクセス</a></li>
          <li><a href="services.html">研修後のサポート</a></li>
          <li class="has-dropdown">
            <a href="javascript:void(0)" class="dropdown-toggle">法務・学則 ▾</a>
            <ul class="dropdown-menu">
              <li><a href="terms.html">利用規約</a></li>
              <li><a href="privacy.html">個人情報保護方針</a></li>
              <li><a href="docs/gakusoku-kiso.pdf" target="_blank" rel="noopener">基礎研修 学則(PDF)</a></li>
              <li><a href="docs/gakusoku-jissen.pdf" target="_blank" rel="noopener">実践研修 学則(PDF)</a></li>
            </ul>
          </li>
        </ul>
        <a href="index.html#apply" class="btn btn-cta header-cta">研修のお申込み</a>
      </nav>'''

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace header nav
    content = re.sub(r'<nav class="header-nav">.*?</nav>', new_header, content, flags=re.DOTALL)
    
    # Replace mailto
    content = content.replace('href="mailto:utility.co.jp.tokyo@gmail.com"', 'href="mailto:utility.co.jp.tokyo@gmail.com?subject=お問い合わせ"')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Headers and mailto updated.")

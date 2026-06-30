import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Benefits section
old_benefit = '<p class="note mt-20">※算定可否はサービス種別・自治体運用・対象者要件等により異なりますので、事前に指定権者へご確認ください。</p>'
new_benefit = '<p class="mt-20">修了証は研修修了後すみやかに発行します。加算申請をお急ぎの方は、当日発行も可能な限り対応いたします（事前にご相談ください）。</p>\n            <p class="note mt-20">※算定可否はサービス種別・自治体運用・対象者要件等により異なりますので、事前に指定権者へご確認ください。</p>'
html = html.replace(old_benefit, new_benefit)

# 2. Visible FAQ
old_faq = '<div class="faq-answer"><p>全カリキュラムを修了した最終日に、原則として会場で直接交付いたします。</p></div>'
new_faq = '<div class="faq-answer"><p>全カリキュラムを修了した最終日に、原則として会場で直接交付いたします。加算申請などでお急ぎの場合は、可能な限り当日発行で対応いたしますので、お申込み時または受講前にご相談ください。</p></div>'
html = html.replace(old_faq, new_faq)

# 3. JSON-LD FAQ
old_jsonld = '''          {
            "@type": "Question",
            "name": "研修の受講時間はどのくらいですか？",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "基礎研修・実践研修ともに各2日間、計12時間のカリキュラムです。開催時間は両日とも9:30〜17:30（昼休憩1時間を含む）です。"
            }
          }
        ]'''
new_jsonld = '''          {
            "@type": "Question",
            "name": "研修の受講時間はどのくらいですか？",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "基礎研修・実践研修ともに各2日間、計12時間のカリキュラムです。開催時間は両日とも9:30〜17:30（昼休憩1時間を含む）です。"
            }
          },
          {
            "@type": "Question",
            "name": "修了証はいつもらえますか？",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "全カリキュラムを修了した最終日に、原則として会場で直接交付いたします。加算申請などでお急ぎの場合は、可能な限り当日発行で対応いたしますので、お申込み時または受講前にご相談ください。"
            }
          }
        ]'''
html = html.replace(old_jsonld, new_jsonld)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML and JSON-LD updated.")

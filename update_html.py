import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Benefits section
old_benefit = '''            <p class="mt-20">修了証は研修修了後すみやかに発行します。加算申請をお急ぎの方は、当日発行も可能な限り対応いたします（事前にご相談ください）。</p>
            <p class="note mt-20">※算定可否はサービス種別・自治体運用・対象者要件等により異なりますので、事前に指定権者へご確認ください。</p>'''
new_benefit = '''            <p class="mt-20">修了証は研修修了後すみやかに発行します。加算申請をお急ぎの方は、当日発行も可能な限り対応いたします（事前にご相談ください）。</p>
            <p class="mt-20">本研修は、重度障害者支援加算や体制整備の要件を満たすだけでなく、行動援護のヘルパーとして従事する際にも必須の研修です（あわせて、知的障害・精神障害のある方への直接支援について1年以上の実務経験が要件となります）。</p>
            <p class="note mt-20">※算定可否はサービス種別・自治体運用・対象者要件等により異なりますので、事前に指定権者へご確認ください。</p>'''
html = html.replace(old_benefit, new_benefit)

# 2. Visible FAQ
old_faq = '''          <div class="faq-item">
            <div class="faq-question">修了証はいつもらえますか？</div>
            <div class="faq-answer"><p>全カリキュラムを修了した最終日に、原則として会場で直接交付いたします。加算申請などでお急ぎの場合は、可能な限り当日発行で対応いたしますので、お申込み時または受講前にご相談ください。</p></div>
          </div>'''
new_faq = '''          <div class="faq-item">
            <div class="faq-question">実践研修の申込時に必要なものはありますか？</div>
            <div class="faq-answer"><p>実践研修は基礎研修の修了が必須要件です。お申込みの際には、基礎研修の修了証のご提出をお願いしております（他機関でも同様に義務付けられており、不正防止および事業者指定取消の防止を目的としています）。</p></div>
          </div>
          <div class="faq-item">
            <div class="faq-question">修了証はいつもらえますか？</div>
            <div class="faq-answer"><p>全カリキュラムを修了した最終日に、原則として会場で修了証の原本を直接お渡しします。PDFデータをご希望の場合は、個別にご相談のうえ対応を検討いたします。</p></div>
          </div>'''
html = html.replace(old_faq, new_faq)

# 3. JSON-LD FAQ
old_jsonld = '''          {
            "@type": "Question",
            "name": "修了証はいつもらえますか？",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "全カリキュラムを修了した最終日に、原則として会場で直接交付いたします。加算申請などでお急ぎの場合は、可能な限り当日発行で対応いたしますので、お申込み時または受講前にご相談ください。"
            }
          }'''
new_jsonld = '''          {
            "@type": "Question",
            "name": "実践研修の申込時に必要なものはありますか？",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "実践研修は基礎研修の修了が必須要件です。お申込みの際には、基礎研修の修了証のご提出をお願いしております（他機関でも同様に義務付けられており、不正防止および事業者指定取消の防止を目的としています）。"
            }
          },
          {
            "@type": "Question",
            "name": "修了証はいつもらえますか？",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "全カリキュラムを修了した最終日に、原則として会場で修了証の原本を直接お渡しします。PDFデータをご希望の場合は、個別にご相談のうえ対応を検討いたします。"
            }
          }'''
html = html.replace(old_jsonld, new_jsonld)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML updated.")

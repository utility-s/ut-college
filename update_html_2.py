import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Benefits section
old_benefit = '''            <ul>
              <li>行動を「状態」として客観的に理解できる</li>
              <li>環境を本人に合わせる視点と具体策の習得</li>
              <li>支援の属人化を防ぎ、チーム支援を可能に</li>
              <li>現場のストレス軽減と虐待リスクの低減</li>
            </ul>
          </div>
          <div class="benefit-card">
            <h3>報酬面・体制面のメリット</h3>
            <p>研修修了者は以下の要件等に活用できます。</p>
            <ul>
              <li>重度障害者支援加算の要件</li>
              <li>強度行動障害児支援加算等の要件</li>
              <li>専門的な支援体制を備えた職員配置の整備</li>
            </ul>
            <p class="mt-20">修了証は研修修了後すみやかに発行します。加算申請をお急ぎの方は、当日発行も可能な限り対応いたします（事前にご相談ください）。</p>
            <p class="mt-20">本研修は、重度障害者支援加算や体制整備の要件を満たすだけでなく、行動援護のヘルパーとして従事する際にも必須の研修です（あわせて、知的障害・精神障害のある方への直接支援について1年以上の実務経験が要件となります）。</p>
            <p class="note mt-20">※算定可否はサービス種別・自治体運用・対象者要件等により異なりますので、事前に指定権者へご確認ください。</p>'''

new_benefit = '''            <ul>
              <li>行動を「状態」として客観的に理解できる：主観に頼らず、行動の背景を捉える視点が身につきます。</li>
              <li>環境を本人に合わせる視点と具体策の習得：構造化など、明日から使える支援技術を学べます。</li>
              <li>支援の属人化を防ぎ、チーム支援を可能に：担当者以外でも一貫した対応ができる体制づくりに役立ちます。</li>
              <li>現場のストレス軽減と虐待リスクの低減：適切な対応により、支援者・利用者双方の負担を軽減します。</li>
            </ul>
          </div>
          <div class="benefit-card">
            <h3>報酬面・体制面のメリット</h3>
            <p>研修修了者は以下の要件等に活用できます。</p>
            <ul>
              <li>重度障害者支援加算の要件</li>
              <li>強度行動障害児支援加算等の要件</li>
              <li>専門的な支援体制を備えた職員配置の整備</li>
            </ul>
            <p class="note mt-20">※算定可否はサービス種別・自治体運用・対象者要件等により異なりますので、事前に指定権者へご確認ください。</p>'''
html = html.replace(old_benefit, new_benefit)

# 2. Target Audience section
old_audience = '''          <p class="note mt-20"><strong>【重要】 実践研修は、基礎研修を修了した方のみ受講可能です。</strong></p>'''
new_audience = '''          <p class="mt-20">本研修は、重度障害者支援加算や体制整備の要件を満たすほか、行動援護のヘルパーとして従事する際にも必須の研修です（行動援護には、知的障害・精神障害のある方への直接支援について1年以上の実務経験も要件となります）。</p>
          <p class="note mt-20">
            <strong>【重要】 実践研修は、基礎研修を修了した方のみ受講可能です。</strong><br>
            <strong>【重要】実践研修をお申込みの際は、基礎研修の修了証のご提出が必須です。</strong>
          </p>'''
html = html.replace(old_audience, new_audience)

# 3. Practical Course Card Emphasis
old_card = '''              <span>基礎研修修了者対象</span>
              <p>より高度なチーム支援やアセスメントを学ぶためのステップアップ研修です。</p>'''
new_card = '''              <span>基礎研修修了者対象</span>
              <p><strong>※お申込み時に基礎研修の修了証のご提出が必須です。</strong></p>
              <p>より高度なチーム支援やアセスメントを学ぶためのステップアップ研修です。</p>'''
html = html.replace(old_card, new_card)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML layout updated successfully.")

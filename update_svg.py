import os
import re

# SVGs
svg_worry = '<div style="text-align:center"><svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#4A7A4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:20px"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"></path><path d="M8 10h.01"></path><path d="M12 10h.01"></path><path d="M16 10h.01"></path></svg></div>'
svg_team = '<div style="text-align:center"><svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#4A7A4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:20px"><path d="M3 3v18h18"></path><path d="m19 9-5 5-4-4-3 3"></path><path d="M14 9h5v5"></path></svg></div>'
svg_form = '<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#4A7A4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="display:block;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><path d="M14 2v6h6"></path><path d="M16 13H8"></path><path d="M16 17H8"></path><path d="M10 9H8"></path></svg>'
svg_mail = '<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#4A7A4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="display:block;"><rect width="20" height="16" x="2" y="4" rx="2"></rect><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path></svg>'
svg_bank = '<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#4A7A4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="display:block;"><rect width="20" height="14" x="2" y="5" rx="2"></rect><line x1="2" x2="22" y1="10" y2="10"></line></svg>'
svg_textbook = '<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#4A7A4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="display:block;"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>'
svg_cert = '<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#4A7A4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="display:block;"><circle cx="12" cy="8" r="6"></circle><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"></path></svg>'

# index.html update
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(r'<img src="images/worry-staff\.png"[^>]*>', svg_worry, content)
content = re.sub(r'<img src="images/team-support\.png"[^>]*>', svg_team, content)
content = re.sub(r'<img src="images/step-form\.png"[^>]*>', svg_form, content)
content = re.sub(r'<img src="images/step-mail\.png"[^>]*>', svg_mail, content)
content = re.sub(r'<img src="images/step-bank\.png"[^>]*>', svg_bank, content)
content = re.sub(r'<img src="images/step-textbook\.png"[^>]*>', svg_textbook, content)
content = re.sub(r'<img src="images/step-certificate\.png"[^>]*>', svg_cert, content)

# Add class="section fade-in" to sections
content = re.sub(r'<section class="section">', '<section class="section fade-in">', content)
content = re.sub(r'<section class="section section-light">', '<section class="section section-light fade-in">', content)
# Ensure the first section (hero) or maybe other ones that don't need fade-in are handled? Actually we can just add fade-in to all sections, but hero shouldn't have it.
# Let\'s just replace all and then fix hero if needed. Hero is <section class="hero">, so it won't be matched by `<section class="section">`.

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

# services.html update
svg_personal = '<div style="text-align:center"><svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#4A7A4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:20px"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg></div>'
svg_staff = '<div style="text-align:center"><svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#4A7A4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:20px"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M22 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg></div>'
svg_company = '<div style="text-align:center"><svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#4A7A4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:20px"><rect width="16" height="20" x="4" y="2" rx="2" ry="2"></rect><path d="M9 22v-4h6v4"></path><path d="M8 6h.01"></path><path d="M16 6h.01"></path><path d="M12 6h.01"></path><path d="M12 10h.01"></path><path d="M12 14h.01"></path><path d="M16 10h.01"></path><path d="M16 14h.01"></path><path d="M8 10h.01"></path><path d="M8 14h.01"></path></svg></div>'

with open("services.html", "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(r'<img src="images/service-personal\.png"[^>]*>', svg_personal, content)
content = re.sub(r'<img src="images/service-staff\.png"[^>]*>', svg_staff, content)
content = re.sub(r'<img src="images/service-company\.png"[^>]*>', svg_company, content)

# Update Headers in services
content = content.replace('<h3>【Mission① 個人向け】 無料・転職サポート</h3>', '<h3>Mission① 個人向け｜転職サポート（求職者登録）</h3>')
content = content.replace('<h3>【Mission② 現場向け】 支援コンサル（TEACCHプログラム）</h3>', '<h3>Mission② 現場向け｜支援コンサル</h3>')
content = content.replace('<h3>【Mission③ 法人向け】 経営コンサル</h3>', '<h3>Mission③ 法人向け｜経営コンサル</h3>')

# Add fade-in
content = re.sub(r'<section class="section">', '<section class="section fade-in">', content)
content = re.sub(r'<section class="section section-light">', '<section class="section section-light fade-in">', content)

with open("services.html", "w", encoding="utf-8") as f:
    f.write(content)

print("HTML SVGs and titles updated.")

import re

with open("services.html", "r", encoding="utf-8") as f:
    content = f.read()

btn1 = '''<a href="https://docs.google.com/forms/d/e/1FAIpQLSfD_FpQgpTkn9lmagQPpd5Sr_S8SRblcDOETqLniTEZYLwepQ/viewform" target="_blank" rel="noopener" class="btn btn-cta" style="margin-right:10px; margin-bottom:10px;">無料・転職サポートに登録する</a>
                <a href="mailto:utility.co.jp.tokyo@gmail.com?subject=お問い合わせ" class="btn btn-outline" style="margin-bottom:10px;">メールで問い合わせる</a>'''
btn2 = '''<a href="https://docs.google.com/forms/d/e/1FAIpQLSdieSIXvcWFPDuTefz9pIerNgRsGVVTuarnCUIXkRqlnNh6lw/viewform" target="_blank" rel="noopener" class="btn btn-cta" style="margin-right:10px; margin-bottom:10px;">支援コンサルを申し込む</a>
                <a href="mailto:utility.co.jp.tokyo@gmail.com?subject=お問い合わせ" class="btn btn-outline" style="margin-bottom:10px;">メールで問い合わせる</a>'''
btn3 = '''<a href="https://docs.google.com/forms/d/e/1FAIpQLSdieSIXvcWFPDuTefz9pIerNgRsGVVTuarnCUIXkRqlnNh6lw/viewform" target="_blank" rel="noopener" class="btn btn-cta" style="margin-right:10px; margin-bottom:10px;">経営コンサルを申し込む</a>
                <a href="mailto:utility.co.jp.tokyo@gmail.com?subject=お問い合わせ" class="btn btn-outline" style="margin-bottom:10px;">メールで問い合わせる</a>'''

# We know they occur in order, we can replace one by one.
occurrences = [btn1, btn2, btn3]

def replacer(match):
    if occurrences:
        return occurrences.pop(0)
    return match.group(0)

content = re.sub(r'<a href="mailto:utility\.co\.jp\.tokyo@gmail\.com\?subject=お問い合わせ" class="btn btn-outline">このサービスについて問い合わせる</a>', replacer, content)

with open("services.html", "w", encoding="utf-8") as f:
    f.write(content)

print("services.html buttons updated.")

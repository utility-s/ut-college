import json
import re
from datetime import date, timedelta
from pathlib import Path
import sys

def validate():
    files = ['index.html', 'services.html', 'terms.html', 'tokushoho.html', 'privacy.html']
    bad_patterns = ['\ufffd', '老E', 'カレチE', '研修老E']
    old_kiso_patterns = [
        '2026年8月6日',
        '2026年8月7日',
        '2026年7月30日',
        '2026-08-06',
        '2026-08-07',
        '2026-07-30'
    ]
    google_form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSePDVOsYhIBRIPuHGyegQP8HumM7EN6QQeE5Xfd3BGoet1c9A/viewform'

    for fname in files:
        path = Path(fname)
        try:
            # 1. UTF-8 strictで読み込める
            text = path.read_text(encoding='utf-8', errors='strict')
        except Exception as e:
            print(f"FAILED: {fname} failed UTF-8 strict decode: {e}")
            sys.exit(1)

        # 2. NUL文字がない
        if '\x00' in text:
            print(f"FAILED: {fname} contains NUL character")
            sys.exit(1)

        # 3. 以下の文字化けパターンがない
        found_bad = [p for p in bad_patterns if p in text]
        if found_bad:
            print(f"FAILED: {fname} contains mojibake patterns: {found_bad}")
            sys.exit(1)

        # 4. 各ページに「UT福祉カレッジ」が存在する
        if 'UT福祉カレッジ' not in text:
            print(f"FAILED: {fname} missing 'UT福祉カレッジ'")
            sys.exit(1)

        # 8. 「23:59」が全対象HTMLに存在しない
        if '23:59' in text:
            print(f"FAILED: {fname} contains '23:59'")
            sys.exit(1)

        # 11. HTML内の相対リンク先がリポジトリ内に存在する
        links = re.findall(r'href="([^"]+)"', text) + re.findall(r'src="([^"]+)"', text)
        for link in links:
            if link.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:', '#')):
                continue

            # Remove fragment or query string from relative link
            clean_link = link.split('#')[0].split('?')[0]
            if not clean_link:
                continue

            # Path resolution
            target_path = Path(clean_link)
            if not target_path.exists():
                print(f"FAILED: {fname} contains broken relative link: {link}")
                sys.exit(1)

        if fname == 'tokushoho.html':
            for req in ['17,980円', '3,520円']:
                if req not in text:
                    print(f"FAILED: tokushoho.html missing required text: '{req}'")
                    sys.exit(1)

        if fname == 'index.html':
            # 5. index.htmlに「強度行動障害支援者養成研修」が存在する
            if '強度行動障害支援者養成研修' not in text:
                print("FAILED: index.html missing '強度行動障害支援者養成研修'")
                sys.exit(1)

            # 7. index.htmlのmanifest指定が正確に1件である
            manifest_count = text.count('<link rel="manifest" href="site.webmanifest"')
            if manifest_count != 1:
                print(f"FAILED: index.html has {manifest_count} manifest links")
                sys.exit(1)

            # 9. index.htmlに「対面（会場）開催のみ」が存在する
            if '対面（会場）開催のみ' not in text:
                print("FAILED: index.html missing '対面（会場）開催のみ'")
                sys.exit(1)

            # 公開表示の基礎研修新日程・情報検証
            required_strings = [
                '2026年10月19日',
                '2026年10月20日',
                '2026年10月12日',
                '追加募集受付中',
                '2027年2月4日',
                '2027年1月28日',
                '21,500円',
                '17,980円',
                '3,520円',
                google_form_url
            ]
            for req in required_strings:
                if req not in text:
                    print(f"FAILED: index.html missing required text: '{req}'")
                    sys.exit(1)

            # 画面FAQの申込締切の回答（HTML）に年月日が無いこと
            faq_match = re.search(r'<div class="faq-question">\s*申込締切はいつですか？\s*</div>\s*<div class="faq-answer">(.*?)</div>', text, re.DOTALL)
            if not faq_match:
                print("FAILED: index.html missing screen FAQ for '申込締切はいつですか？'")
                sys.exit(1)
            screen_faq_answer = faq_match.group(1)
            if re.search(r'\d{4}年\d{1,2}月\d{1,2}日', screen_faq_answer):
                print("FAILED: index.html screen FAQ answer contains specific date (YYYY年M月D日)")
                sys.exit(1)

            # 旧基礎研修情報の残存チェック
            found_old = [p for p in old_kiso_patterns if p in text]
            if found_old:
                print(f"FAILED: index.html contains old 基礎研修 info: {found_old}")
                sys.exit(1)

            # 6 & 13. index.html内のapplication/ld+jsonを抽出し、解析・検証する
            json_ld_matches = list(re.finditer(r'<script type="application/ld\+json">\s*({.*?})\s*</script>', text, re.DOTALL))
            if not json_ld_matches:
                print("FAILED: index.html missing JSON-LD")
                sys.exit(1)

            for match in json_ld_matches:
                try:
                    data = json.loads(match.group(1))
                except Exception as e:
                    print(f"FAILED: index.html JSON-LD parse error: {e}")
                    sys.exit(1)

                if "@graph" in data:
                    kiso_oct_events = []
                    kiso_feb_events = []
                    jissen_events = []
                    for item in data["@graph"]:
                        if item.get("@type") == "Event":
                            name = item.get("name", "")
                            if "基礎研修" in name:
                                if "2026年10月開催" in name or "2026-10-19" in item.get("startDate", ""):
                                    kiso_oct_events.append(item)
                                elif "2027年2月開催" in name or "2027-02-04" in item.get("startDate", ""):
                                    kiso_feb_events.append(item)
                            elif "実践研修" in name:
                                jissen_events.append(item)

                            # 全Eventについて、各Offerの validThrough が startDate の日付の7日前と一致することを確認する
                            start_str = item.get("startDate", "")
                            start_date_str = start_str[:10]
                            try:
                                start_date = date.fromisoformat(start_date_str)
                            except Exception as e:
                                print(f"FAILED: Event {name} invalid startDate format: {start_str}")
                                sys.exit(1)
                            expected_valid_through = (start_date - timedelta(days=7)).isoformat()

                            raw_offers = item.get("offers")
                            offers_list = raw_offers if isinstance(raw_offers, list) else [raw_offers] if isinstance(raw_offers, dict) else []
                            if not offers_list:
                                print(f"FAILED: Event {name} missing offers")
                                sys.exit(1)
                            for o in offers_list:
                                if o.get("validThrough") != expected_valid_through:
                                    print(f"FAILED: Event {name} offer validThrough mismatch. Expected {expected_valid_through}, got {o.get('validThrough')}")
                                    sys.exit(1)

                        if item.get("@type") == "FAQPage":
                            main_entity = item.get("mainEntity", [])
                            deadline_questions = [q for q in main_entity if q.get("name") == "申込締切はいつですか？"]
                            if len(deadline_questions) != 1:
                                print(f"FAILED: Expected exactly 1 FAQPage question '申込締切はいつですか？', found {len(deadline_questions)}")
                                sys.exit(1)
                            deadline_q = deadline_questions[0]
                            ans_text = deadline_q.get("acceptedAnswer", {}).get("text", "")
                            if "開催初日の7日前" not in ans_text:
                                print("FAILED: FAQPage deadline question answer missing '開催初日の7日前'")
                                sys.exit(1)
                            if re.search(r'\d{4}年\d{1,2}月\d{1,2}日', ans_text):
                                print("FAILED: FAQPage deadline question answer contains specific date (YYYY年M月D日)")
                                sys.exit(1)

                    # 基礎研修（2026年10月開催）Eventの検証
                    if len(kiso_oct_events) != 1:
                        print(f"FAILED: Expected exactly 1 基礎研修(10月) Event, found {len(kiso_oct_events)}")
                        sys.exit(1)
                    kiso_oct = kiso_oct_events[0]
                    if kiso_oct.get("startDate") != "2026-10-19T09:30:00+09:00":
                        print(f"FAILED: 基礎研修(10月) startDate mismatch: {kiso_oct.get('startDate')}")
                        sys.exit(1)
                    if kiso_oct.get("endDate") != "2026-10-20T17:30:00+09:00":
                        print(f"FAILED: 基礎研修(10月) endDate mismatch: {kiso_oct.get('endDate')}")
                        sys.exit(1)
                    if kiso_oct.get("eventStatus") != "https://schema.org/EventScheduled":
                        print(f"FAILED: 基礎研修(10月) eventStatus mismatch: {kiso_oct.get('eventStatus')}")
                        sys.exit(1)
                    if kiso_oct.get("eventAttendanceMode") != "https://schema.org/OfflineEventAttendanceMode":
                        print("FAILED: 基礎研修(10月) eventAttendanceMode not Offline")
                        sys.exit(1)
                    if kiso_oct.get("performer", {}).get("name") != "若林佳史":
                        print(f"FAILED: 基礎研修(10月) performer mismatch: {kiso_oct.get('performer')}")
                        sys.exit(1)

                    kiso_oct_offers = kiso_oct.get("offers", {})
                    if str(kiso_oct_offers.get("price")) != "21500":
                        print(f"FAILED: 基礎研修(10月) price mismatch: {kiso_oct_offers.get('price')}")
                        sys.exit(1)
                    if kiso_oct_offers.get("priceCurrency") != "JPY":
                        print(f"FAILED: 基礎研修(10月) priceCurrency mismatch: {kiso_oct_offers.get('priceCurrency')}")
                        sys.exit(1)
                    if kiso_oct_offers.get("availability") != "https://schema.org/InStock":
                        print(f"FAILED: 基礎研修(10月) availability mismatch: {kiso_oct_offers.get('availability')}")
                        sys.exit(1)
                    if kiso_oct_offers.get("validThrough") != "2026-10-12":
                        print(f"FAILED: 基礎研修(10月) validThrough mismatch: {kiso_oct_offers.get('validThrough')}")
                        sys.exit(1)
                    if kiso_oct_offers.get("url") != google_form_url:
                        print(f"FAILED: 基礎研修(10月) url mismatch: {kiso_oct_offers.get('url')}")
                        sys.exit(1)

                    # 基礎研修（2027年2月開催）Eventの検証
                    if len(kiso_feb_events) != 1:
                        print(f"FAILED: Expected exactly 1 基礎研修(2027年2月) Event, found {len(kiso_feb_events)}")
                        sys.exit(1)
                    kiso_feb = kiso_feb_events[0]
                    if "東京都強度行動障害支援者養成研修（基礎研修・2027年2月開催）" not in kiso_feb.get("name", ""):
                        print(f"FAILED: 基礎研修(2027年2月) name mismatch: {kiso_feb.get('name')}")
                        sys.exit(1)
                    if kiso_feb.get("startDate") != "2027-02-04T09:30:00+09:00":
                        print(f"FAILED: 基礎研修(2027年2月) startDate mismatch: {kiso_feb.get('startDate')}")
                        sys.exit(1)
                    if kiso_feb.get("endDate") != "2027-02-05T17:30:00+09:00":
                        print(f"FAILED: 基礎研修(2027年2月) endDate mismatch: {kiso_feb.get('endDate')}")
                        sys.exit(1)
                    if kiso_feb.get("eventStatus") != "https://schema.org/EventScheduled":
                        print(f"FAILED: 基礎研修(2027年2月) eventStatus mismatch: {kiso_feb.get('eventStatus')}")
                        sys.exit(1)
                    if kiso_feb.get("eventAttendanceMode") != "https://schema.org/OfflineEventAttendanceMode":
                        print("FAILED: 基礎研修(2027年2月) eventAttendanceMode not Offline")
                        sys.exit(1)
                    if kiso_feb.get("performer", {}).get("name") != "若林佳史":
                        print(f"FAILED: 基礎研修(2027年2月) performer mismatch: {kiso_feb.get('performer')}")
                        sys.exit(1)

                    kiso_feb_offers = kiso_feb.get("offers", {})
                    if str(kiso_feb_offers.get("price")) != "21500":
                        print(f"FAILED: 基礎研修(2027年2月) price mismatch: {kiso_feb_offers.get('price')}")
                        sys.exit(1)
                    if kiso_feb_offers.get("priceCurrency") != "JPY":
                        print(f"FAILED: 基礎研修(2027年2月) priceCurrency mismatch: {kiso_feb_offers.get('priceCurrency')}")
                        sys.exit(1)
                    if kiso_feb_offers.get("availability") != "https://schema.org/InStock":
                        print(f"FAILED: 基礎研修(2027年2月) availability mismatch: {kiso_feb_offers.get('availability')}")
                        sys.exit(1)
                    if kiso_feb_offers.get("validThrough") != "2027-01-28":
                        print(f"FAILED: 基礎研修(2027年2月) validThrough mismatch: {kiso_feb_offers.get('validThrough')}")
                        sys.exit(1)
                    if kiso_feb_offers.get("url") != google_form_url:
                        print(f"FAILED: 基礎研修(2027年2月) url mismatch: {kiso_feb_offers.get('url')}")
                        sys.exit(1)

                    # 実践研修Eventの検証
                    if len(jissen_events) != 1:
                        print(f"FAILED: Expected exactly 1 実践研修 Event, found {len(jissen_events)}")
                        sys.exit(1)
                    jissen = jissen_events[0]
                    if jissen.get("startDate") != "2026-11-05T09:30:00+09:00":
                        print(f"FAILED: 実践研修 startDate mismatch: {jissen.get('startDate')}")
                        sys.exit(1)
                    if jissen.get("endDate") != "2026-11-06T17:30:00+09:00":
                        print(f"FAILED: 実践研修 endDate mismatch: {jissen.get('endDate')}")
                        sys.exit(1)
                    if jissen.get("eventStatus") != "https://schema.org/EventScheduled":
                        print(f"FAILED: 実践研修 eventStatus mismatch: {jissen.get('eventStatus')}")
                        sys.exit(1)
                    if jissen.get("eventAttendanceMode") != "https://schema.org/OfflineEventAttendanceMode":
                        print("FAILED: 実践研修 eventAttendanceMode not Offline")
                        sys.exit(1)
                    if jissen.get("performer", {}).get("name") != "若林佳史":
                        print(f"FAILED: 実践研修 performer mismatch: {jissen.get('performer')}")
                        sys.exit(1)
                    if "+09:00" not in jissen.get("startDate", "") or "+09:00" not in jissen.get("endDate", ""):
                        print("FAILED: 実践研修 dates missing +09:00 timezone")
                        sys.exit(1)

                    jissen_offers_raw = jissen.get("offers")
                    if isinstance(jissen_offers_raw, list):
                        prices = {str(o.get("price")) for o in jissen_offers_raw}
                        if prices != {"21500", "17980"}:
                            print(f"FAILED: 実践研修 list offers prices mismatch: {prices}")
                            sys.exit(1)
                        for o in jissen_offers_raw:
                            if o.get("availability") != "https://schema.org/InStock":
                                print(f"FAILED: 実践研修 offer availability mismatch: {o.get('availability')}")
                                sys.exit(1)
                            if o.get("validThrough") != "2026-10-29":
                                print(f"FAILED: 実践研修 offer validThrough mismatch: {o.get('validThrough')}")
                                sys.exit(1)
                            if o.get("priceCurrency") != "JPY":
                                print(f"FAILED: 実践研修 offer priceCurrency mismatch: {o.get('priceCurrency')}")
                                sys.exit(1)
                            if o.get("url") != google_form_url:
                                print(f"FAILED: 実践研修 offer url mismatch: {o.get('url')}")
                                sys.exit(1)
                    elif isinstance(jissen_offers_raw, dict):
                        if jissen_offers_raw.get("availability") != "https://schema.org/InStock":
                            print(f"FAILED: 実践研修 availability mismatch: {jissen_offers_raw.get('availability')}")
                            sys.exit(1)
                        if jissen_offers_raw.get("validThrough") != "2026-10-29":
                            print(f"FAILED: 実践研修 validThrough mismatch: {jissen_offers_raw.get('validThrough')}")
                            sys.exit(1)
                    else:
                        print("FAILED: 実践研修 offers is neither dict nor list")
                        sys.exit(1)

        # 10. index.html、terms.html、tokushoho.htmlに返金規定が存在する
        if fname in ['index.html', 'terms.html', 'tokushoho.html']:
            if '返金' not in text:
                print(f"FAILED: {fname} missing '返金'")
                sys.exit(1)

    print("SUCCESS: All validation criteria passed successfully.")
    sys.exit(0)

if __name__ == '__main__':
    validate()

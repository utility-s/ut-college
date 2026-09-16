import json
import re
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
                '21,500円',
                google_form_url
            ]
            for req in required_strings:
                if req not in text:
                    print(f"FAILED: index.html missing required text: '{req}'")
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
                    kiso_events = []
                    jissen_events = []
                    for item in data["@graph"]:
                        if item.get("@type") == "Event":
                            if "基礎研修" in item.get("name", ""):
                                kiso_events.append(item)
                            elif "実践研修" in item.get("name", ""):
                                jissen_events.append(item)

                    # 基礎研修Eventが1件存在する
                    if len(kiso_events) != 1:
                        print(f"FAILED: Expected exactly 1 基礎研修 Event, found {len(kiso_events)}")
                        sys.exit(1)
                    kiso = kiso_events[0]

                    # 基礎研修Eventの検証
                    if "基礎研修" not in kiso.get("name", ""):
                        print("FAILED: 基礎研修 name does not contain '基礎研修'")
                        sys.exit(1)
                    if kiso.get("startDate") != "2026-10-19T09:30:00+09:00":
                        print(f"FAILED: 基礎研修 startDate mismatch: {kiso.get('startDate')}")
                        sys.exit(1)
                    if kiso.get("endDate") != "2026-10-20T17:30:00+09:00":
                        print(f"FAILED: 基礎研修 endDate mismatch: {kiso.get('endDate')}")
                        sys.exit(1)
                    if kiso.get("eventStatus") != "https://schema.org/EventScheduled":
                        print(f"FAILED: 基礎研修 eventStatus mismatch: {kiso.get('eventStatus')}")
                        sys.exit(1)
                    if kiso.get("eventAttendanceMode") != "https://schema.org/OfflineEventAttendanceMode":
                        print("FAILED: 基礎研修 eventAttendanceMode not Offline")
                        sys.exit(1)
                    if kiso.get("performer", {}).get("name") != "若林佳史":
                        print(f"FAILED: 基礎研修 performer mismatch: {kiso.get('performer')}")
                        sys.exit(1)

                    kiso_offers = kiso.get("offers", {})
                    if str(kiso_offers.get("price")) != "21500":
                        print(f"FAILED: 基礎研修 price mismatch: {kiso_offers.get('price')}")
                        sys.exit(1)
                    if kiso_offers.get("priceCurrency") != "JPY":
                        print(f"FAILED: 基礎研修 priceCurrency mismatch: {kiso_offers.get('priceCurrency')}")
                        sys.exit(1)
                    if kiso_offers.get("availability") != "https://schema.org/InStock":
                        print(f"FAILED: 基礎研修 availability mismatch: {kiso_offers.get('availability')}")
                        sys.exit(1)
                    if kiso_offers.get("validThrough") != "2026-10-12":
                        print(f"FAILED: 基礎研修 validThrough mismatch: {kiso_offers.get('validThrough')}")
                        sys.exit(1)
                    if kiso_offers.get("url") != google_form_url:
                        print(f"FAILED: 基礎研修 url mismatch: {kiso_offers.get('url')}")
                        sys.exit(1)
                    if "+09:00" not in kiso.get("startDate", "") or "+09:00" not in kiso.get("endDate", ""):
                        print("FAILED: 基礎研修 dates missing +09:00 timezone")
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

                    jissen_offers = jissen.get("offers", {})
                    if jissen_offers.get("availability") != "https://schema.org/InStock":
                        print(f"FAILED: 実践研修 availability mismatch: {jissen_offers.get('availability')}")
                        sys.exit(1)
                    if jissen_offers.get("validThrough") != "2026-10-29":
                        print(f"FAILED: 実践研修 validThrough mismatch: {jissen_offers.get('validThrough')}")
                        sys.exit(1)
                    if "+09:00" not in jissen.get("startDate", "") or "+09:00" not in jissen.get("endDate", ""):
                        print("FAILED: 実践研修 dates missing +09:00 timezone")
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

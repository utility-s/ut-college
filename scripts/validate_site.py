import json
import re
from pathlib import Path
import sys

def validate():
    files = ['index.html', 'services.html', 'terms.html', 'tokushoho.html', 'privacy.html']
    bad_patterns = ['\ufffd', '老E', 'カレチE', '研修老E']
    
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
                    for item in data["@graph"]:
                        if item.get("@type") == "Event":
                            # eventAttendanceModeがOfflineEventAttendanceMode
                            if item.get("eventAttendanceMode") != "https://schema.org/OfflineEventAttendanceMode":
                                print("FAILED: JSON-LD eventAttendanceMode not Offline")
                                sys.exit(1)
                            
                            # 講師名が若林佳史
                            if item.get("performer", {}).get("name") != "若林佳史":
                                print("FAILED: JSON-LD performer name not 若林佳史")
                                sys.exit(1)
                                
                            if "基礎研修" in item.get("name", ""):
                                # 基礎研修日時に+09:00がある
                                if "+09:00" not in item.get("startDate", "") or "+09:00" not in item.get("endDate", ""):
                                    print("FAILED: JSON-LD 基礎研修 dates missing +09:00 timezone")
                                    sys.exit(1)
                                    
                            if "実践研修" in item.get("name", ""):
                                # 実践研修がEventScheduled
                                if item.get("eventStatus") != "https://schema.org/EventScheduled":
                                    print("FAILED: JSON-LD 実践研修 status not EventScheduled")
                                    sys.exit(1)
                                # 実践研修validThroughが2026-10-29
                                if item.get("offers", {}).get("validThrough") != "2026-10-29":
                                    print("FAILED: JSON-LD 実践研修 validThrough not 2026-10-29")
                                    sys.exit(1)
                                # 実践研修日時に+09:00がある
                                if "+09:00" not in item.get("startDate", "") or "+09:00" not in item.get("endDate", ""):
                                    print("FAILED: JSON-LD 実践研修 dates missing +09:00 timezone")
                                    sys.exit(1)

        # 10. index.html、terms.html、tokushoho.htmlに返金規定が存在する
        if fname in ['index.html', 'terms.html', 'tokushoho.html']:
            if '返金' not in text:
                print(f"FAILED: {fname} missing '返金'")
                sys.exit(1)
                
    print("SUCCESS: All 13 validation criteria passed successfully.")
    sys.exit(0)

if __name__ == '__main__':
    validate()

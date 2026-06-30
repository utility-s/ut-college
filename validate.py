import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

json_str = html.split('<script type="application/ld+json">')[1].split('</script>')[0].strip()
try:
    json.loads(json_str)
    print("Valid JSON")
except Exception as e:
    print("Invalid JSON:", e)

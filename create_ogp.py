import os
from PIL import Image, ImageDraw, ImageFont

def create_ogp():
    width = 1200
    height = 630
    
    # Create white image
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw some green accents (e.g. top and bottom borders)
    draw.rectangle([0, 0, width, 20], fill=(74, 122, 74))  # #4A7A4A
    draw.rectangle([0, height-20, width, height], fill=(74, 122, 74))
    
    # Fonts
    # Using generic Windows fonts
    try:
        font_main = ImageFont.truetype("meiryo.ttc", 60)
        font_sub = ImageFont.truetype("meiryo.ttc", 40)
        font_small = ImageFont.truetype("meiryo.ttc", 32)
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Paste Logo
    logo_path = 'images/logo.png'
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        # Resize logo to fit nicely, let's say max height 100
        aspect = logo.width / logo.height
        new_h = 80
        new_w = int(new_h * aspect)
        logo = logo.resize((new_w, new_h), Image.Resampling.LANCZOS)
        # Paste at bottom right or center top
        # We'll put it in the center top
        img.paste(logo, ((width - new_w) // 2, 80), mask=logo)
    
    # Texts
    text1 = "東京都指定"
    text2 = "強度行動障害支援者養成研修"
    text3 = "基礎研修・実践研修"
    text4 = "東京・拝島駅徒歩2分"
    text5 = "UT福祉カレッジ"

    def get_text_size(text, font):
        return font.getbbox(text)[2:4] # (width, height) - ignoring x/y offsets

    y = 200
    for txt, font, color in [
        (text1, font_sub, (50, 50, 50)),
        (text2, font_main, (74, 122, 74)),
        (text3, font_main, (30, 30, 30)),
        (text4, font_sub, (50, 50, 50)),
    ]:
        w, h = get_text_size(txt, font)
        draw.text(((width - w) // 2, y), txt, font=font, fill=color)
        y += h + 30

    # Ensure images directory exists
    os.makedirs('images', exist_ok=True)
    img.save('images/ogp.png')

if __name__ == '__main__':
    create_ogp()
    print("OGP image created.")

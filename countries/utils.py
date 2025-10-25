import os

import requests
from django.conf import settings
from PIL import Image, ImageDraw ,ImageFont

RESTCOUNTRIES_URL = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
EXCHANGE_URL = "https://open.er-api.com/v6/latest/USD"
CACHE_IMAGE_PATH = os.path.join(settings.BASE_DIR, "cache", "summary.png")

def fetch_json(url, timeout=600):
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()

def generate_summary_image(total, top5, timestamp_iso):
    os.makedirs(os.path.dirname(CACHE_IMAGE_PATH), exist_ok=True)
    width, height = 1200, 800
    img = Image.new("RGB", (width, height), color=(215,0,200))
    draw = ImageDraw.Draw(img)
    title = f"Countries Summary"
    font = ImageFont.truetype("arial.ttf", size=24)
    font2 = ImageFont.truetype("arial.ttf", size=32)
    draw.text((40,40), title, fill="black", font=font2)
    draw.text((40,90), f"Total countries: {total}", fill="blue", font=font)
    draw.text((40,120), f"Last refreshed: {timestamp_iso}", fill="blue", font=font)
    draw.text((40,180), "Top 5 by estimated GDP:", fill="blue", font=font)
    y = 220
    for idx, c in enumerate(top5, start=1):
        line = f"{idx}. {c.name} — {c.estimated_gdp or 0:,.2f} {c.currency_code or ''}"
        draw.text((60,y), line, fill="blue", font=font)
        y += 36
    img.save(CACHE_IMAGE_PATH)
    print("========================executed==============")
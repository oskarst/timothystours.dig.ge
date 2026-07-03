import asyncio
import json
import os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

REGIONS = [
    {"name": "Samegrelo", "url": "https://timothystours.ge/georgia-and-its-regions/samegrelo/"},
    {"name": "Guria", "url": "https://timothystours.ge/georgia-and-its-regions/guria/"},
    {"name": "Adjara", "url": "https://timothystours.ge/georgia-and-its-regions/adjara/"},
    {"name": "Lechkhumi", "url": "https://timothystours.ge/georgia-and-its-regions/lechkhumi/"},
    {"name": "Racha", "url": "https://timothystours.ge/georgia-and-its-regions/racha/"},
    {"name": "Imereti", "url": "https://timothystours.ge/georgia-and-its-regions/imereti/"},
    {"name": "Meskheti", "url": "https://timothystours.ge/georgia-and-its-regions/meskheti/"},
    {"name": "Javakheti", "url": "https://timothystours.ge/georgia-and-its-regions/javakheti/"},
    {"name": "Kartli", "url": "https://timothystours.ge/georgia-and-its-regions/kartli/"},
    {"name": "Svaneti", "url": "https://timothystours.ge/georgia-and-its-regions/svaneti/"},
    {"name": "Mtianeti", "url": "https://timothystours.ge/georgia-and-its-regions/mtianeti/"},
    {"name": "Kakheti", "url": "https://timothystours.ge/georgia-and-its-regions/kakheti/"},
    {"name": "Tbilisi", "url": "https://timothystours.ge/georgia-and-its-regions/tbilisi/"}
]

async def scrape_text(page, region):
    print(f"Scraping text for {region['name']}...")
    try:
        await page.goto(region['url'], wait_until="domcontentloaded", timeout=60000)
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')
        
        # Elementor entry-content
        content_div = soup.find(class_='entry-content')
        if not content_div:
            return ""
            
        # Get all text, but filter out image captions or random empty space
        # Better: get all <p> and <h> tags
        elements = content_div.find_all(['p', 'h2', 'h3'])
        text_blocks = [el.get_text(strip=True) for el in elements if el.get_text(strip=True)]
        
        # Remove common footer/unwanted text like "Jump to pictures" or "Send me a message"
        filtered = []
        for t in text_blocks:
            if "Jump to pictures" in t: continue
            if "Send me a message" in t: continue
            filtered.append(t)
            
        return "\n\n".join(filtered)
    except Exception as e:
        print(f"Error scraping {region['name']}: {e}")
        return ""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        results = {}
        for region in REGIONS:
            text = await scrape_text(page, region)
            results[region['name']] = text
            
        with open('region_texts_original.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

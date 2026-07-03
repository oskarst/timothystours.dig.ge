import asyncio
import json
import os
import re
from urllib.parse import urlparse
import urllib.request
from playwright.async_api import async_playwright
from PIL import Image
import io

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

PUB_DIR = os.path.join(os.path.dirname(__file__), "pub")
IMG_DIR = os.path.join(PUB_DIR, "img", "regions")
REGIONS_DIR = os.path.join(PUB_DIR, "regions")

async def download_image(url, region_name):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            image_data = response.read()
            img = Image.open(io.BytesIO(image_data))
            
            basename = os.path.basename(urlparse(url).path)
            if not basename:
                basename = "image.jpg"
            name_only = os.path.splitext(basename)[0]
            clean_name = re.sub(r'[^a-zA-Z0-9-]', '_', name_only).lower()
            
            filename = f"{region_name.lower()}-gallery-{clean_name}.webp"
            filepath = os.path.join(IMG_DIR, filename)
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(filepath, 'webp', quality=75)
            
            return f"../img/regions/{filename}"
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return ""

async def scrape_region(page, region):
    print(f"Scraping gallery for {region['name']}...")
    try:
        await page.goto(region['url'], wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(2000)
        
        images = await page.evaluate('''() => {
            let imgs = Array.from(document.querySelectorAll('.entry-content img, article img'));
            return imgs.map(i => {
                // If it has a data-src (lazy loaded), use that. Otherwise use src.
                let url = i.getAttribute('data-src') || i.src;
                return url;
            }).filter(src => src && !src.startsWith('data:image'));
        }''')
        return images
    except Exception as e:
        print(f"Error scraping {region['name']}: {e}")
        return []

def inject_carousel_into_html(region_name, images_paths):
    filepath = os.path.join(REGIONS_DIR, f"{region_name.lower()}.html")
    if not os.path.exists(filepath):
        print(f"Cannot inject into {filepath}, file not found.")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # If carousel already exists or no images, skip
    if 'carousel-container' in content or not images_paths:
        return

    # Build Carousel HTML
    images_html = ""
    for path in images_paths:
        images_html += f'                <img src="{path}" alt="{region_name} Gallery Image" class="w-80 h-64 object-cover shrink-0 snap-center border-2 border-primary" loading="lazy" />\n'

    carousel_html = f'''
        <!-- Carousel Section -->
        <div class="w-full bg-bgPrimary py-8 border-b-2 border-gray-800 relative z-20">
            <div class="max-w-6xl mx-auto px-4 relative group">
                <button class="carousel-prev absolute left-0 top-1/2 transform -translate-y-1/2 z-30 bg-gray-900 border-2 border-primary text-accent w-12 h-12 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 hover:bg-primary hover:text-white cursor-pointer hidden md:flex">&#10094;</button>
                
                <div class="carousel-container flex gap-4 overflow-x-auto snap-x snap-mandatory scroll-smooth scrollbar-hide py-4 px-2">
{images_html}
                </div>
                
                <button class="carousel-next absolute right-0 top-1/2 transform -translate-y-1/2 z-30 bg-gray-900 border-2 border-primary text-accent w-12 h-12 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 hover:bg-primary hover:text-white cursor-pointer hidden md:flex">&#10095;</button>
            </div>
        </div>
'''

    # Inject immediately before the main content section
    # Which we recently gave 'brush-edge-top bg-bgPrimary'
    target_section_start = '<section class="py-20 px-8 max-w-4xl mx-auto bg-bgPrimary brush-edge-top'
    if target_section_start in content:
        content = content.replace(target_section_start, f'{carousel_html}\n        {target_section_start}')
        
        # Also ensure the JS is loaded
        if 'carousel.js' not in content:
            content = content.replace('</body>', '    <script src="../js/carousel.js"></script>\n</body>')
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Injected carousel into {region_name.lower()}.html")
    else:
        print(f"Could not find insertion point in {filepath}")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        for region in REGIONS:
            image_urls = await scrape_region(page, region)
            
            # Skip the first image because it's already used as the hero banner
            if len(image_urls) > 1:
                gallery_urls = image_urls[1:]
                local_paths = []
                for url in gallery_urls:
                    path = await download_image(url, region['name'])
                    if path:
                        local_paths.append(path)
                
                inject_carousel_into_html(region['name'], local_paths)
            else:
                print(f"Not enough images for {region['name']} to build a carousel.")
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

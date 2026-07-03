import asyncio
import json
import os
import re
from urllib.parse import urljoin
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
REGIONS_DIR = os.path.join(PUB_DIR, "regions")
IMG_DIR = os.path.join(PUB_DIR, "img", "regions")

os.makedirs(REGIONS_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} | Timothy's Tours</title>
    <meta name="description" content="Explore {name}, a beautiful region in Georgia.">
    <link rel="stylesheet" href="../uno.css">
</head>
<body class="bg-bgPrimary text-textLight font-sans m-0 p-0 leading-relaxed pt-16 flex flex-col min-h-screen overflow-x-hidden">

    <!-- Top Navigation -->
    <nav class="flex justify-between items-center px-6 py-4 bg-bgPrimary border-b-2 border-primary fixed w-full top-0 z-50 shadow-md">
        <div class="text-xl font-serif text-accent uppercase tracking-widest font-bold"><a href="../index.html" class="no-underline text-accent hover:text-yellow-500">Timothy's Tours</a></div>
        <div class="flex gap-6 hidden md:flex">
            <a href="../index.html" class="no-underline text-textLight hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300">Home</a>
            <a href="../about.html" class="no-underline text-textLight hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300">About Me</a>
            <a href="../trip-planning.html" class="no-underline text-textLight hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300">Trip Planning</a>
            <a href="index.html" class="no-underline text-accent hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300">Regions</a>
            <a href="../contact.html" class="no-underline text-textLight hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300">Contact</a>
        </div>
    </nav>
    <main class="flex-grow">
        <!-- Hero Section -->
        <header class="relative flex flex-col justify-center items-center text-center p-8 border-b-4 border-primary brush-edge-bottom" style="height: 60vh; width: 100%; overflow: hidden;">
            <div class="absolute top-0 left-0 w-full h-full z-0">
                <img src="../{hero_img}" alt="{name} Landscape" class="w-full h-full object-cover" />
            </div>
            <div class="absolute top-0 left-0 w-full h-full z-10 bg-gray-900 bg-opacity-60"></div>
            
            <div class="relative z-20 w-full max-w-4xl mx-auto">
                <h1 class="font-serif text-4xl md:text-5xl text-accent uppercase tracking-widest mb-6">{name}</h1>
            </div>
        </header>

        <!-- Content Section -->
        <section class="py-20 px-8 max-w-4xl mx-auto relative z-10 text-lg text-gray-300">
            {content_html}
        </section>
        
        <!-- CTA -->
        <div class="text-center pb-20">
             <a href="../contact.html" class="inline-block bg-primary text-textLight px-6 py-3 font-bold uppercase tracking-widest border-2 border-primary hover:bg-transparent hover:text-primary transition-all duration-300">Explore {name} With Me</a>
        </div>
    </main>
    
    <footer class="bg-gray-900 text-center py-6 border-t border-gray-700 mt-auto">
        <p class="text-gray-400 text-sm m-0">&copy; 2026 Timothy Calvin Merkel</p>
    </footer>
</body>
</html>
"""

async def download_image(url, region_name):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            image_data = response.read()
            img = Image.open(io.BytesIO(image_data))
            
            # Create a safe filename
            basename = os.path.basename(urllib.parse.urlparse(url).path)
            if not basename:
                basename = "image.jpg"
            name_only = os.path.splitext(basename)[0]
            clean_name = re.sub(r'[^a-zA-Z0-9-]', '_', name_only).lower()
            
            filename = f"{region_name.lower()}-{clean_name}.webp"
            filepath = os.path.join(IMG_DIR, filename)
            
            # Convert to RGB if necessary and save as WebP
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(filepath, 'webp', quality=80)
            
            return f"img/regions/{filename}"
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return ""

async def scrape_region(page, region):
    print(f"Scraping {region['name']} at {region['url']}...")
    try:
        await page.goto(region['url'], timeout=60000, wait_until="domcontentloaded")
        # Give it a second to bypass cloudflare just in case
        await page.wait_for_timeout(3000)
        
        # Extract main content and images. We assume the content is in the main article body.
        # Since we don't know the exact DOM structure, let's grab paragraphs and images.
        data = await page.evaluate('''() => {
            let paragraphs = Array.from(document.querySelectorAll('.entry-content p, .entry-content h2, .entry-content h3'));
            if (paragraphs.length === 0) {
                paragraphs = Array.from(document.querySelectorAll('p, h2, h3'));
            }
            let imgs = Array.from(document.querySelectorAll('.entry-content img, article img'));
            
            let content = paragraphs.map(p => {
                return { tag: p.tagName.toLowerCase(), text: p.innerText };
            });
            let images = imgs.map(i => i.src).filter(src => src);
            return { content, images };
        }''')
        
        return data
    except Exception as e:
        print(f"Error scraping {region['name']}: {e}")
        return None

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        grid_html = ""
        
        for region in REGIONS:
            data = await scrape_region(page, region)
            if not data:
                continue
            
            content_blocks = data.get('content', [])
            image_urls = data.get('images', [])
            
            content_html = ""
            for block in content_blocks:
                tag = block['tag']
                text = block['text'].strip()
                if not text: continue
                if tag == 'p':
                    content_html += f"<p class='mb-6'>{text}</p>\\n"
                elif tag == 'h2':
                    content_html += f"<h2 class='text-2xl text-accent font-serif mb-4 mt-8'>{text}</h2>\\n"
                elif tag == 'h3':
                    content_html += f"<h3 class='text-xl text-primary font-serif mb-3 mt-6'>{text}</h3>\\n"
            
            # Download images
            hero_img = ""
            if image_urls:
                # Use first image as hero
                hero_img = await download_image(image_urls[0], region['name'])
            
            if not hero_img:
                # Fallback to trip planning background
                hero_img = "img/trip_planning/svaneti-alpine-trek-1024x768.webp"
                
            # Write HTML file
            html_content = HTML_TEMPLATE.format(
                name=region['name'],
                hero_img=hero_img,
                content_html=content_html
            )
            
            file_path = os.path.join(REGIONS_DIR, f"{region['name'].lower()}.html")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            print(f"Created {file_path}")
            
            # Add to grid
            grid_html += f'''
                <a href="{region['name'].lower()}.html" class="block group relative overflow-hidden h-80 border-2 border-gray-800 transition-all duration-300 hover:border-accent">
                    <img src="../{hero_img}" alt="{region['name']} Landscape" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
                    <div class="absolute inset-0 bg-gray-900 bg-opacity-50 group-hover:bg-opacity-30 transition-all duration-300"></div>
                    <div class="absolute inset-0 flex items-center justify-center">
                        <h3 class="font-serif text-3xl text-white uppercase tracking-widest drop-shadow-md group-hover:text-accent transition-colors duration-300">{region['name']}</h3>
                    </div>
                </a>
            '''
            
        # Update regions/index.html with the grid
        index_path = os.path.join(REGIONS_DIR, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            index_content = f.read()
            
        index_content = index_content.replace("<!-- Region cards will be generated by the script -->", grid_html)
        
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)
            
        print("Updated regions/index.html with grid.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

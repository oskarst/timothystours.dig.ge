import glob
import os
import re

files = glob.glob(r"C:\Users\shawn\.gemini\antigravity\scratch\DevAll\timothystours.dig.ge-working\pub\regions\*.html")

pattern = re.compile(r'<!-- Carousel Section -->.*?</div>\s*</div>', re.DOTALL)

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<!-- Carousel Section -->' in content:
        # Remove the carousel
        content = pattern.sub('', content)
        
        # We also need to fix the <section> brush-edge-top because we removed it earlier
        content = content.replace(
            '<section class="py-20 px-8 max-w-4xl mx-auto bg-bgPrimary relative z-20 text-lg text-gray-300">',
            '<section class="py-20 px-8 max-w-4xl mx-auto bg-bgPrimary brush-edge-top relative z-20 text-lg text-gray-300">'
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Stripped old carousel from {os.path.basename(filepath)}")

import os
import re
import glob

pub_dir = r"C:\Users\shawn\.gemini\antigravity\scratch\DevAll\timothystours.dig.ge-working\pub\regions"
html_files = glob.glob(os.path.join(pub_dir, "*.html"))

for filepath in html_files:
    if filepath.endswith('index.html'):
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove the red edge div
    content = content.replace('            <div class="absolute bottom-0 left-0 w-full h-3 bg-primary brush-edge-bottom z-30"></div>\n', '')
    content = content.replace('<div class="absolute bottom-0 left-0 w-full h-3 bg-primary brush-edge-bottom z-30"></div>', '')

    # 2. Change the main section to have brush-edge-top and bg-bgPrimary
    old_section = '<section class="py-20 px-8 max-w-4xl mx-auto relative z-10 text-lg text-gray-300">'
    new_section = '<section class="py-20 px-8 max-w-4xl mx-auto bg-bgPrimary brush-edge-top relative z-20 text-lg text-gray-300">'
    
    if old_section in content:
        content = content.replace(old_section, new_section)
    elif new_section not in content:
        # Just in case it was slightly modified
        print(f"Warning: Could not find exact section tag in {filepath}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print(f"Applied dark jagged edge bleeding over hero in {os.path.basename(filepath)}")

print("Done.")

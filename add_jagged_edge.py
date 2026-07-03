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

    # 1. Remove overflow: hidden from header
    content = content.replace('style="height: 60vh; width: 100%; overflow: hidden;"', 'style="height: 60vh; width: 100%;"')
    
    # 2. Remove border-b-4 border-primary brush-edge-bottom from header
    content = content.replace('border-b-4 border-primary brush-edge-bottom', '')

    # 3. Add the red jagged edge bar at the bottom of the header
    red_edge_div = '\n            <div class="absolute bottom-0 left-0 w-full h-3 bg-primary brush-edge-bottom z-30"></div>'
    
    # We want to insert this div right before the closing </header>
    if '<div class="absolute bottom-0 left-0 w-full h-3 bg-primary brush-edge-bottom z-30"></div>' not in content:
        content = content.replace('</header>', f'{red_edge_div}\n        </header>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        print(f"Added jagged red border to {os.path.basename(filepath)}")

print("Done.")

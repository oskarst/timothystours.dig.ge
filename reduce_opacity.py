import os
import re
import glob

pub_dir = r"C:\Users\shawn\.gemini\antigravity\scratch\DevAll\timothystours.dig.ge-working\pub"

# Find all HTML files in pub and pub/regions
html_files = glob.glob(os.path.join(pub_dir, "*.html")) + glob.glob(os.path.join(pub_dir, "regions", "*.html"))

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Reduce dark overlay opacity from 50% to 40%
    new_content = content.replace('bg-gray-900 opacity-50', 'bg-gray-900 opacity-40')
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            print(f"Updated opacity to 40% in {os.path.basename(filepath)}")

print("All dark overlays reduced to 40%.")

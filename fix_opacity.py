import os
import re
import glob

pub_dir = r"C:\Users\shawn\.gemini\antigravity\scratch\DevAll\timothystours.dig.ge-working\pub"

# Find all HTML files in pub and pub/regions
html_files = glob.glob(os.path.join(pub_dir, "*.html")) + glob.glob(os.path.join(pub_dir, "regions", "*.html"))

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace bg-opacity-XX with opacity-XX
    # UnoCSS sometimes doesn't parse bg-opacity well depending on the preset, 
    # but opacity-XX applies standard opacity which works universally.
    new_content = re.sub(r'bg-opacity-([0-9]+)', r'opacity-\1', content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            print(f"Fixed opacity in {filepath}")

print("Opacity fix applied globally.")

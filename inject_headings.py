import json
import os
import glob
import re

def main():
    with open('region_headings.json', 'r', encoding='utf-8') as f:
        headings = json.load(f)
        
    files = glob.glob(r"pub\regions\*.html")
    
    for filepath in files:
        basename = os.path.basename(filepath)
        region_name = basename.replace('.html', '').capitalize()
        
        if region_name not in headings:
            continue
            
        h1, h2 = headings[region_name]
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # The structure is:
        # <section class="pt-20 px-8 max-w-4xl mx-auto bg-bgPrimary brush-edge-top relative z-20 text-lg text-gray-300">
        #     <p class="mb-6">Paragraph 1...</p>
        
        # We want to inject the first heading right after the opening section tag.
        section1_pattern = r'(<section class="pt-20 px-8 max-w-4xl mx-auto bg-bgPrimary brush-edge-top relative z-20 text-lg text-gray-300">)'
        heading1_html = f'\\1\n            <h2 class="text-3xl text-accent font-serif mb-6 uppercase tracking-wider">{h1}</h2>'
        
        if not re.search(r'<h2 class="text-3xl text-accent font-serif', content):
            content = re.sub(section1_pattern, heading1_html, content)
            
        # We want to inject the second heading right after the lower section tag
        section2_pattern = r'(<section class="pb-20 pt-8 px-8 max-w-4xl mx-auto bg-bgPrimary relative z-20 text-lg text-gray-300">)'
        heading2_html = f'\\1\n            <h2 class="text-3xl text-accent font-serif mb-6 uppercase tracking-wider">{h2}</h2>'
        
        # Only inject if we haven't already (by checking for 2 h2s, but here we just replace the exact pattern if we know it's clean)
        # We'll just sub it because the pattern will only match the start of the section
        if len(re.findall(r'<h2 class="text-3xl text-accent font-serif', content)) < 2:
            content = re.sub(section2_pattern, heading2_html, content)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Injected headings for {region_name}")

if __name__ == "__main__":
    main()

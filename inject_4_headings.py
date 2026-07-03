import json
import os
import glob
import re

def main():
    with open('region_headings_4.json', 'r', encoding='utf-8') as f:
        headings = json.load(f)
        
    files = glob.glob(r"pub\regions\*.html")
    
    for filepath in files:
        basename = os.path.basename(filepath)
        region_name = basename.replace('.html', '').capitalize()
        
        if region_name not in headings:
            continue
            
        h1, h2, h3, h4 = headings[region_name]
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # First, let's strip out ANY existing h2 tags with the specific class
        content = re.sub(r'\s*<h2 class="text-3xl text-accent font-serif mb-6 uppercase tracking-wider">.*?</h2>', '', content)
        
        # Now find all 4 paragraphs. We know they are inside sections.
        # Let's extract the two sections entirely and rebuild them.
        
        # Find upper section
        upper_match = re.search(r'<section class="pt-20 px-8 max-w-4xl mx-auto bg-bgPrimary brush-edge-top relative z-20 text-lg text-gray-300">(.*?)</section>', content, re.DOTALL)
        if not upper_match:
            print(f"Skipping {region_name}: could not find upper section")
            continue
            
        # Find lower section
        lower_match = re.search(r'<section class="pb-20 pt-8 px-8 max-w-4xl mx-auto bg-bgPrimary relative z-20 text-lg text-gray-300">(.*?)</section>', content, re.DOTALL)
        if not lower_match:
            print(f"Skipping {region_name}: could not find lower section")
            continue
            
        upper_inner = upper_match.group(1)
        lower_inner = lower_match.group(1)
        
        # Extract the <p> tags
        p_upper = re.findall(r'<p class="mb-6">.*?</p>', upper_inner, re.DOTALL)
        p_lower = re.findall(r'<p class="mb-6">.*?</p>', lower_inner, re.DOTALL)
        
        if len(p_upper) != 2 or len(p_lower) != 2:
            print(f"Skipping {region_name}: Unexpected paragraph count {len(p_upper)} and {len(p_lower)}")
            continue
            
        # Rebuild upper inner HTML
        new_upper_inner = f"""
            <h2 class="text-3xl text-accent font-serif mb-6 uppercase tracking-wider">{h1}</h2>
            {p_upper[0]}
            <h2 class="text-3xl text-accent font-serif mb-6 uppercase tracking-wider mt-8">{h2}</h2>
            {p_upper[1]}
        """
        
        # Rebuild lower inner HTML
        new_lower_inner = f"""
            <h2 class="text-3xl text-accent font-serif mb-6 uppercase tracking-wider">{h3}</h2>
            {p_lower[0]}
            <h2 class="text-3xl text-accent font-serif mb-6 uppercase tracking-wider mt-8">{h4}</h2>
            {p_lower[1]}
        """
        
        # Replace back into content
        content = content.replace(upper_match.group(1), new_upper_inner)
        content = content.replace(lower_match.group(1), new_lower_inner)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Injected 4 headings for {region_name}")

if __name__ == "__main__":
    main()

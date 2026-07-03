import json
import os
import glob
import re

def main():
    # Load the finalized texts
    with open('region_texts_final.json', 'r', encoding='utf-8') as f:
        texts = json.load(f)
        
    # Get all region files
    files = glob.glob(r"pub\regions\*.html")
    
    for filepath in files:
        basename = os.path.basename(filepath)
        region_name = basename.replace('.html', '').capitalize()
        
        if region_name not in texts:
            print(f"Skipping {region_name}, no text found.")
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        paragraphs = texts[region_name].strip().split('\n\n')
        if len(paragraphs) != 4:
            print(f"Warning: {region_name} has {len(paragraphs)} paragraphs instead of 4.")
            
        p1, p2, p3, p4 = paragraphs[:4]
        
        # Extract the existing carousel block
        # The carousel starts with <!-- Carousel Section --> and ends with </div>\s*</div> or similar.
        carousel_match = re.search(r'(<!-- Carousel Section -->.*?</div>\s*</div>)', content, re.DOTALL)
        if not carousel_match:
            print(f"Warning: No carousel found in {region_name}. Skipping.")
            continue
            
        carousel_html = carousel_match.group(1)
        
        # We need to remove the jagged edge from the carousel, since it is now moving into the middle of the text
        carousel_html = carousel_html.replace('brush-edge-top', '')
        carousel_html = carousel_html.replace('py-16', 'py-8') # reduce vertical padding since it's inline now
        
        # Construct the new content block
        upper_section = f"""<section class="pt-20 px-8 max-w-4xl mx-auto bg-bgPrimary brush-edge-top relative z-20 text-lg text-gray-300">
            <p class="mb-6">{p1}</p>
            <p class="mb-6">{p2}</p>
        </section>"""
        
        lower_section = f"""<section class="pb-20 pt-8 px-8 max-w-4xl mx-auto bg-bgPrimary relative z-20 text-lg text-gray-300">
            <p class="mb-6">{p3}</p>
            <p class="mb-6">{p4}</p>
        </section>"""
        
        new_content_block = f"""{upper_section}\n\n        {carousel_html}\n\n        {lower_section}"""
        
        # Remove the old carousel block
        content = content.replace(carousel_match.group(1), '')
        
        # Find the old section block and replace it
        section_match = re.search(r'<section class=".*?bg-bgPrimary.*?relative z-20 text-lg text-gray-300">.*?</section>', content, re.DOTALL)
        if section_match:
            content = content.replace(section_match.group(0), new_content_block)
        else:
            print(f"Could not find section block in {region_name}")
            continue
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Successfully injected content for {region_name}")

if __name__ == "__main__":
    main()

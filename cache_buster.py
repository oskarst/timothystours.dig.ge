import os
import glob
import re

def bump_version(content):
    # Regex for uno.css
    # If no ?v=, add ?v=1
    content = re.sub(r'href="uno\.css"', 'href="uno.css?v=1"', content)
    content = re.sub(r'href="\.\./uno\.css"', 'href="../uno.css?v=1"', content)
    
    # If it has ?v=\d+, increment it (for future proofing)
    def increment(match):
        prefix = match.group(1)
        val = int(match.group(2)) + 1
        suffix = match.group(3)
        return f'{prefix}{val}{suffix}'
        
    content = re.sub(r'(href="uno\.css\?v=)(\d+)(")', increment, content)
    content = re.sub(r'(href="\.\./uno\.css\?v=)(\d+)(")', increment, content)
    
    # Same for JS files
    # nav.js
    content = re.sub(r'src="js/nav\.js"', 'src="js/nav.js?v=1"', content)
    content = re.sub(r'src="\.\./js/nav\.js"', 'src="../js/nav.js?v=1"', content)
    
    # carousel.js
    content = re.sub(r'src="js/carousel\.js"', 'src="js/carousel.js?v=1"', content)
    content = re.sub(r'src="\.\./js/carousel\.js"', 'src="../js/carousel.js?v=1"', content)
    
    return content

def main():
    files = glob.glob(r"pub\*.html") + glob.glob(r"pub\regions\*.html")
    for filepath in files:
        if "timothystours_old.html" in filepath:
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = bump_version(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
    print("Cache busters bumped.")

if __name__ == "__main__":
    main()

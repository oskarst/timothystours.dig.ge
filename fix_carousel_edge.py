import glob
import os

files = glob.glob(r"C:\Users\shawn\.gemini\antigravity\scratch\DevAll\timothystours.dig.ge-working\pub\regions\*.html")

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<!-- Carousel Section -->' in content:
        # Avoid double replacing
        if 'brush-edge-top' not in content.split('<!-- Carousel Section -->')[1].split('<div')[1].split('>')[0]:
            content = content.replace(
                '<div class="w-full bg-bgPrimary py-8 border-b-2 border-gray-800 relative z-20">',
                '<div class="w-full bg-bgPrimary py-16 border-b-2 border-gray-800 relative z-20 brush-edge-top">'
            )
            content = content.replace(
                '<section class="py-20 px-8 max-w-4xl mx-auto bg-bgPrimary brush-edge-top relative z-20 text-lg text-gray-300">',
                '<section class="py-20 px-8 max-w-4xl mx-auto bg-bgPrimary relative z-20 text-lg text-gray-300">'
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed jagged edge in {os.path.basename(filepath)}")

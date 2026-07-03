import os
import re

pub_dir = r"C:\Users\shawn\.gemini\antigravity\scratch\DevAll\timothystours.dig.ge-working\pub"

regions = [
    "samegrelo", "guria", "adjara", "lechkhumi", "racha", "imereti", "meskheti",
    "javakheti", "kartli", "svaneti", "mtianeti", "kakheti", "tbilisi"
]

def generate_nav(is_in_regions_dir=False):
    prefix = "../" if is_in_regions_dir else ""
    regions_prefix = "" if is_in_regions_dir else "regions/"
    
    # We use UnoCSS group-hover to create a pure CSS dropdown menu
    dropdown_html = f'''<li class="relative group">
                <a href="{regions_prefix}index.html" class="no-underline text-textLight hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300 py-2">Regions &#9662;</a>
                <ul class="absolute left-0 mt-2 hidden group-hover:block bg-bgPrimary border-2 border-primary w-48 shadow-lg list-none p-0 m-0 z-50">'''
                
    for r in regions:
        dropdown_html += f'\n                    <li><a href="{regions_prefix}{r}.html" class="block px-4 py-3 text-textLight hover:text-accent hover:bg-gray-800 transition-colors capitalize">{r}</a></li>'
    
    dropdown_html += '\n                </ul>\n            </li>'

    nav = f'''<ul class="flex gap-8 hidden md:flex list-none m-0 p-0 items-center">
            <li><a href="{prefix}index.html" class="no-underline text-textLight hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300">Home</a></li>
            <li><a href="{prefix}about.html" class="no-underline text-textLight hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300">About Me</a></li>
            <li><a href="{prefix}trip-planning.html" class="no-underline text-textLight hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300">Trip Planning</a></li>
            {dropdown_html}
            <li><a href="{prefix}contact.html" class="no-underline text-textLight hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300">Contact</a></li>
        </ul>'''
    return nav

def update_file(filepath, is_in_regions_dir):
    if not os.path.exists(filepath):
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find the current nav list and replace it
    # It could be <div class="flex gap-6 hidden md:flex">...</div>
    # Or it could be <ul class="flex gap-6 hidden md:flex list-none m-0 p-0">...</ul>
    
    # Try UL first
    pattern_ul = re.compile(r'<ul class="flex gap-6 hidden md:flex list-none m-0 p-0">.*?</ul>', re.DOTALL)
    new_nav = generate_nav(is_in_regions_dir)
    
    if pattern_ul.search(content):
        content = pattern_ul.sub(new_nav, content)
    else:
        # Try DIV
        pattern_div = re.compile(r'<div class="flex gap-6 hidden md:flex">.*?</div>', re.DOTALL)
        if pattern_div.search(content):
            content = pattern_div.sub(new_nav, content)

    # Highlight active link (simple text replacement based on filename)
    filename = os.path.basename(filepath)
    if filename == "index.html" and not is_in_regions_dir:
        content = content.replace('href="" class="no-underline text-textLight', 'href="" class="no-underline text-accent')
        content = content.replace('href="index.html" class="no-underline text-textLight', 'href="index.html" class="no-underline text-accent')
    elif filename == "about.html":
        content = content.replace('href="about.html" class="no-underline text-textLight', 'href="about.html" class="no-underline text-accent')
    elif filename == "trip-planning.html":
        content = content.replace('href="trip-planning.html" class="no-underline text-textLight', 'href="trip-planning.html" class="no-underline text-accent')
    elif filename == "contact.html":
        content = content.replace('href="contact.html" class="no-underline text-textLight', 'href="contact.html" class="no-underline text-accent')
    elif is_in_regions_dir:
        content = content.replace('Regions &#9662;</a>', 'Regions &#9662;</a>').replace('text-textLight hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300 py-2">Regions', 'text-accent hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300 py-2">Regions')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Update root files
for f in ["index.html", "about.html", "contact.html", "trip-planning.html"]:
    update_file(os.path.join(pub_dir, f), False)

# Update region files
for r in regions + ["index"]:
    update_file(os.path.join(pub_dir, "regions", f"{r}.html"), True)

print("Nav updated globally.")

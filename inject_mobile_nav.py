import os
import glob
import re

def get_nav_html(is_region):
    # Prefix for links targeting the root directory (pub)
    root_prefix = "../" if is_region else ""
    # Prefix for links targeting the regions directory (pub/regions)
    region_prefix = "" if is_region else "regions/"
    
    return f"""<nav class="flex flex-wrap justify-between items-center px-6 py-4 bg-bgPrimary border-b-2 border-primary fixed w-full top-0 z-50 shadow-md">
        <div class="text-xl font-serif text-accent uppercase tracking-widest font-bold z-50">
            <a href="{root_prefix}index.html" class="no-underline text-accent hover:text-yellow-500">Timothy's Tours</a>
        </div>
        
        <!-- Pancake Menu Button -->
        <button id="mobile-menu-btn" class="md:hidden text-accent focus:outline-none z-50">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
        </button>

        <!-- Nav Links -->
        <ul id="nav-links" class="hidden md:flex flex-col md:flex-row absolute md:relative top-full left-0 w-full md:w-auto bg-bgPrimary md:bg-transparent border-b-2 md:border-none border-primary gap-8 list-none m-0 p-6 md:p-0 items-center z-40 transition-all duration-300">
            <li class="w-full md:w-auto text-center md:text-left"><a href="{root_prefix}index.html" class="block no-underline text-textLight hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300">Home</a></li>
            <li class="w-full md:w-auto text-center md:text-left"><a href="{root_prefix}about.html" class="block no-underline text-textLight hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300">About Me</a></li>
            <li class="w-full md:w-auto text-center md:text-left"><a href="{root_prefix}trip-planning.html" class="block no-underline text-textLight hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300">Trip Planning</a></li>
            <li class="relative group w-full md:w-auto text-center md:text-left">
                <a href="{region_prefix}index.html" id="mobile-regions-btn" class="block no-underline text-textLight hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300 md:py-2">Regions &#9662;</a>
                <ul id="mobile-regions-dropdown" class="hidden md:group-hover:block relative md:absolute left-0 mt-2 bg-bgPrimary md:border-2 md:border-primary w-full md:w-48 shadow-none md:shadow-lg list-none p-0 m-0 z-50">
                    <li><a href="{region_prefix}samegrelo.html" class="block px-4 py-3 text-textLight hover:text-accent hover:bg-gray-800 transition-colors capitalize">samegrelo</a></li>
                    <li><a href="{region_prefix}guria.html" class="block px-4 py-3 text-textLight hover:text-accent hover:bg-gray-800 transition-colors capitalize">guria</a></li>
                    <li><a href="{region_prefix}adjara.html" class="block px-4 py-3 text-textLight hover:text-accent hover:bg-gray-800 transition-colors capitalize">adjara</a></li>
                    <li><a href="{region_prefix}lechkhumi.html" class="block px-4 py-3 text-textLight hover:text-accent hover:bg-gray-800 transition-colors capitalize">lechkhumi</a></li>
                    <li><a href="{region_prefix}racha.html" class="block px-4 py-3 text-textLight hover:text-accent hover:bg-gray-800 transition-colors capitalize">racha</a></li>
                    <li><a href="{region_prefix}imereti.html" class="block px-4 py-3 text-textLight hover:text-accent hover:bg-gray-800 transition-colors capitalize">imereti</a></li>
                    <li><a href="{region_prefix}meskheti.html" class="block px-4 py-3 text-textLight hover:text-accent hover:bg-gray-800 transition-colors capitalize">meskheti</a></li>
                    <li><a href="{region_prefix}javakheti.html" class="block px-4 py-3 text-textLight hover:text-accent hover:bg-gray-800 transition-colors capitalize">javakheti</a></li>
                    <li><a href="{region_prefix}kartli.html" class="block px-4 py-3 text-textLight hover:text-accent hover:bg-gray-800 transition-colors capitalize">kartli</a></li>
                    <li><a href="{region_prefix}svaneti.html" class="block px-4 py-3 text-textLight hover:text-accent hover:bg-gray-800 transition-colors capitalize">svaneti</a></li>
                    <li><a href="{region_prefix}mtianeti.html" class="block px-4 py-3 text-textLight hover:text-accent hover:bg-gray-800 transition-colors capitalize">mtianeti</a></li>
                    <li><a href="{region_prefix}kakheti.html" class="block px-4 py-3 text-textLight hover:text-accent hover:bg-gray-800 transition-colors capitalize">kakheti</a></li>
                    <li><a href="{region_prefix}tbilisi.html" class="block px-4 py-3 text-textLight hover:text-accent hover:bg-gray-800 transition-colors capitalize">tbilisi</a></li>
                </ul>
            </li>
            <li class="w-full md:w-auto text-center md:text-left"><a href="{root_prefix}contact.html" class="block no-underline text-textLight hover:text-accent uppercase tracking-widest font-bold text-sm transition-colors duration-300">Contact</a></li>
        </ul>
    </nav>"""

def process_file(filepath):
    is_region = "regions" in filepath.replace('\\', '/')
    root_prefix = "../" if is_region else ""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace the <nav> element
    nav_pattern = r'<nav class="[^"]*".*?</nav>'
    content = re.sub(nav_pattern, get_nav_html(is_region), content, flags=re.DOTALL)
    
    # Inject nav.js before </body>
    script_tag = f'<script src="{root_prefix}js/nav.js"></script>'
    if script_tag not in content:
        content = content.replace('</body>', f'    {script_tag}\n</body>')
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Processed {filepath}")

def main():
    root_files = glob.glob(r"pub\*.html")
    region_files = glob.glob(r"pub\regions\*.html")
    
    for f in root_files + region_files:
        if "timothystours_old.html" in f:
            continue
        process_file(f)

if __name__ == "__main__":
    main()

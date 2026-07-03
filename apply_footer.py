import os
import re
import glob

pub_dir = r"C:\Users\shawn\.gemini\antigravity\scratch\DevAll\timothystours.dig.ge-working\pub"

def get_footer(is_in_regions_dir=False):
    prefix = "../" if is_in_regions_dir else ""
    regions_prefix = "" if is_in_regions_dir else "regions/"
    
    return f'''<footer class="bg-gray-900 py-12 border-t-4 border-primary mt-auto z-20 relative">
        <div class="max-w-6xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-12">
            <!-- Brand -->
            <div>
                <h3 class="font-serif text-2xl text-accent uppercase tracking-widest mb-4">Timothy's Tours</h3>
                <p class="text-gray-400 mb-6 leading-relaxed">Expert guidance through the rivers, dirt roads, and unpolished beauty of Georgia. No tourist traps, just the real deal.</p>
                <p class="text-gray-500 text-sm">&copy; 2026 Timothy's Tours. All rights reserved.</p>
            </div>
            
            <!-- Links -->
            <div>
                <h4 class="font-serif text-lg text-white uppercase tracking-widest mb-4">Explore</h4>
                <ul class="list-none p-0 flex flex-col gap-3">
                    <li><a href="{prefix}index.html" class="no-underline text-gray-400 hover:text-accent transition-colors">Home</a></li>
                    <li><a href="{prefix}about.html" class="no-underline text-gray-400 hover:text-accent transition-colors">About Me</a></li>
                    <li><a href="{prefix}trip-planning.html" class="no-underline text-gray-400 hover:text-accent transition-colors">Trip Planning</a></li>
                    <li><a href="{regions_prefix}index.html" class="no-underline text-gray-400 hover:text-accent transition-colors">Regions</a></li>
                    <li><a href="{prefix}contact.html" class="no-underline text-gray-400 hover:text-accent transition-colors">Contact</a></li>
                </ul>
            </div>
            
            <!-- Contact -->
            <div>
                <h4 class="font-serif text-lg text-white uppercase tracking-widest mb-4">Contact</h4>
                <ul class="list-none p-0 flex flex-col gap-3 mb-8">
                    <li><a href="mailto:timothy@timothystours.ge" class="no-underline text-gray-400 hover:text-accent transition-colors">timothy@timothystours.ge</a></li>
                    <li><a href="tel:+995598411778" class="no-underline text-gray-400 hover:text-accent transition-colors">+995 598 411 778</a></li>
                </ul>
                <div class="flex gap-6">
                    <a href="https://www.facebook.com/timothys.tours.georgia/" target="_blank" rel="noopener noreferrer" class="no-underline text-gray-400 hover:text-accent text-sm uppercase tracking-widest font-bold transition-colors">Facebook</a>
                    <a href="https://www.instagram.com/tiresias.monk/" target="_blank" rel="noopener noreferrer" class="no-underline text-gray-400 hover:text-accent text-sm uppercase tracking-widest font-bold transition-colors">Instagram</a>
                </div>
                <p class="mt-8 text-xs text-left md:text-right">Built by <a href="https://dig.ge" class="no-underline text-gray-500 hover:text-accent transition-colors">DIG</a></p>
            </div>
        </div>
    </footer>'''

def update_footers():
    # Gather all HTML files
    root_files = glob.glob(os.path.join(pub_dir, "*.html"))
    region_files = glob.glob(os.path.join(pub_dir, "regions", "*.html"))
    
    pattern = re.compile(r'<footer.*?>.*?</footer>', re.DOTALL)
    
    for filepath in root_files:
        if 'timothystours_old.html' in filepath:
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_footer = get_footer(is_in_regions_dir=False)
        content = pattern.sub(new_footer, content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            print(f"Updated footer in {os.path.basename(filepath)}")
            
    for filepath in region_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_footer = get_footer(is_in_regions_dir=True)
        content = pattern.sub(new_footer, content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            print(f"Updated footer in regions/{os.path.basename(filepath)}")

update_footers()

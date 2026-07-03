import os
import re
import json

regions_data = {
    "adjara.html": {
        "name": "Adjara",
        "h2_1": "Beyond the Neon Coast",
        "p_1": "Forget the overcrowded, neon-lit beaches of Batumi. Real Adjara isn't found in concrete resorts; it's carved into the steep, rain-drenched mountains of the interior. Here, sheer limestone gorges plunge into wild, untamed rivers, and the air smells of ancient forests and woodsmoke. The highland Adjarians are tough, resourceful, and unfailingly generous. We'll leave the coastal tourists behind to ride deep into the clouds, stopping for strong coffee and high-altitude cheeses you won't find on any restaurant menu.",
        "h2_2": "Deep Mountain Trails",
        "p_2": "This isn't your average scenic drive. The roads here are rough, cutting through dense jungles in the Mtirala and Kintrishi reserves. You'll meet herding families who bring their cattle up to the alpine zones each summer, living in wooden cottages perched on the edge of the world. It's raw, it's green, and it demands respect. If you want to see the real Adjara, lace up your boots and let's go."
    },
    "guria.html": {
        "name": "Guria",
        "h2_1": "The Subtropical Frontier",
        "p_1": "Guria is the Georgian wild west—a subtropical labyrinth of tea fields, ancient woodlands, and sharp ridges. Most tourists fly past it on the highway, entirely missing the magic hiding in the Lesser Caucasus foothills. Their loss is our gain. The Gurian people are fiercely proud, sharp-tongued, and fiercely hospitable. This is a land of heavy humidity and rolling green peaks where the terrain demands as much sweat as it rewards you with vistas.",
        "h2_2": "Tea, Trails, and Tradition",
        "p_2": "We bypass the artificial resorts. Instead, we push into the highlands, where mountain herding families spend their summers among endless fields of wildflowers and rhododendrons. You'll taste wild blueberry leaf tea, forage for subtropical fruits, and climb ridges that offer nothing but silence and sea clouds. Bring your stamina—Guria earns every ounce of your respect."
    },
    "imereti.html": {
        "name": "Imereti",
        "h2_1": "The Heart of the Karst",
        "p_1": "Imereti is vast, rugged, and unyielding. The sheer diversity of this province will chew up the unprepared. It's a subterranean battleground of karstic caves, sinkholes, and sweeping limestone plateaus scarred by old Soviet manganese mines. But look closer: between the stark canyons and the crumbling industrial towns, you'll find some of the richest gastronomy and fiercest mountain passes in the country.",
        "h2_2": "No Beaten Paths",
        "p_2": "We don't do the standard Kutaisi day trips. We head into the deep cuts—the unmapped waterfalls of the Khani valley, the dark natural tunnels of Tsutskhvati, and the grueling ascents up to the Zekari Pass. Imereti requires grit to explore properly, but the reward is a heavy slice of hot cheese bread from a village oven and a view that stretches to the edge of the Colchian plain."
    },
    "javakheti.html": {
        "name": "Javakheti",
        "h2_1": "The Volcanic Plateau",
        "p_1": "Welcome to the Georgian Siberia. Javakheti is a high-altitude, volcanic wasteland of alpine lakes, jagged obsidian outcrops, and bone-chilling winds. It's a harsh, unforgiving environment that weeds out casual tourists instantly. The winters are brutal, and the summers are fleeting. But for those willing to brave the elements, the stark beauty of this treeless plateau is unmatched.",
        "h2_2": "Ruins in the Wind",
        "p_2": "Megalithic fortresses stand like silent sentinels over the plains, battered by centuries of storms. We'll navigate the rutted tracks past flocks of sheep and ancient cyclopean ruins, pushing deep into a landscape that feels older than time itself. Pack layers and expect the wind to howl. Javakheti doesn't coddle its visitors."
    },
    "kakheti.html": {
        "name": "Kakheti",
        "h2_1": "The Sun-Baked East",
        "p_1": "Kakheti isn't just wine country; it's a sun-baked crucible of fertile valleys bordered by the towering, impenetrable wall of the Greater Caucasus. The heat here is heavy, and the history is written in blood and grape juice. Most people come for a polite winery tour. We're here to dig deeper—into the dusty plains of Vashlovani, the remote fortified villages, and the raw, unfiltered life of the winemakers who work this soil with calloused hands.",
        "h2_2": "Beyond the Vineyard",
        "p_2": "We trade the manicured chateaus for rugged 4x4 trails leading into the Gombori mountains and the semi-deserts bordering Azerbaijan. You'll sweat, you'll get dusty, and at the end of the day, you'll earn your glass of amber wine poured straight from a clay qvevri buried in the earth. Kakheti is a land of extremes. Be ready for them."
    },
    "kartli.html": {
        "name": "Kartli",
        "h2_1": "The Historic Crucible",
        "p_1": "Kartli is the backbone of Georgia. It's a central artery of sun-scorched plains, strategic river valleys, and wind-blasted ridges. This is where empires clashed, and the landscape is littered with the scars to prove it—ruined citadels, ancient cave cities, and battle-hardened monasteries. It's not a place for leisurely strolls; it's a place for reckoning with history in the raw elements.",
        "h2_2": "The Scars of Empires",
        "p_2": "Forget the sanitized tourist spots. We're heading off the highway to track down forgotten fortresses hidden in the Trialeti range and navigate the rugged gorge of the Mtkvari River. It's dry, it's rocky, and the sun beats down relentlessly. But if you want to understand the true resilience of the Georgian spirit, you have to walk the rough terrain of Kartli."
    },
    "lechkhumi.html": {
        "name": "Lechkhumi",
        "h2_1": "The Hidden Gorge",
        "p_1": "Lechkhumi is a secret tightly guarded by deep gorges, towering limestone peaks, and roads that barely cling to the mountainsides. It's one of the most inaccessible and least-visited regions in the country. The rivers here run fast and cold, cutting through dense, ancient forests. It's a place that demands a sturdy vehicle, strong legs, and a willingness to embrace the unknown.",
        "h2_2": "Untamed Valleys",
        "p_2": "You won't find tourist infrastructure here—just raw, unfiltered wilderness and villages that have defied gravity and time. We'll push up the Tskhenistskali river valley, navigating switchbacks and steep trails to reach viewpoints that will leave you breathless. Lechkhumi is rugged isolation at its finest. Don't expect a smooth ride."
    },
    "meskheti.html": {
        "name": "Meskheti",
        "h2_1": "The Borderlands",
        "p_1": "Meskheti is a labyrinth of steep pine-clad mountains, deep river canyons, and ancient terraced valleys. Straddling the Turkish border, it's a frontier land that feels heavily fortified and historically complex. The air is dry and smells of resin and dust. The terrain is unforgiving, but it hides architectural marvels carved directly into the bedrock.",
        "h2_2": "Carved from Rock",
        "p_2": "We aren't just looking at the famous cave city of Vardzia from a distance; we're exploring the rugged hinterlands that surround it. We'll hike through forgotten fortresses, navigate the rugged trails of the Mtkvari gorge, and uncover a landscape defined by centuries of struggle and survival. Meskheti is tough terrain. Wear good boots."
    },
    "mtianeti.html": {
        "name": "Mtianeti",
        "h2_1": "The High Crags",
        "p_1": "Mtianeti is the gateway to the high Caucasus, a realm of sheer rock faces, roaring alpine rivers, and weather that can turn deadly in an hour. It's where the Georgian Military Highway cuts a brutal path through the mountains. This isn't a place for the faint of heart. The altitude is high, the air is thin, and the landscapes are staggeringly huge.",
        "h2_2": "Thin Air and Stone",
        "p_2": "We leave the asphalt behind and take to the trails. Whether it's pushing up towards the glaciers of Mount Kazbek or exploring the isolated, stone-built villages of the Sno Valley, Mtianeti demands physical effort. It's a landscape that tests your limits and rewards you with views that make you feel entirely insignificant."
    },
    "racha.html": {
        "name": "Racha",
        "h2_1": "The Alpine Bastion",
        "p_1": "Racha is surrounded by an impenetrable fortress of limestone ridges and snow-capped peaks. It's slower-paced than the rest of Georgia, but don't mistake that for softness. The mountains here are massive, the forests are deep and full of bears, and the trails are steep and challenging. It's a region of heavy snowfall, dense woods, and powerful, cold rivers.",
        "h2_2": "Deep in the Woods",
        "p_2": "We bypass the central towns and head straight into the high-altitude wilderness. Expect long, grueling hikes up the Rioni River gorge and into the remote glaciated valleys. The reward? Pristine alpine lakes, ancient defensive towers, and a level of quiet isolation that's increasingly hard to find. Racha is wild. We'll keep it that way."
    },
    "samegrelo.html": {
        "name": "Samegrelo",
        "h2_1": "From Swamps to Alpine Peaks",
        "p_1": "Samegrelo is a land of stark contrasts—from the impenetrable, humid swamps of the Colchian lowlands to the jagged, sheer rock teeth of the Egrisi mountains. The people are fiercely independent and the food is notoriously spicy, hot enough to make you sweat. It's a lush, dense, and aggressively green region that hides deep, water-carved canyons and forgotten fortresses.",
        "h2_2": "Into the Green Hell",
        "p_2": "Forget the polite paths. We delve into the deep canyons of Martvili and the rugged, forested slopes of the Egrisi range. You'll be wading through ice-cold rivers, hacking through dense undergrowth, and pushing up to alpine pastures where the weather changes on a dime. Samegrelo is an adventure that requires grit."
    },
    "svaneti.html": {
        "name": "Svaneti",
        "h2_1": "The Unconquered Towers",
        "p_1": "Svaneti is the roof of Europe, a brutal, high-altitude world of glaciers, avalanches, and medieval stone towers. The Svans have lived up here for millennia, surviving some of the harshest winters on earth. This is serious alpine territory. The mountains don't care about your itinerary, and the weather commands absolute respect.",
        "h2_2": "Vertical Ascents",
        "p_2": "We aren't here to take pictures from the valley floor. We're heading up—way up. We'll tackle the steep, lung-busting trails that lead to the Shkhara glacier and the remote passes connecting the high villages. Svaneti is rugged, raw, and dangerous if you don't know what you're doing. Stick with me, and we'll conquer it."
    },
    "tbilisi.html": {
        "name": "Tbilisi",
        "h2_1": "The Urban Crucible",
        "p_1": "Tbilisi is a chaotic collision of empires, built in a deep gorge and baked by the summer sun. It's not a polished European capital; it's a gritty, layered city where crumbling 19th-century balconies overhang steep, cobbled alleys and brutalist Soviet concrete blocks the skyline. It's loud, it's fast, and it's unashamedly real.",
        "h2_2": "Concrete and Cobblestones",
        "p_2": "We skip the tourist traps and dive into the backstreets. We'll hike the steep, scrub-covered hills of Mtatsminda, explore the forgotten, crumbling courtyards of Sololaki, and navigate the labyrinthine alleys where the real life of the city pulses. Tbilisi takes no prisoners, and it rewards those willing to get a little dust on their boots."
    }
}

target_dir = r"C:\Users\shawn\.gemini\antigravity\scratch\DevAll\timothystours.dig.ge-working\pub\regions"
pub_dir = r"C:\Users\shawn\.gemini\antigravity\scratch\DevAll\timothystours.dig.ge-working\pub"

# 1. Update Region Pages (SEO + A11y Nav + A11y Contrast)
for filename, data in regions_data.items():
    filepath = os.path.join(target_dir, filename)
    if not os.path.exists(filepath):
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # SEO: Schema
    schema = {
        "@context": "https://schema.org",
        "@type": "TouristDestination",
        "name": data["name"],
        "description": data["p_1"],
        "url": f"https://timothystours.dig.ge/regions/{filename}"
    }
    schema_script = f'\n    <script type="application/ld+json">\n    {json.dumps(schema, indent=4)}\n    </script>\n</head>'

    if '<script type="application/ld+json">' not in content:
        content = content.replace("</head>", schema_script)

    # SEO/Copywriter: Content
    new_section = f'''<section class="py-20 px-8 max-w-4xl mx-auto relative z-10 text-lg text-gray-300">
            <h2 class="text-2xl text-accent font-serif mb-4 mt-8">{data["h2_1"]}</h2>
            <p class="mb-6">{data["p_1"]}</p>
            <h2 class="text-2xl text-accent font-serif mb-4 mt-8">{data["h2_2"]}</h2>
            <p class="mb-6">{data["p_2"]}</p>
        </section>'''

    content = re.sub(
        r'<section class="py-20 px-8 max-w-4xl mx-auto relative z-10 text-lg text-gray-300">.*?</section>',
        new_section,
        content,
        flags=re.DOTALL
    )

    # A11y: Contrast on CTA
    content = content.replace("hover:text-primary", "hover:text-accent")

    # A11y: Nav semantic HTML (<div> to <ul>)
    nav_match = re.search(r'<div class="flex gap-6 hidden md:flex">(.*?)</div>', content, re.DOTALL)
    if nav_match:
        links = nav_match.group(1).strip()
        # Wrap links in <li>
        new_links = "\\n            ".join([f"<li>{a.strip()}</li>" for a in links.split("\\n") if a.strip()])
        new_nav = f'<ul class="flex gap-6 hidden md:flex list-none m-0 p-0">\n            {new_links}\n        </ul>'
        content = content.replace(nav_match.group(0), new_nav)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# 2. Global Updates (index.html, about.html, contact.html, trip-planning.html, regions/index.html)
global_files = ["index.html", "about.html", "contact.html", "trip-planning.html", "regions/index.html"]
for filename in global_files:
    filepath = os.path.join(pub_dir, filename.replace("/", os.sep))
    if not os.path.exists(filepath):
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # A11y: Contrast
    content = content.replace("hover:text-primary", "hover:text-accent")

    # A11y: Nav semantic HTML
    nav_match = re.search(r'<div class="flex gap-6 hidden md:flex">(.*?)</div>', content, re.DOTALL)
    if nav_match:
        links = nav_match.group(1).strip()
        new_links = "\\n            ".join([f"<li>{a.strip()}</li>" for a in links.split("\\n") if a.strip()])
        new_nav = f'<ul class="flex gap-6 hidden md:flex list-none m-0 p-0">\n            {new_links}\n        </ul>'
        content = content.replace(nav_match.group(0), new_nav)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Applied A11y (Contrast & Nav) and SEO (Schema & Brand Voice Rewrite) to all files.")

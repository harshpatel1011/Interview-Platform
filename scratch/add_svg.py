import os
import re

templates_dir = r'c:\Users\HARSH PATEL\Patel\Coding\Creative Institute\AI\Interview Platform\templates\emails'

logo_html = '<div style="background-color: #ffffff; color: #000000; display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 8px; margin-right: 10px; vertical-align: middle;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" style="width: 16px; height: 16px;"><path d="M 28 30 L 12 50 L 28 70" /><path d="M 72 30 L 88 50 L 72 70" /><path d="M 50 32 L 50 68" /><path d="M 32 50 L 68 50" /></svg></div>'

for filename in os.listdir(templates_dir):
    if not filename.endswith('.html'):
        continue
    filepath = os.path.join(templates_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to replace >TechPlus with >logo_htmlTechPlus
    # Make sure we don't duplicate it if it's already there
    if logo_html not in content and '>TechPlus' in content:
        # replace only the first occurrence to avoid messing up footer Text if it has >TechPlus
        # actually footer has "} TechPlus. All rights reserved." or something
        # Let's target the exact logo container
        content = re.sub(r'(display:inline-block;\s*letter-spacing:-0\.5px[^>]*>)(\s*)TechPlus', rf'\1\2{logo_html}TechPlus', content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Added SVG back to {filename}')

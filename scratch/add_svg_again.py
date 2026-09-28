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
    
    # We want to replace TechPlus with logo_html TechPlus but only inside the header logo div
    # In the new html, it looks like:
    # <div class="logo" style="...letter-spacing:-0.5px">
    #                 TechPlus
    # </div>
    
    # Let's replace just the exact string match if possible
    # We can use regex to match the exact pattern
    content = re.sub(
        r'(letter-spacing:-0\.5px[^>]*>)(\s*)TechPlus(\s*</div>)',
        rf'\1\2{logo_html}TechPlus\3',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Added SVG back to {filename}')

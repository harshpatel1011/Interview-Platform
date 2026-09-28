import os
import re

templates_dir = r'c:\Users\HARSH PATEL\Patel\Coding\Creative Institute\AI\Interview Platform\templates\emails'

color_map = {
    '168,85,247': {'hex': '#A855F7', 'text': '#ffffff'}, # Purple
    '16,185,129': {'hex': '#10B981', 'text': '#ffffff'}, # Green
    '245,158,11': {'hex': '#F59E0B', 'text': '#000000'}, # Yellow
    '59,130,246': {'hex': '#3B82F6', 'text': '#ffffff'}, # Blue
    '239,68,68':  {'hex': '#EF4444', 'text': '#ffffff'}, # Red
}

for filename in os.listdir(templates_dir):
    if not filename.endswith('.html'):
        continue
        
    filepath = os.path.join(templates_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find the glow color
    match = re.search(r'rgba\((\d+,\d+,\d+)', content)
    if not match:
        continue
        
    rgb = match.group(1)
    if rgb in color_map:
        btn_hex = color_map[rgb]['hex']
        btn_text = color_map[rgb]['text']
        
        # Replace the btn CSS
        # Looking for .btn { ... background-color: #ffffff; color: #000000; ... }
        # Let's just use regex to replace background-color and color in .btn
        
        # It's safer to just replace the exact string if we know it
        old_btn_style = "background-color: #ffffff; color: #000000;"
        new_btn_style = f"background-color: {btn_hex}; color: {btn_text};"
        
        if old_btn_style in content:
            content = content.replace(old_btn_style, new_btn_style)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filename} with button color {btn_hex}")
        else:
            print(f"Could not find exact button style in {filename}")


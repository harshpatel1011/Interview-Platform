import os
import re

templates_dir = r'c:\Users\HARSH PATEL\Patel\Coding\Creative Institute\AI\Interview Platform\templates\emails'

count = 0
for filename in os.listdir(templates_dir):
    if not filename.endswith('.html'):
        continue
    filepath = os.path.join(templates_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to replace the thematic color in .logo-box and the inline style for the logo back to white/black
    
    # First, find the glow color used for the button to know what color to replace
    # Wait, it's easier to just use regex to replace all `.logo-box { background-color: #XXXXXX; color: #XXXXXX;`
    content = re.sub(
        r'\.logo-box\s*\{\s*background-color:\s*#[0-9a-fA-F]+;\s*color:\s*#[0-9a-fA-F]+;',
        r'.logo-box { background-color: #ffffff; color: #000000;',
        content
    )
    
    # Second, replace the inline style
    content = re.sub(
        r'<div style="background-color:\s*#[0-9a-fA-F]+;\s*color:\s*#[0-9a-fA-F]+;\s*(display:\s*inline-flex;.*?width:\s*32px;\s*height:\s*32px;)',
        r'<div style="background-color: #ffffff; color: #000000; \1',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    count += 1
    
print(f'Reverted logo color in {count} emails.')

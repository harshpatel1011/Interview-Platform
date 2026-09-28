import os
import re

templates_dir = r'c:\Users\HARSH PATEL\Patel\Coding\Creative Institute\AI\Interview Platform\templates\emails'

for filename in os.listdir(templates_dir):
    if not filename.endswith('.html'):
        continue
    filepath = os.path.join(templates_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the empty logo box div
    content = re.sub(r'<div style="background-color: #ffffff; color: #000000; display: inline-flex;[^>]+></div>', '', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

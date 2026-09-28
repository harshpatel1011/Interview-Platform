import os
import re
from premailer import transform

templates_dir = r'c:\Users\HARSH PATEL\Patel\Coding\Creative Institute\AI\Interview Platform\templates\emails'

for filename in os.listdir(templates_dir):
    if not filename.endswith('.html'):
        continue
        
    filepath = os.path.join(templates_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    # Remove SVG entirely
    html_content = re.sub(r'<svg.*?</svg>', '', html_content, flags=re.DOTALL)
    
    # Hide Django tags and HTML entities that premailer might mangle
    placeholders = {}
    
    def tag_replacer(match):
        placeholder = f"__DJANGO_TAG_{len(placeholders)}__"
        placeholders[placeholder] = match.group(0)
        return placeholder
        
    html_content = re.sub(r'\{\{.*?\}\}', tag_replacer, html_content)
    html_content = re.sub(r'\{%.*?%\}', tag_replacer, html_content)
    html_content = html_content.replace('&copy;', '__COPY_ENTITY__')
    html_content = html_content.replace('&rarr;', '__RARR_ENTITY__')
    
    # Process with premailer
    inlined_html = transform(html_content, preserve_internal_links=True, disable_validation=True)
    
    # Restore the tags
    for placeholder, original_tag in placeholders.items():
        inlined_html = inlined_html.replace(placeholder, original_tag)
        
    inlined_html = inlined_html.replace('__COPY_ENTITY__', '&copy;')
    inlined_html = inlined_html.replace('__RARR_ENTITY__', '&rarr;')
        
    if '<!DOCTYPE' not in inlined_html:
        inlined_html = '<!DOCTYPE html>\n' + inlined_html
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(inlined_html)
        
    print(f"Inlined CSS for {filename}")

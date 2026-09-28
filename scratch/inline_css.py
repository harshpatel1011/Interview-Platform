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
        
    # Remove SVG icons because they break email clients
    html_content = re.sub(r'<svg.*?</svg>', '', html_content, flags=re.DOTALL)
    
    # 1. Extract all Django template tags
    placeholders = {}
    
    def tag_replacer(match):
        placeholder = f"__DJANGO_TAG_{len(placeholders)}__"
        placeholders[placeholder] = match.group(0)
        return placeholder
        
    html_content = re.sub(r'\{\{.*?\}\}', tag_replacer, html_content)
    html_content = re.sub(r'\{%.*?%\}', tag_replacer, html_content)
    
    # ADD UTF-8 META TAG TO FIX LXML ENCODING ISSUES!
    if '<meta charset=' not in html_content:
        html_content = html_content.replace('<head>', '<head>\n    <meta charset="utf-8">')
        
    # Process with premailer
    inlined_html = transform(html_content, preserve_internal_links=True, disable_validation=True)
    
    # Restore the Django tags
    for placeholder, original_tag in placeholders.items():
        inlined_html = inlined_html.replace(placeholder, original_tag)
        
    if '<!DOCTYPE' not in inlined_html:
        inlined_html = '<!DOCTYPE html>\n' + inlined_html
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(inlined_html)
        
    print(f"Inlined CSS for {filename}")

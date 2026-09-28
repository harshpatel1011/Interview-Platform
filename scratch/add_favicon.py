import os

filepath = r'c:\Users\HARSH PATEL\Patel\Coding\Creative Institute\AI\Interview Platform\templates\base.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add load static if not present
if '{% load static %}' not in content:
    content = '{% load static %}\n' + content

# Add favicon
if 'rel="icon"' not in content:
    favicon_tag = '<link rel="icon" type="image/svg+xml" href="{% static \'images/logo_concept_1.svg\' %}">'
    content = content.replace('<head>', f'<head>\n    {favicon_tag}')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

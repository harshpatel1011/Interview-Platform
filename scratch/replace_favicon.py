import os

filepath = r'c:\Users\HARSH PATEL\Patel\Coding\Creative Institute\AI\Interview Platform\templates\base.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the static tag with the data URI
old_favicon = '<link rel="icon" type="image/svg+xml" href="{% static \'images/logo_concept_1.svg\' %}">'
new_favicon = '<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'%3E%3Crect width=\'100\' height=\'100\' rx=\'22\' fill=\'%23ffffff\'/%3E%3Cg fill=\'none\' stroke=\'%23000000\' stroke-width=\'10\' stroke-linecap=\'round\' stroke-linejoin=\'round\'%3E%3Cpath d=\'M 28 30 L 12 50 L 28 70\' /%3E%3Cpath d=\'M 72 30 L 88 50 L 72 70\' /%3E%3Cpath d=\'M 50 32 L 50 68\' /%3E%3Cpath d=\'M 32 50 L 68 50\' /%3E%3C/g%3E%3C/svg%3E">'

if old_favicon in content:
    content = content.replace(old_favicon, new_favicon)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Favicon replaced with Data URI!')
else:
    print('Old favicon not found!')

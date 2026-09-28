import os

templates_dir = r'c:\Users\HARSH PATEL\Patel\Coding\Creative Institute\AI\Interview Platform\templates\emails'

old_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512" fill="currentColor" style="width: 14px; height: 14px;"><path d="M264.5 5.2c14.9-6.9 32.1-6.9 47 0l218.6 101c8.5 3.9 13.9 12.4 13.9 21.8s-5.4 17.9-13.9 21.8l-218.6 101c-14.9 6.9-32.1 6.9-47 0L45.9 149.8C37.4 145.9 32 137.4 32 128s5.4-17.9 13.9-21.8L264.5 5.2zM476.9 209.6l53.2 24.6c8.5 3.9 13.9 12.4 13.9 21.8s-5.4 17.9-13.9 21.8l-218.6 101c-14.9 6.9-32.1 6.9-47 0L45.9 277.8C37.4 273.9 32 265.4 32 256s5.4-17.9 13.9-21.8l53.2-24.6 152 70.2c23.4 10.8 50.4 10.8 73.8 0l152-70.2zM476.9 337.6l53.2 24.6c8.5 3.9 13.9 12.4 13.9 21.8s-5.4 17.9-13.9 21.8l-218.6 101c-14.9 6.9-32.1 6.9-47 0L45.9 405.8C37.4 401.9 32 393.4 32 384s5.4-17.9 13.9-21.8l53.2-24.6 152 70.2c23.4 10.8 50.4 10.8 73.8 0l152-70.2z"/></svg>'

new_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" style="width: 16px; height: 16px;"><path d="M 28 30 L 12 50 L 28 70" /><path d="M 72 30 L 88 50 L 72 70" /><path d="M 50 32 L 50 68" /><path d="M 32 50 L 68 50" /></svg>'

count = 0
for filename in os.listdir(templates_dir):
    if not filename.endswith('.html'):
        continue
    filepath = os.path.join(templates_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_svg in content:
        content = content.replace(old_svg, new_svg)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
print(f'Updated {count} email templates.')

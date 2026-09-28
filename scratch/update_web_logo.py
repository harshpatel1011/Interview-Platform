import os
import glob

templates = glob.glob(r'c:\Users\HARSH PATEL\Patel\Coding\Creative Institute\AI\Interview Platform\templates\**\*.html', recursive=True)

old_sm = '<i class="fa-solid fa-layer-group text-black text-sm"></i>'
new_sm = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4 text-black"><path d="M 28 30 L 12 50 L 28 70" /><path d="M 72 30 L 88 50 L 72 70" /><path d="M 50 32 L 50 68" /><path d="M 32 50 L 68 50" /></svg>'

old_xs = '<i class="fa-solid fa-layer-group text-black text-[10px]"></i>'
new_xs = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" class="w-3 h-3 text-black"><path d="M 28 30 L 12 50 L 28 70" /><path d="M 72 30 L 88 50 L 72 70" /><path d="M 50 32 L 50 68" /><path d="M 32 50 L 68 50" /></svg>'

count = 0
for filepath in templates:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    if old_sm in content:
        content = content.replace(old_sm, new_sm)
        modified = True
    if old_xs in content:
        content = content.replace(old_xs, new_xs)
        modified = True
        
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1

print(f'Updated {count} web templates.')

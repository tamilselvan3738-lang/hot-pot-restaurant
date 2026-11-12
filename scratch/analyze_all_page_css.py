import glob
import re

public_pages = [
    'index.html',
    'about.html',
    'menu.html',
    'contact.html',
    'experience.html',
    'gallery.html',
    'offers.html',
    'reservation.html',
    'resources.html',
    'home-2.html'
]

for p in public_pages:
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Extract style block
    m = re.search(r'<style>([\s\S]*?)</style>', text)
    if not m:
        print(f"[{p}] NO STYLE TAG")
        continue
    style = m.group(1)
    
    # Check existing media queries inside the style
    mqs = re.findall(r'@media[^{]+', style)
    print(f"\n[{p}] Style length: {len(style)} | Media queries: {len(mqs)}")
    for mq in mqs:
        clean_mq = ' '.join(mq.split())
        print(f"   {clean_mq}")

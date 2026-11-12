import glob
import re

files = sorted(glob.glob('*.html'))

print("=== SCANNING FOR POTENTIAL OVERFLOW HAZARDS ===")

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    
    # 1. min-width >= 320px
    min_widths = re.findall(r'min-width:\s*([3-9]\d{2,}|[1-9]\d{3,})px', c)
    # 2. fixed width >= 340px in CSS
    fixed_widths = re.findall(r'(?:^|[^-])width:\s*([4-9]\d{2,}|[1-9]\d{3,})px', c)
    # 3. grid-template-columns without auto-fit or auto-fill
    grids = re.findall(r'grid-template-columns:\s*([^;]+);', c)
    hardcoded_grids = [g for g in grids if ('repeat(3,' in g or 'repeat(4,' in g or 'repeat(5,' in g or 'repeat(6,' in g) and 'minmax' not in g]
    
    # 4. Check global overflow-x: hidden
    has_html_overflow = bool(re.search(r'html[^{]*\{[^}]*overflow-x:\s*hidden', c))
    has_body_overflow = bool(re.search(r'body[^{]*\{[^}]*overflow-x:\s*hidden', c))
    has_universal_box_sizing = 'box-sizing: border-box' in c
    
    print(f"\n[{f}]")
    print(f"  html overflow-x:hidden: {has_html_overflow} | body overflow-x:hidden: {has_body_overflow} | box-sizing: {has_universal_box_sizing}")
    if min_widths:
        print(f"  min-widths >= 320px: {set(min_widths)}")
    if fixed_widths:
        print(f"  fixed widths >= 400px: {len(fixed_widths)} occurrences (samples: {set(fixed_widths[:5])})")
    if hardcoded_grids:
        print(f"  hardcoded multi-col grids: {len(hardcoded_grids)} (samples: {hardcoded_grids[:3]})")

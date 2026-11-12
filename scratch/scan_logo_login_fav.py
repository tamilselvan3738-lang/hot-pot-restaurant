import os, re

html_files = [f for f in sorted(os.listdir(r'd:\Projects\hot pot restaurant')) if f.endswith('.html')]

print("=== LOGO OCCURRENCES ===")
for f in html_files:
    with open(f, 'r', encoding='utf-8') as fh:
        c = fh.read()
    logos = re.findall(r'<a[^>]*brand-logo[^>]*>', c)
    brand_headers = re.findall(r'<div[^>]*card-brand-header[^>]*>', c)
    admin_logos = re.findall(r'<div[^>]*admin-brand[^>]*>', c)
    print(f"[{f}]: brand-logo tags={len(logos)}, card-brand-header={len(brand_headers)}, admin-brand={len(admin_logos)}")

print("\n=== LOGIN / LOGOUT OCCURRENCES ===")
for f in html_files:
    with open(f, 'r', encoding='utf-8') as fh:
        c = fh.read()
    login_matches = re.findall(r'<(?:button|a)[^>]*(?:login|logout)[^>]*>', c, re.IGNORECASE)
    print(f"[{f}]: login/logout elements={len(login_matches)}")
    for m in login_matches[:5]:
        print("  -", m[:100])

print("\n=== FAVICON OCCURRENCES ===")
for f in html_files:
    with open(f, 'r', encoding='utf-8') as fh:
        c = fh.read()
    favicons = re.findall(r'<link[^>]*rel="[^"]*icon[^"]*"[^>]*>', c, re.IGNORECASE)
    print(f"[{f}]: favicons={len(favicons)} -> {favicons}")

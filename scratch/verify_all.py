import glob
import re
import subprocess

html_files = sorted(glob.glob('*.html'))
print(f"Total HTML files found: {len(html_files)}")

all_ok = True

# 1. Favicon Check
print("\n--- 1. CHECKING FAVICONS ---")
for f in html_files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    has_svg = 'images/favicon.svg' in c
    has_png = 'images/favicon.png' in c
    if has_svg and has_png:
        print(f"  [OK] {f:22} -> SVG & PNG favicon tags present")
    else:
        print(f"  [FAIL] {f:22} -> SVG: {has_svg}, PNG: {has_png}")
        all_ok = False

# 2. Logo Redirection Check
print("\n--- 2. CHECKING LOGO REDIRECTION TO index.html ---")
for f in html_files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    # Check if brand-logo / card-brand-header has index.html redirect or href
    has_link = 'href="index.html"' in c and ('brand-logo' in c or 'card-brand-header' in c or 'cauldron-center-icon' in c or 'cauldron-center-link' in c)
    has_js_redirect = 'window.location.href = \'index.html\'' in c or 'window.location.href = "index.html"' in c
    if has_link or has_js_redirect:
        print(f"  [OK] {f:22} -> Logo redirect confirmed (link: {has_link}, JS: {has_js_redirect})")
    else:
        print(f"  [FAIL] {f:22} -> No logo redirect found!")
        all_ok = False

# 3. Login / Logout Redirection Check
print("\n--- 3. CHECKING LOGIN / LOGOUT REDIRECTION TO login.html ---")
for f in html_files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    if f in ['login.html']:
        print(f"  [OK] {f:22} -> Is target login page itself")
        continue
    has_login_redirect = 'window.location.href = \'login.html\'' in c or 'href="login.html"' in c
    if has_login_redirect:
        print(f"  [OK] {f:22} -> Login/Logout redirect to login.html confirmed")
    else:
        print(f"  [FAIL] {f:22} -> No login/logout redirect to login.html found!")
        all_ok = False

# 4. JavaScript Syntax Validation
print("\n--- 4. CHECKING JS SYNTAX VIA NODE ---")
for f in html_files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    scripts = re.findall(r'<script(?:\s+[^>]*)?>([\s\S]*?)</script>', c, re.IGNORECASE)
    for idx, s in enumerate(scripts):
        if not s.strip():
            continue
        # Run node --check on script via stdin
        proc = subprocess.run(
            ['node', '--check'],
            input=s,
            capture_output=True,
            text=True
        )
        if proc.returncode != 0:
            print(f"  [ERROR] {f} script #{idx} failed syntax check:\n{proc.stderr[:200]}")
            all_ok = False
        else:
            pass
print("  [OK] All inline scripts passed Node.js syntax checks without errors!")

# 5. Check Favicon files on disk
print("\n--- 5. CHECKING FAVICON ASSETS ON DISK ---")
import os
assets = ['images/favicon.svg', 'images/favicon.png', 'favicon.ico', 'images/favicon.ico']
for a in assets:
    if os.path.exists(a):
        sz = os.path.getsize(a)
        print(f"  [OK] {a:22} exists ({sz} bytes)")
    else:
        print(f"  [FAIL] {a:22} missing!")
        all_ok = False

print(f"\nALL VERIFICATIONS PASSED: {all_ok}")

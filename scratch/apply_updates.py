import os
import re

files_all = [
    '404.html',
    'about.html',
    'admin-dashboard.html',
    'contact.html',
    'experience.html',
    'gallery.html',
    'home-2.html',
    'index.html',
    'login.html',
    'menu.html',
    'navbar.html',
    'offers.html',
    'registeration.html',
    'reservation.html',
    'user-dashboard.html'
]

favicon_snippet = '''  <!-- Authentic Brand Hot Pot Favicon -->
  <link rel="icon" type="image/svg+xml" href="images/favicon.svg">
  <link rel="alternate icon" type="image/png" href="images/favicon.png">
'''

# 1. Favicon injection
for fn in files_all:
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'images/favicon.svg' not in content:
        # Insert after <meta name="viewport" ...>
        viewport_pattern = re.compile(r'(<meta\s+name=["\']viewport["\'][^>]*>)', re.IGNORECASE)
        m = viewport_pattern.search(content)
        if m:
            content = content[:m.end()] + '\n' + favicon_snippet + content[m.end():]
            with open(fn, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'[Favicon] Added to {fn}')
        else:
            # Fallback before </head>
            idx = content.find('</head>')
            if idx != -1:
                content = content[:idx] + favicon_snippet + '\n' + content[idx:]
                with open(fn, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'[Favicon] Added before </head> in {fn}')
    else:
        print(f'[Favicon] Already present in {fn}')

# 2. Main 10 pages script updates for logo & login redirect
target_pages = [
    'index.html',
    'about.html',
    'menu.html',
    'experience.html',
    'contact.html',
    'gallery.html',
    'offers.html',
    'reservation.html',
    'home-2.html',
    'navbar.html'
]

for fn in target_pages:
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # A. Update openLoginModal
    old_modal_pattern = re.compile(r'function openLoginModal\(\)\s*\{[\s\S]*?closeDrawer\(\);\s*\}', re.MULTILINE)
    new_modal_func = '''function openLoginModal() {
        window.location.href = 'login.html';
      }'''

    if old_modal_pattern.search(content):
        content = old_modal_pattern.sub(new_modal_func, content)
        modified = True
        print(f'[{fn}] Replaced openLoginModal definition with redirect to login.html')
    else:
        # Check if already updated
        if 'window.location.href = \'login.html\';' in content and 'openLoginModal' in content:
            print(f'[{fn}] openLoginModal already redirects')
        else:
            print(f'[{fn}] Warning: openLoginModal pattern not matched')

    # B. Add universal logo redirect & login handlers if not already present
    hook_marker = '// --- 7. MODAL WINDOW'
    if hook_marker in content and '/* UNIVERSAL LOGO & LOGIN REDIRECTS */' not in content:
        replacement = '''/* UNIVERSAL LOGO & LOGIN REDIRECTS */
      document.querySelectorAll('.brand-logo, .footer-brand-logo').forEach(function(el) {
        el.addEventListener('click', function(e) {
          e.preventDefault();
          window.location.href = 'index.html';
        });
      });

      document.querySelectorAll('#loginBtn, #mobileLoginBtn, #footerLoginLink, #ofrMemberLoginBtn').forEach(function(el) {
        el.addEventListener('click', function(e) {
          e.preventDefault();
          window.location.href = 'login.html';
        });
      });

      ''' + hook_marker

        content = content.replace(hook_marker, replacement, 1)
        modified = True
        print(f'[{fn}] Injected universal logo and login listeners')

    # C. In offers.html specifically, check if ofrMemberLoginBtn handler is updated
    if fn == 'offers.html':
        if 'ofrMemberLoginBtn' in content and 'window.location.href = \'login.html\'' not in content:
            content = content.replace(
                "ofrMemberLoginBtn.addEventListener('click', openLoginModal);",
                "ofrMemberLoginBtn.addEventListener('click', () => { window.location.href = 'login.html'; });"
            )
            modified = True
            print('[offers.html] Updated ofrMemberLoginBtn handler')

    if modified:
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'[{fn}] Saved successfully.')

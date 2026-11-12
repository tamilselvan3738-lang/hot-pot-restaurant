import os
import re

MARKER_START = "/* === FULL MOBILE RESPONSIVE ENGINE (320px, 480px, 768px, 1024px) === */"
MARKER_END = "/* === END MOBILE RESPONSIVE ENGINE === */"

def wrap_responsive_block(css_content):
    return f"\n{MARKER_START}\n{css_content.strip()}\n{MARKER_END}\n"

def inject_or_replace_responsive(filepath, css_content):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_block = wrap_responsive_block(css_content)

    # Check if marker already exists
    if MARKER_START in content and MARKER_END in content:
        pattern = re.compile(rf"{re.escape(MARKER_START)}[\s\S]*?{re.escape(MARKER_END)}")
        content = pattern.sub(new_block.strip(), content)
        print(f"[{filepath}] Updated existing mobile responsive engine.")
    else:
        # Insert before </style>
        idx = content.rfind("</style>")
        if idx != -1:
            content = content[:idx] + new_block + content[idx:]
            print(f"[{filepath}] Injected new mobile responsive engine before </style>.")
        else:
            print(f"[{filepath}] ERROR: </style> not found!")
            return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

# -------------------------------------------------------------
# 1. CORE RESPONSIVE BASELINE (included across all pages)
# -------------------------------------------------------------
CORE_BASELINE = """
/* 1. Global Box Sizing & Anti-Overflow */
html {
  box-sizing: border-box !important;
  overflow-x: hidden !important;
  max-width: 100vw !important;
  width: 100% !important;
  -webkit-text-size-adjust: 100%;
}

*, *::before, *::after {
  box-sizing: inherit !important;
}

body {
  overflow-x: hidden !important;
  max-width: 100vw !important;
  width: 100% !important;
  position: relative !important;
  word-wrap: break-word !important;
  overflow-wrap: break-word !important;
}

/* 2. Media Asset Fluidity */
img, svg, video, canvas, picture {
  max-width: 100% !important;
  height: auto;
}

/* 3. Text & Inline Element Boundaries */
h1, h2, h3, h4, h5, h6, p, span, a, li, blockquote, dt, dd, th, td, label {
  overflow-wrap: break-word !important;
  word-break: break-word !important;
}

/* 4. Universal Form Element Adaptability */
button, input, select, textarea {
  max-width: 100% !important;
  box-sizing: border-box !important;
}

/* 5. RTL Directional Icon Alignment */
[dir="rtl"] {
  direction: rtl;
  text-align: right;
}

[dir="rtl"] .icon-left, [dir="rtl"] svg.icon-left {
  margin-left: 8px !important;
  margin-right: 0 !important;
}

[dir="rtl"] .icon-right, [dir="rtl"] svg.icon-right {
  margin-right: 8px !important;
  margin-left: 0 !important;
  transform: scaleX(-1);
}
"""

print("Base setup ready.")

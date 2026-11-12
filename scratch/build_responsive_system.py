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

    if MARKER_START in content and MARKER_END in content:
        pattern = re.compile(rf"{re.escape(MARKER_START)}[\s\S]*?{re.escape(MARKER_END)}")
        content = pattern.sub(new_block.strip(), content)
        print(f"[{filepath}] Updated existing mobile responsive engine.")
    else:
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

CSS_INDEX = CORE_BASELINE + """
/* --- INDEX.HTML RESPONSIVE BREAKPOINTS --- */
@media (max-width: 1024px) {
  .hp-section { padding: 80px 24px !important; }
  .hp-hero-grid, .hp-communal-grid, .hp-ing-split, .hp-specials-grid {
    grid-template-columns: 1fr !important;
    gap: 32px !important;
  }
  .hp-broth-grid, .hp-pillars-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 20px !important;
  }
  .hp-metrics-row {
    grid-template-columns: repeat(2, 1fr) !important;
  }
  .hp-hero-title {
    font-size: clamp(2.2rem, 5vw, 3.2rem) !important;
  }
}

@media (max-width: 768px) {
  .hp-section { padding: 65px 18px !important; }
  .hp-broth-grid, .hp-pillars-grid, .hp-specials-grid, .hp-combos-grid, .hp-hero-grid, .hp-communal-grid {
    grid-template-columns: 1fr !important;
    gap: 20px !important;
  }
  .hp-broth-card, .hp-special-card, .hp-combo-row, .hp-pillar-card {
    width: 100% !important;
    margin-bottom: 16px !important;
  }
  .hp-hero-actions, .cta-actions, .hp-reserve-actions {
    flex-direction: column !important;
    width: 100% !important;
    gap: 12px !important;
    align-items: stretch !important;
  }
  .hp-cta-primary, .hp-cta-secondary, .cta-secondary-btn, .btn-3d-login.cta-reserve-btn {
    width: 100% !important;
    min-height: 48px !important;
    justify-content: center !important;
    text-align: center !important;
  }
  .hp-hero-title {
    font-size: clamp(1.85rem, 5.5vw, 2.4rem) !important;
    line-height: 1.15 !important;
  }
  .hp-sec-title {
    font-size: clamp(1.5rem, 4.5vw, 1.95rem) !important;
    line-height: 1.2 !important;
  }
  .hp-hero-desc, .hp-sec-desc {
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
  }
  .hp-metrics-row {
    grid-template-columns: 1fr !important;
    gap: 12px !important;
  }
  .hp-reserve-content {
    padding: 32px 18px !important;
  }
}

@media (max-width: 480px) {
  .hp-section { padding: 50px 14px !important; }
  .hp-hero-title {
    font-size: clamp(1.55rem, 7vw, 1.95rem) !important;
  }
  .hp-sec-title {
    font-size: clamp(1.3rem, 6vw, 1.65rem) !important;
  }
  .hp-broth-title {
    font-size: 1.15rem !important;
  }
  .hp-broth-card, .hp-special-card, .hp-reserve-content {
    padding: 18px 14px !important;
    border-radius: 14px !important;
  }
  .hp-broth-img-box, .hp-special-img-box {
    height: 180px !important;
    border-radius: 12px !important;
  }
  .hp-reserve-form-box {
    grid-template-columns: 1fr !important;
    gap: 10px !important;
  }
  .hp-select-field, .hp-date-input, .hp-time-input {
    height: 46px !important;
    font-size: 0.88rem !important;
  }
  .hp-floating-badge {
    display: none !important;
  }
  .site-footer {
    padding: 60px 14px 30px !important;
  }
}

@media (max-width: 320px) {
  .hp-section { padding: 40px 10px !important; }
  .hp-hero-title { font-size: 1.4rem !important; }
  .hp-sec-title { font-size: 1.2rem !important; }
  .hp-broth-title { font-size: 1.05rem !important; }
  p, .hp-hero-desc { font-size: 0.82rem !important; }
  .hp-cta-primary, .hp-cta-secondary {
    padding: 10px 12px !important;
    font-size: 0.82rem !important;
    min-height: 44px !important;
  }
  .hp-broth-card, .hp-special-card {
    padding: 14px 10px !important;
    border-radius: 10px !important;
  }
  .hp-broth-img-box, .hp-special-img-box {
    height: 150px !important;
  }
}
"""

CSS_MENU = CORE_BASELINE + """
/* --- MENU.HTML RESPONSIVE BREAKPOINTS --- */
@media (max-width: 1024px) {
  .mp-section { padding: 80px 24px !important; }
  .mp-meat-card { grid-column: span 6 !important; }
  .mp-grain-card.wide, .mp-grain-card.regular { grid-column: span 6 !important; }
  .mp-seafood-grid { grid-template-columns: repeat(2, 1fr) !important; gap: 20px !important; }
  .mp-sauce-palette-grid { grid-template-columns: repeat(3, 1fr) !important; }
  .mp-sim-grid { grid-template-columns: 1fr !important; }
}

@media (max-width: 768px) {
  .mp-section { padding: 65px 18px !important; }
  .mp-meat-card, .mp-grain-card.wide, .mp-grain-card.regular,
  .mp-broth-card.featured, .mp-broth-card.standard, .mp-broth-card.medium,
  .mp-wagyu-spotlight {
    grid-column: span 12 !important;
    width: 100% !important;
    margin-bottom: 16px !important;
  }
  .mp-meat-grid, .mp-broth-grid, .mp-seafood-grid, .mp-garden-columns, .mp-sim-grid {
    grid-template-columns: 1fr !important;
    gap: 18px !important;
  }
  .mp-sauce-palette-grid { grid-template-columns: repeat(2, 1fr) !important; gap: 14px !important; }
  .mp-dock-inner {
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 12px !important;
  }
  .mp-dock-filters {
    overflow-x: auto !important;
    flex-wrap: nowrap !important;
    -webkit-overflow-scrolling: touch !important;
    padding-bottom: 6px !important;
    justify-content: flex-start !important;
  }
  .mp-sec-title {
    font-size: clamp(1.5rem, 5vw, 2rem) !important;
  }
  .mp-sec-subtitle { font-size: 0.9rem !important; }
}

@media (max-width: 480px) {
  .mp-section { padding: 50px 14px !important; }
  .mp-sauce-palette-grid { grid-template-columns: 1fr !important; gap: 12px !important; }
  .mp-spice-scale { grid-template-columns: 1fr !important; gap: 10px !important; }
  .mp-meat-card, .mp-seafood-card, .mp-grain-card, .mp-broth-card, .mp-garden-group-card {
    padding: 16px 14px !important;
    border-radius: 14px !important;
  }
  .mp-meat-visual, .mp-seafood-thumb, .mp-grain-visual, .mp-broth-media {
    height: 160px !important;
    max-height: 180px !important;
    border-radius: 10px !important;
  }
  .mp-broth-footer {
    flex-wrap: wrap !important;
    gap: 8px !important;
    justify-content: space-between !important;
  }
  .mp-broth-price {
    font-size: 1.15rem !important;
  }
}

@media (max-width: 320px) {
  .mp-section { padding: 40px 10px !important; }
  .mp-sec-title { font-size: 1.25rem !important; }
  .mp-meat-title, .mp-seafood-title { font-size: 1.05rem !important; }
  p, .mp-meat-desc, .mp-seafood-desc { font-size: 0.8rem !important; }
  .mp-filter-btn {
    padding: 6px 10px !important;
    font-size: 0.78rem !important;
  }
  .mp-meat-card, .mp-seafood-card, .mp-grain-card {
    padding: 12px 10px !important;
    border-radius: 10px !important;
  }
  .mp-meat-visual, .mp-seafood-thumb, .mp-grain-visual {
    height: 140px !important;
  }
}
"""

CSS_ABOUT = CORE_BASELINE + """
/* --- ABOUT.HTML RESPONSIVE BREAKPOINTS --- */
@media (max-width: 1024px) {
  .abt-section { padding: 80px 24px !important; }
  .abt-hero-split, .abt-story-split, .abt-trad-split {
    grid-template-columns: 1fr !important;
    gap: 32px !important;
  }
  .abt-pillars-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 20px !important;
  }
  .abt-mv-grid {
    grid-template-columns: 1fr !important;
    gap: 24px !important;
  }
}

@media (max-width: 768px) {
  .abt-section { padding: 65px 18px !important; }
  .abt-pillars-grid, .abt-sourcing-grid, .abt-tradition-grid, .abt-chefs-grid {
    grid-template-columns: 1fr !important;
    gap: 18px !important;
  }
  .abt-pillar-card, .abt-sourcing-card, .abt-trad-card, .abt-chef-profile-card {
    width: 100% !important;
    margin-bottom: 16px !important;
  }
  .abt-chef-profile-card {
    flex-direction: column !important;
    align-items: center !important;
    text-align: center !important;
    padding: 24px 18px !important;
  }
  .abt-chef-img-wrapper {
    width: 100% !important;
    max-width: 260px !important;
    margin: 0 auto 16px !important;
  }
  .abt-chef-img {
    width: 100% !important;
    height: auto !important;
    max-height: 280px !important;
  }
  .abt-hero-title, .abt-sec-title {
    font-size: clamp(1.6rem, 5vw, 2.2rem) !important;
    line-height: 1.2 !important;
  }
  .abt-hero-desc, .abt-sec-desc { font-size: 0.9rem !important; }
}

@media (max-width: 480px) {
  .abt-section { padding: 50px 14px !important; }
  .abt-pillar-card, .abt-mv-panel, .abt-sourcing-card {
    padding: 18px 14px !important;
    border-radius: 14px !important;
  }
  .abt-philosophy-quote-box {
    padding: 20px 16px !important;
  }
  .abt-philosophy-quote-box blockquote {
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
  }
  .abt-action-btns {
    flex-direction: column !important;
    width: 100% !important;
  }
  .abt-experience-btn {
    width: 100% !important;
    text-align: center !important;
    justify-content: center !important;
  }
}

@media (max-width: 320px) {
  .abt-section { padding: 40px 10px !important; }
  .abt-hero-title, .abt-sec-title { font-size: 1.3rem !important; }
  .abt-pillar-card, .abt-sourcing-card {
    padding: 14px 10px !important;
    border-radius: 10px !important;
  }
  .abt-chef-img-wrapper {
    max-width: 200px !important;
  }
}
"""

CSS_CONTACT = CORE_BASELINE + """
/* --- CONTACT.HTML RESPONSIVE BREAKPOINTS --- */
@media (max-width: 1024px) {
  .cnt-section { padding: 80px 24px !important; }
  .cnt-info-grid, .cnt-hours-grid, .cnt-transport-grid, .cnt-group-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 20px !important;
  }
}

@media (max-width: 768px) {
  .cnt-section { padding: 65px 18px !important; }
  .cnt-info-grid, .cnt-hours-grid, .cnt-holiday-grid, .cnt-map-container,
  .cnt-transport-grid, .cnt-form-grid, .cnt-group-grid {
    grid-template-columns: 1fr !important;
    gap: 18px !important;
  }
  .cnt-info-card, .cnt-shift-card, .cnt-transport-card, .cnt-group-card {
    width: 100% !important;
    margin-bottom: 16px !important;
  }
  .cnt-map-iframe { height: 280px !important; }
  .cnt-form-row { grid-template-columns: 1fr !important; gap: 12px !important; }
  .cnt-submit-btn { width: 100% !important; justify-content: center !important; }
  .cnt-sec-title { font-size: clamp(1.5rem, 5vw, 2rem) !important; }
}

@media (max-width: 480px) {
  .cnt-section { padding: 50px 14px !important; }
  .cnt-info-card, .cnt-shift-card, .cnt-transport-card, .cnt-group-card {
    padding: 18px 14px !important;
    border-radius: 14px !important;
  }
  .cnt-map-iframe { height: 230px !important; }
  .cnt-input, .cnt-select, .cnt-textarea {
    width: 100% !important;
    font-size: 0.88rem !important;
  }
  .cnt-submit-btn { min-height: 48px !important; font-size: 0.9rem !important; }
}

@media (max-width: 320px) {
  .cnt-section { padding: 40px 10px !important; }
  .cnt-sec-title { font-size: 1.25rem !important; }
  .cnt-info-card, .cnt-shift-card { padding: 14px 10px !important; }
  .cnt-action-btn { padding: 8px 10px !important; font-size: 0.78rem !important; }
}
"""

CSS_EXPERIENCE = CORE_BASELINE + """
/* --- EXPERIENCE.HTML RESPONSIVE BREAKPOINTS --- */
@media (max-width: 1024px) {
  .exp-section { padding: 80px 24px !important; }
  .exp-solo-grid, .exp-corp-grid, .exp-family-grid, .exp-private-grid {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}

@media (max-width: 768px) {
  .exp-section { padding: 65px 18px !important; }
  .exp-ritual-grid, .exp-solo-grid, .exp-corp-grid, .exp-family-grid,
  .exp-private-grid, .exp-gallery-grid {
    grid-template-columns: 1fr !important;
    gap: 18px !important;
  }
  .exp-step-card, .exp-solo-card, .exp-corp-card, .exp-family-card, .exp-private-card {
    width: 100% !important;
    margin-bottom: 16px !important;
  }
  .exp-actions-row {
    flex-direction: column !important;
    width: 100% !important;
    gap: 12px !important;
  }
  .exp-btn-primary, .exp-btn-secondary {
    width: 100% !important;
    justify-content: center !important;
    text-align: center !important;
    min-height: 48px !important;
  }
  .exp-sec-title { font-size: clamp(1.5rem, 5vw, 2rem) !important; }
}

@media (max-width: 480px) {
  .exp-section { padding: 50px 14px !important; }
  .exp-step-card, .exp-solo-card, .exp-private-card {
    padding: 18px 14px !important;
    border-radius: 14px !important;
  }
  .exp-card-media { height: 180px !important; }
}

@media (max-width: 320px) {
  .exp-section { padding: 40px 10px !important; }
  .exp-sec-title { font-size: 1.25rem !important; }
  .exp-card-media { height: 150px !important; }
}
"""

CSS_GALLERY = CORE_BASELINE + """
/* --- GALLERY.HTML RESPONSIVE BREAKPOINTS --- */
@media (max-width: 1024px) {
  .gal-section { padding: 80px 24px !important; }
  .gal-broth-grid, .gal-meat-grid, .gal-seafood-grid, .gal-harvest-grid, .gal-interior-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 18px !important;
  }
}

@media (max-width: 768px) {
  .gal-section { padding: 65px 18px !important; }
  .gal-broth-grid, .gal-meat-grid, .gal-seafood-grid, .gal-harvest-grid,
  .gal-interior-grid, .gal-moments-grid {
    grid-template-columns: 1fr !important;
    gap: 16px !important;
  }
  .gal-card, .gal-item { width: 100% !important; }
  .gal-filter-bar {
    overflow-x: auto !important;
    flex-wrap: nowrap !important;
    -webkit-overflow-scrolling: touch !important;
    padding-bottom: 8px !important;
    justify-content: flex-start !important;
  }
  .gal-sec-title { font-size: clamp(1.5rem, 5vw, 2rem) !important; }
}

@media (max-width: 480px) {
  .gal-section { padding: 50px 14px !important; }
  .gal-card { padding: 14px !important; border-radius: 14px !important; }
  .gal-img-wrapper { height: 200px !important; }
}

@media (max-width: 320px) {
  .gal-section { padding: 40px 10px !important; }
  .gal-sec-title { font-size: 1.25rem !important; }
  .gal-img-wrapper { height: 165px !important; }
}
"""

CSS_OFFERS = CORE_BASELINE + """
/* --- OFFERS.HTML RESPONSIVE BREAKPOINTS --- */
@media (max-width: 1024px) {
  .ofr-section { padding: 80px 24px !important; }
  .ofr-lunch-grid, .ofr-dinner-grid, .ofr-family-grid, .ofr-vip-grid {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}

@media (max-width: 768px) {
  .ofr-section { padding: 65px 18px !important; }
  .ofr-lunch-grid, .ofr-dinner-grid, .ofr-family-grid, .ofr-vip-grid, .ofr-seasonal-grid {
    grid-template-columns: 1fr !important;
    gap: 18px !important;
  }
  .ofr-card, .ofr-lunch-card, .ofr-dinner-card, .ofr-family-card, .ofr-vip-pass {
    width: 100% !important;
    margin-bottom: 16px !important;
  }
  .ofr-actions-row {
    flex-direction: column !important;
    width: 100% !important;
    gap: 12px !important;
  }
  .ofr-btn-primary, .ofr-btn-secondary, .ofr-claim-btn {
    width: 100% !important;
    justify-content: center !important;
    text-align: center !important;
    min-height: 48px !important;
  }
  .ofr-sec-title { font-size: clamp(1.5rem, 5vw, 2rem) !important; }
}

@media (max-width: 480px) {
  .ofr-section { padding: 50px 14px !important; }
  .ofr-card, .ofr-lunch-card, .ofr-dinner-card {
    padding: 18px 14px !important;
    border-radius: 14px !important;
  }
  .ofr-price-row { flex-wrap: wrap !important; gap: 6px !important; }
  .ofr-price-tag { font-size: 1.35rem !important; }
}

@media (max-width: 320px) {
  .ofr-section { padding: 40px 10px !important; }
  .ofr-sec-title { font-size: 1.25rem !important; }
  .ofr-card, .ofr-lunch-card { padding: 14px 10px !important; }
}
"""

CSS_RESERVATION = CORE_BASELINE + """
/* --- RESERVATION.HTML RESPONSIVE BREAKPOINTS --- */
@media (max-width: 1024px) {
  .rsv-section { padding: 80px 24px !important; }
  .rsv-covenant-grid, .rsv-seating-grid, .rsv-cauldron-grid {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}

@media (max-width: 768px) {
  .rsv-section { padding: 65px 18px !important; }
  .rsv-covenant-grid, .rsv-seating-grid, .rsv-cauldron-grid, .rsv-dietary-grid,
  .rsv-booking-form-box, .rsv-schedule-grid {
    grid-template-columns: 1fr !important;
    gap: 18px !important;
  }
  .rsv-covenant-card, .rsv-seating-card, .rsv-broth-card, .rsv-dietary-card {
    width: 100% !important;
    margin-bottom: 16px !important;
  }
  .rsv-booking-actions {
    flex-direction: column !important;
    width: 100% !important;
    gap: 12px !important;
  }
  .rsv-btn-primary, .rsv-btn-secondary {
    width: 100% !important;
    justify-content: center !important;
    text-align: center !important;
    min-height: 48px !important;
  }
  .rsv-sec-title { font-size: clamp(1.5rem, 5vw, 2rem) !important; }
}

@media (max-width: 480px) {
  .rsv-section { padding: 50px 14px !important; }
  .rsv-covenant-card, .rsv-seating-card, .rsv-ticket-card {
    padding: 18px 14px !important;
    border-radius: 14px !important;
  }
  .rsv-field-input, .rsv-select {
    height: 46px !important;
    font-size: 0.88rem !important;
  }
}

@media (max-width: 320px) {
  .rsv-section { padding: 40px 10px !important; }
  .rsv-sec-title { font-size: 1.25rem !important; }
  .rsv-covenant-card { padding: 14px 10px !important; }
}
"""

CSS_HOME2 = CORE_BASELINE + """
/* --- HOME-2.HTML RESPONSIVE BREAKPOINTS --- */
@media (max-width: 1024px) {
  .home2-section, section { padding: 80px 24px !important; }
  .home2-spectrum-grid, .home2-craft-grid { grid-template-columns: repeat(2, 1fr) !important; }
}

@media (max-width: 768px) {
  .home2-section, section { padding: 65px 18px !important; }
  .home2-spectrum-grid, .home2-craft-grid, .home2-ops-grid {
    grid-template-columns: 1fr !important;
    gap: 18px !important;
  }
  .home2-assembly-card, .home2-pillar-card { width: 100% !important; }
  .home2-hero-title { font-size: clamp(1.85rem, 5.5vw, 2.4rem) !important; }
}

@media (max-width: 480px) {
  .home2-section, section { padding: 50px 14px !important; }
  .home2-assembly-card, .home2-pillar-card { padding: 18px 14px !important; }
}

@media (max-width: 320px) {
  .home2-section, section { padding: 40px 10px !important; }
  .home2-hero-title { font-size: 1.4rem !important; }
}
"""

CSS_DASHBOARDS = CORE_BASELINE + """
/* --- DASHBOARD RESPONSIVE BREAKPOINTS --- */
@media (max-width: 1024px) {
  .kpi-cards-grid { grid-template-columns: repeat(2, 1fr) !important; gap: 16px !important; }
  .grid-4col { grid-template-columns: repeat(2, 1fr) !important; gap: 16px !important; }
  .op-metrics-grid { grid-template-columns: repeat(2, 1fr) !important; gap: 14px !important; }
  .admin-main, .dashboard-main { padding: 24px 20px !important; }
}

@media (max-width: 768px) {
  .admin-sidebar, .dashboard-sidebar {
    position: fixed !important;
    top: 0 !important;
    bottom: 0 !important;
    left: 0 !important;
    width: 280px !important;
    max-width: 85vw !important;
    z-index: 9999 !important;
    transform: translateX(-100%);
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
  }
  .admin-sidebar.mobile-open, .dashboard-sidebar.mobile-open {
    transform: translateX(0) !important;
  }
  [dir="rtl"] .admin-sidebar, [dir="rtl"] .dashboard-sidebar {
    left: auto !important;
    right: 0 !important;
    transform: translateX(100%);
  }
  [dir="rtl"] .admin-sidebar.mobile-open, [dir="rtl"] .dashboard-sidebar.mobile-open {
    transform: translateX(0) !important;
  }
  .admin-main, .dashboard-main {
    margin-left: 0 !important;
    margin-right: 0 !important;
    width: 100% !important;
    padding: 20px 14px !important;
  }
  .kpi-cards-grid, .grid-4col, .grid-3col, .grid-2col, .op-metrics-grid {
    grid-template-columns: 1fr !important;
    gap: 14px !important;
  }
  .admin-topbar, .dashboard-topbar {
    padding: 0 14px !important;
    height: 60px !important;
  }
  .topbar-search-box {
    display: none !important;
  }
  .topbar-user-badge span:not(.user-avatar) {
    display: none !important;
  }
  .card-title-row {
    flex-wrap: wrap !important;
    gap: 10px !important;
  }
  .card-actions-row {
    width: 100% !important;
    flex-wrap: wrap !important;
  }
  .data-table-container, .table-wrapper {
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
    width: 100% !important;
    display: block !important;
  }
  .modal-dialog {
    max-width: calc(100% - 24px) !important;
    width: 100% !important;
    margin: 16px auto !important;
    padding: 20px 16px !important;
  }
}

@media (max-width: 480px) {
  .admin-main, .dashboard-main { padding: 14px 10px !important; }
  .content-card {
    padding: 16px 12px !important;
    border-radius: 14px !important;
    margin-bottom: 14px !important;
  }
  .kpi-card { padding: 14px 12px !important; }
  .kpi-val { font-size: 1.5rem !important; }
  .btn-action-primary, .btn-secondary {
    width: 100% !important;
    justify-content: center !important;
    text-align: center !important;
    height: 44px !important;
  }
  .filter-tabs-row {
    overflow-x: auto !important;
    flex-wrap: nowrap !important;
    -webkit-overflow-scrolling: touch !important;
  }
}

@media (max-width: 320px) {
  .admin-main, .dashboard-main { padding: 10px 6px !important; }
  .content-card { padding: 12px 8px !important; border-radius: 10px !important; }
  .admin-topbar, .dashboard-topbar { padding: 0 8px !important; }
  .brand-title { font-size: 1rem !important; }
  .card-title { font-size: 1.05rem !important; }
}
"""

CSS_LOGIN = CORE_BASELINE + """
/* --- LOGIN.HTML RESPONSIVE BREAKPOINTS --- */
@media (max-width: 1024px) {
  .login-main { padding: 40px 20px; }
}

@media (max-width: 768px) {
  .login-main { padding: 30px 16px; }
  .login-card { max-width: 100%; width: 100%; }
}

@media (max-width: 480px) {
  .login-main { padding: 20px 12px; min-height: 100vh; }
  .login-card { padding: 20px 16px 18px; border-radius: 16px; width: 100%; max-width: 100%; }
  .card-title { font-size: 1.4rem; }
  .card-subtitle { font-size: 0.85rem; }
  .social-auth-grid { gap: 8px; }
  .social-auth-btn { height: 42px; font-size: 0.82rem; padding: 0 8px; }
  .remember-forgot-row { flex-wrap: wrap; gap: 8px; }
  .btn-3d-submit { height: 46px; font-size: 0.92rem; width: 100%; }
}

@media (max-width: 320px) {
  .login-main { padding: 12px 8px; }
  .login-card { padding: 16px 10px 14px; border-radius: 12px; }
  .card-title { font-size: 1.25rem; }
  .brand-title { font-size: 1.15rem; }
  .social-auth-grid { grid-template-columns: 1fr; gap: 6px; }
  .social-auth-btn { height: 38px; font-size: 0.8rem; width: 100%; }
  .input-wrapper input { font-size: 0.85rem; padding: 10px 12px 10px 36px; }
  .btn-3d-submit { height: 44px; font-size: 0.88rem; }
  .top-actions-bar { top: 8px; left: 8px; gap: 6px; }
  [dir="rtl"] .top-actions-bar { left: auto; right: 8px; }
  .action-icon-btn { width: 34px; height: 34px; }
}
"""

CSS_REGISTERATION = CORE_BASELINE + """
/* --- REGISTERATION.HTML RESPONSIVE BREAKPOINTS --- */
@media (max-width: 1024px) {
  .login-main { padding: 40px 24px; }
}

@media (max-width: 768px) {
  .login-main { padding: 30px 16px; }
  .register-card { max-width: 100%; width: 100%; padding: 26px 20px; }
  .form-grid-row { grid-template-columns: 1fr; gap: 14px; }
  .card-title { font-size: 1.7rem; }
}

@media (max-width: 480px) {
  .login-main { padding: 20px 12px; }
  .register-card { padding: 20px 14px 18px; border-radius: 16px; }
  .card-title { font-size: 1.45rem; }
  .card-subtitle { font-size: 0.85rem; }
  .strength-meter-bar { gap: 4px; }
  .social-auth-grid { grid-template-columns: 1fr; gap: 8px; }
  .login-header { padding: 12px 14px; }
  .back-btn span { font-size: 0.82rem; }
  .back-btn { padding: 6px 10px; font-size: 0.8rem; }
  .btn-3d-submit { height: 46px; font-size: 0.92rem; width: 100%; }
}

@media (max-width: 320px) {
  .login-main { padding: 10px 6px; }
  .register-card { padding: 16px 10px 14px; border-radius: 12px; }
  .card-title { font-size: 1.25rem; }
  .brand-title { font-size: 1.15rem; }
  .form-label { font-size: 0.78rem; }
  .input-wrapper input, .input-wrapper select { font-size: 0.82rem; padding: 10px 10px 10px 34px; }
  .btn-3d-submit { height: 44px; font-size: 0.88rem; width: 100%; }
  .login-header { padding: 8px 10px; }
  .back-btn span { display: none; }
  .action-icon-btn { width: 34px; height: 34px; }
}
"""

CSS_404 = CORE_BASELINE + """
/* --- 404.HTML RESPONSIVE BREAKPOINTS --- */
@media (max-width: 1024px) {
  .error-card { max-width: 100%; width: 680px; }
}

@media (max-width: 768px) {
  .error-card { max-width: 100%; width: 100%; padding: 30px 22px; }
  .error-404-glitch { font-size: clamp(4rem, 14vw, 6rem); }
  .error-title { font-size: clamp(1.6rem, 5vw, 2.1rem); }
  .error-desc { font-size: 0.92rem; }
}

@media (max-width: 480px) {
  .error-main { padding: 20px 12px; }
  .error-card { padding: 22px 14px 20px; border-radius: 16px; }
  .error-404-glitch { font-size: clamp(3rem, 16vw, 4.5rem); }
  .cauldron-center-icon { width: 56px; height: 56px; margin: -6px auto 10px; }
  .error-title { font-size: 1.45rem; }
  .error-desc { font-size: 0.85rem; line-height: 1.5; }
  .quick-search-box { margin-bottom: 16px; }
  .search-input { height: 44px; font-size: 0.85rem; padding: 0 38px 0 38px; }
  .nav-pills-row { gap: 6px; }
  .nav-pill-chip { padding: 6px 10px; font-size: 0.78rem; }
  .error-actions-row { grid-template-columns: 1fr; gap: 10px; }
  .btn-3d-home, .btn-outline-menu { height: 46px; font-size: 0.88rem; width: 100%; }
  .error-header { padding: 12px 14px; }
}

@media (max-width: 320px) {
  .error-main { padding: 10px 6px; }
  .error-card { padding: 16px 10px 14px; border-radius: 12px; }
  .error-404-glitch { font-size: 2.8rem; }
  .cauldron-center-icon { width: 48px; height: 48px; }
  .error-title { font-size: 1.25rem; }
  .error-desc { font-size: 0.8rem; }
  .search-input { height: 40px; font-size: 0.8rem; }
  .nav-pill-chip { font-size: 0.74rem; padding: 5px 8px; }
  .error-header { padding: 8px 10px; }
  .back-btn span { display: none; }
  .action-icon-btn { width: 32px; height: 32px; }
}
"""

# Map files to their specific responsive configs
files_map = {
    'index.html': CSS_INDEX,
    'navbar.html': CSS_INDEX,
    'menu.html': CSS_MENU,
    'about.html': CSS_ABOUT,
    'contact.html': CSS_CONTACT,
    'experience.html': CSS_EXPERIENCE,
    'gallery.html': CSS_GALLERY,
    'offers.html': CSS_OFFERS,
    'reservation.html': CSS_RESERVATION,
    'reservations.html': CSS_RESERVATION,
    'home-2.html': CSS_HOME2,
    'admin-dashboard.html': CSS_DASHBOARDS,
    'user-dashboard.html': CSS_DASHBOARDS,
    'login.html': CSS_LOGIN,
    'registeration.html': CSS_REGISTERATION,
    '404.html': CSS_404
}

for fname, css in files_map.items():
    if os.path.exists(fname):
        inject_or_replace_responsive(fname, css)
    else:
        print(f"Skipping {fname}: file does not exist.")

print("\n--- ALL RESPONSIVE SYSTEM INJECTIONS COMPLETED ---")

import math
from PIL import Image, ImageDraw

def create_favicon(size=128):
    # Create RGBA image with anti-aliasing supersampling (4x)
    scale = 4
    w = size * scale
    h = size * scale
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = (w / 2, h / 2)
    radius = w * 0.46

    # Draw circular dark background
    draw.ellipse(
        [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
        fill=(22, 9, 7, 255),
        outline=(212, 172, 13, 255),
        width=int(2.5 * scale)
    )

    # Inner dashed/subtle ring
    inner_rad = radius * 0.92
    draw.ellipse(
        [center[0] - inner_rad, center[1] - inner_rad, center[0] + inner_rad, center[1] + inner_rad],
        fill=None,
        outline=(245, 176, 65, 120),
        width=int(1 * scale)
    )

    # Pot dimensions
    pot_w = w * 0.58
    pot_h = h * 0.32
    pot_top = h * 0.52
    pot_center_x = w / 2

    # Pot Outer Body (cauldron bottom)
    body_bbox = [pot_center_x - pot_w/2, pot_top, pot_center_x + pot_w/2, pot_top + pot_h]
    draw.pieslice(body_bbox, start=0, end=180, fill=(60, 16, 12, 255), outline=(212, 172, 13, 255), width=int(2 * scale))

    # Handles
    handle_w = w * 0.08
    handle_h = h * 0.12
    # Left handle
    draw.arc([pot_center_x - pot_w/2 - handle_w*0.8, pot_top + pot_h*0.1, pot_center_x - pot_w/2 + handle_w*0.2, pot_top + pot_h*0.1 + handle_h],
             start=90, end=270, fill=(245, 176, 65, 255), width=int(2.8 * scale))
    # Right handle
    draw.arc([pot_center_x + pot_w/2 - handle_w*0.2, pot_top + pot_h*0.1, pot_center_x + pot_w/2 + handle_w*0.8, pot_top + pot_h*0.1 + handle_h],
             start=270, end=90, fill=(245, 176, 65, 255), width=int(2.8 * scale))

    # Yin-Yang dual broth rim (ellipse)
    rim_w = pot_w
    rim_h = h * 0.22
    rim_bbox = [pot_center_x - rim_w/2, pot_top - rim_h/2, pot_center_x + rim_w/2, pot_top + rim_h/2]
    draw.ellipse(rim_bbox, fill=(28, 10, 8, 255), outline=(245, 176, 65, 255), width=int(2.5 * scale))

    # Broth halves
    # Left broth: Spicy Sichuan Red
    draw.pieslice(rim_bbox, start=90, end=270, fill=(192, 57, 43, 255))
    # Right broth: Golden Herbal
    draw.pieslice(rim_bbox, start=270, end=90, fill=(243, 156, 18, 255))

    # Yin-Yang Divider line
    div_y_top = pot_top - rim_h/2
    div_y_bot = pot_top + rim_h/2
    draw.line([(pot_center_x, div_y_top), (pot_center_x, div_y_bot)], fill=(255, 248, 231, 240), width=int(2 * scale))

    # Broth accents / bubbles
    draw.ellipse([pot_center_x - rim_w*0.25, pot_top - scale*2, pot_center_x - rim_w*0.25 + scale*4, pot_top + scale*2], fill=(255, 87, 34, 255))
    draw.ellipse([pot_center_x - rim_w*0.15, pot_top + scale*3, pot_center_x - rim_w*0.15 + scale*3, pot_top + scale*6], fill=(255, 160, 0, 255))
    draw.ellipse([pot_center_x + rim_w*0.2, pot_top - scale*2, pot_center_x + rim_w*0.2 + scale*4, pot_top + scale*2], fill=(255, 224, 130, 255))
    draw.ellipse([pot_center_x + rim_w*0.1, pot_top + scale*3, pot_center_x + rim_w*0.1 + scale*3, pot_top + scale*6], fill=(192, 57, 43, 255))

    # Steam wisps rising above
    steam_color = (255, 243, 224, 200)
    for offset_x in [-w*0.14, 0, w*0.14]:
        sx = pot_center_x + offset_x
        draw.arc([sx - scale*6, pot_top - rim_h - scale*18, sx + scale*6, pot_top - rim_h],
                 start=180, end=0, fill=steam_color, width=int(2.2 * scale))

    # Downscale for crisp anti-aliasing
    final_img = img.resize((size, size), Image.Resampling.LANCZOS)
    return final_img

# Generate 128x128 PNG
fav128 = create_favicon(128)
fav128.save("images/favicon.png", "PNG")

# Generate multi-size ICO
ico_sizes = [16, 32, 48, 64]
ico_images = [create_favicon(s) for s in ico_sizes]
ico_images[0].save("favicon.ico", format="ICO", sizes=[(s, s) for s in ico_sizes], append_images=ico_images[1:])
ico_images[0].save("images/favicon.ico", format="ICO", sizes=[(s, s) for s in ico_sizes], append_images=ico_images[1:])

print("Favicon files successfully generated:")
print(" - images/favicon.svg")
print(" - images/favicon.png")
print(" - favicon.ico")
print(" - images/favicon.ico")

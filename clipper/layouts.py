import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from .config import CANVAS_WIDTH, CANVAS_HEIGHT, DEFAULT_FONT

def create_banner_and_sticker_template(
    out_path: str,
    top_title: str = None,
    sticker_path: str = None,
    sticker_pos: tuple = (405, 160, 270, 270),
    main_border_box: tuple = (140, 450, 800, 600),
    sec_border_box: tuple = (305, 1065, 470, 510)
) -> str:
    """
    Generate an RGBA overlay template containing top banner, rounded sticker,
    and frame borders with 100% transparent cutouts for live video streams.
    """
    overlay = Image.new('RGBA', (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 1. Top Banner
    if top_title:
        try:
            font_title = ImageFont.truetype(f"{DEFAULT_FONT}.ttf", 74)
        except:
            font_title = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), top_title, font=font_title)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        pill_w = tw + 80
        pill_h = th + 36
        px1 = (CANVAS_WIDTH - pill_w) // 2
        py1 = 55
        px2 = px1 + pill_w
        py2 = py1 + pill_h

        draw.rounded_rectangle([px1 + 4, py1 + 6, px2 + 4, py2 + 6], radius=24, fill=(0, 0, 0, 160))
        draw.rounded_rectangle([px1, py1, px2, py2], radius=24, fill=(225, 25, 35, 255), outline=(255, 255, 255, 255), width=5)
        tx = (CANVAS_WIDTH - tw) // 2
        ty = py1 + (pill_h - th) // 2 - 4
        draw.text((tx + 3, ty + 3), top_title, font=font_title, fill=(0, 0, 0, 200))
        draw.text((tx, ty), top_title, font=font_title, fill=(255, 255, 255, 255))

    # 2. Sticker
    if sticker_path and os.path.exists(sticker_path):
        sx, sy, sw, sh = sticker_pos
        sticker = Image.open(sticker_path).convert("RGBA")
        sticker = sticker.resize((sw, sh), Image.Resampling.LANCZOS)
        
        # Shadow
        shadow = Image.new('RGBA', (sw + 20, sh + 20), (0, 0, 0, 0))
        draw_s = ImageDraw.Draw(shadow)
        draw_s.rounded_rectangle([(6, 8), (sw + 14, sh + 16)], radius=40, fill=(0, 0, 0, 150))
        overlay.paste(shadow, (sx - 10, sy - 6), mask=shadow)
        overlay.paste(sticker, (sx, sy), mask=sticker)

    # 3. Main Video Border (e.g. Valorant Cards)
    if main_border_box:
        mx, my, mw, mh = main_border_box
        draw.rounded_rectangle([mx - 3, my - 3, mx + mw + 3, my + mh + 3],
                               radius=18, outline=(255, 255, 255, 220), width=6)

    # 4. Secondary Video Border (e.g. Discord Voice Chat)
    if sec_border_box:
        bx, by, bw, bh = sec_border_box
        draw.rounded_rectangle([bx - 3, by - 3, bx + bw + 3, by + bh + 3],
                               radius=20, outline=(88, 101, 242, 255), width=6)

    overlay.save(out_path)
    return out_path

def create_discord_game_template(
    out_path: str,
    game_box: tuple = (60, 130, 960, 540),
    discord_box: tuple = (305, 695, 470, 506)
) -> str:
    """
    Generate an overlay template for a dual-stream layout:
    - Main game frame on top (with rounded white border)
    - Discord voice overlay card in center (with Discord blurple border)
    """
    overlay = Image.new('RGBA', (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Main game border
    gx, gy, gw, gh = game_box
    draw.rounded_rectangle([gx - 3, gy - 3, gx + gw + 3, gy + gh + 3],
                           radius=18, outline=(255, 255, 255, 220), width=6)

    # Discord card border
    dx, dy, dw, dh = discord_box
    draw.rounded_rectangle([dx - 3, dy - 3, dx + dw + 3, dy + dh + 3],
                           radius=20, outline=(88, 101, 242, 255), width=6)

    overlay.save(out_path)
    return out_path


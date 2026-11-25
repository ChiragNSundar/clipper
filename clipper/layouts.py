import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from .config import CANVAS_WIDTH, CANVAS_HEIGHT, DEFAULT_FONT

def create_banner_and_sticker_template(
    out_path: str,
    top_title: str = None,
    sticker_path: str = None,
    sticker_pos: tuple = None,
    main_border_box: tuple = None,
    sec_border_box: tuple = None
) -> str:
    """
    Generate an RGBA overlay template containing top banner, rounded sticker,
    and optional frame borders with 100% transparent cutouts for live video streams.
    """
    overlay = Image.new('RGBA', (CANVAS_WIDTH, CANVAS_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    py2 = 0
    # 1. Top Banner
    if top_title:
        font_candidates = [
            r"C:\Windows\Fonts\impact.ttf",
            "impact.ttf",
            f"{DEFAULT_FONT}.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
            "arialbd.ttf"
        ]
        font_title = None
        for fpath in font_candidates:
            try:
                font_title = ImageFont.truetype(fpath, 95)
                break
            except Exception:
                continue

        if not font_title:
            font_title = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), top_title, font=font_title)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        pill_w = tw + 140
        pill_h = th + 50
        px1 = (CANVAS_WIDTH - pill_w) // 2
        py1 = 60
        px2 = px1 + pill_w
        py2 = py1 + pill_h

        # Drop shadow behind banner
        draw.rounded_rectangle([px1 + 5, py1 + 8, px2 + 5, py2 + 8], radius=35, fill=(0, 0, 0, 180))
        # Vibrant red pill with solid white outline
        draw.rounded_rectangle([px1, py1, px2, py2], radius=35, fill=(230, 30, 40, 255), outline=(255, 255, 255, 255), width=8)
        tx = (CANVAS_WIDTH - tw) // 2
        ty = py1 + (pill_h - th) // 2 - 6
        draw.text((tx + 4, ty + 4), top_title, font=font_title, fill=(0, 0, 0, 220))
        draw.text((tx, ty), top_title, font=font_title, fill=(255, 255, 255, 255))

    # 2. Sticker
    if sticker_path and os.path.exists(sticker_path):
        if sticker_pos is None:
            sw, sh = 420, 420
            sx = (CANVAS_WIDTH - sw) // 2
            sy = (py2 + 25) if top_title else 120
            sticker_pos = (sx, sy, sw, sh)
        else:
            sx, sy, sw, sh = sticker_pos

        sticker = Image.open(sticker_path).convert("RGBA")
        sticker = sticker.resize((sw, sh), Image.Resampling.LANCZOS)
        
        # Rounded corners mask
        mask = Image.new('L', (sw, sh), 0)
        draw_m = ImageDraw.Draw(mask)
        draw_m.rounded_rectangle([(0, 0), (sw, sh)], radius=45, fill=255)

        # Soft drop shadow
        shadow = Image.new('RGBA', (sw + 30, sh + 30), (0, 0, 0, 0))
        draw_s = ImageDraw.Draw(shadow)
        draw_s.rounded_rectangle([(10, 15), (sw + 20, sh + 25)], radius=50, fill=(0, 0, 0, 190))
        overlay.paste(shadow, (sx - 10, sy - 10), mask=shadow)
        
        # Rounded sticker
        overlay.paste(sticker, (sx, sy), mask=mask)

        # White border around sticker card
        draw.rounded_rectangle([sx - 3, sy - 3, sx + sw + 3, sy + sh + 3], radius=48, outline=(255, 255, 255, 240), width=7)

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


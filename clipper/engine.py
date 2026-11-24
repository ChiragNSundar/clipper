import os
import sys
import json
import subprocess
from .config import FFMPEG, FFPROBE, CANVAS_WIDTH, CANVAS_HEIGHT
from .layouts import create_banner_and_sticker_template
from .subtitles import build_ass_script

def probe_video(video_path: str) -> dict:
    """Probe video file and return stream details."""
    cmd = [
        FFPROBE, "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        video_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(res.stdout)
    v_stream = next(s for s in data["streams"] if s["codec_type"] == "video")
    a_stream = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    return {
        "duration": float(data["format"].get("duration", 0)),
        "width": int(v_stream["width"]),
        "height": int(v_stream["height"]),
        "has_audio": a_stream is not None,
        "size_bytes": int(data["format"].get("size", 0))
    }

def render_reel(
    input_video: str,
    output_video: str,
    layout: str = "center",
    ass_subtitle_path: str = None,
    start_time: float = None,
    duration: float = None,
    # For split / multi-crop layout:
    main_crop: str = "640:480:320:160",
    main_scale: str = "800:600",
    main_pos: tuple = (140, 450),
    sec_crop: str = "230:250:0:15",
    sec_scale: str = "440:480",
    sec_pos: tuple = (320, 1080),
    sec_bg_box: tuple = (305, 1065, 470, 510),
    top_header: str = None,
    sticker_path: str = None,
    crf: int = 20,
    preset: str = "veryfast",
    timeout_sec: int = 180
) -> str:
    """
    Universally render an Instagram / TikTok 9:16 Reel.
    Guarantees no stuck renders via -shortest, bounded drawbox, and timeout.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_video)), exist_ok=True)
    if os.path.exists(output_video):
        try:
            os.remove(output_video)
        except:
            pass

    # Build input args
    input_args = []
    if start_time is not None:
        input_args.extend(["-ss", str(start_time)])
    if duration is not None:
        input_args.extend(["-t", str(duration)])
    input_args.extend(["-i", input_video])

    # Windows safe path for subtitles in filtergraph
    safe_ass = ""
    if ass_subtitle_path and os.path.exists(ass_subtitle_path):
        safe_ass = os.path.abspath(ass_subtitle_path).replace("\\", "/").replace(":", "\\:")

    filter_complex = ""
    extra_inputs = []

    if layout == "center":
        # Direct 9:16 center crop
        vf = f"crop=ih*9/16:ih:(iw-ow)/2:0,scale={CANVAS_WIDTH}:{CANVAS_HEIGHT}:flags=lanczos,setsar=1"
        if safe_ass:
            vf += f",subtitles='{safe_ass}'"
        cmd = [
            FFMPEG, "-y",
            *input_args,
            "-vf", vf,
            "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            output_video
        ]

    elif layout == "ambient":
        # Blurred background + centered 16:9 feed
        fc = (
            f"[0:v]scale={CANVAS_WIDTH}:{CANVAS_HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={CANVAS_WIDTH}:{CANVAS_HEIGHT},boxblur=20:4,eq=brightness=-0.1:contrast=1.05[bg];"
            f"[0:v]scale={CANVAS_WIDTH}:-1[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2[v_comp]"
        )
        if safe_ass:
            fc += f";[v_comp]subtitles='{safe_ass}'[v_out]"
            map_v = "[v_out]"
        else:
            map_v = "[v_comp]"

        cmd = [
            FFMPEG, "-y",
            *input_args,
            "-filter_complex", fc,
            "-map", map_v, "-map", "0:a",
            "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            output_video
        ]

    elif layout == "split":
        # Multi-crop layout (e.g. Valorant cards + Discord overlay + Header + Sticker)
        template_png = os.path.join(os.path.dirname(output_video), "temp_overlay_template.png")
        create_banner_and_sticker_template(
            out_path=template_png,
            top_title=top_header,
            sticker_path=sticker_path,
            main_border_box=(main_pos[0], main_pos[1], int(main_scale.split(':')[0]), int(main_scale.split(':')[1])),
            sec_border_box=sec_bg_box
        )
        extra_inputs = ["-loop", "1", "-i", template_png]

        # Note: drawbox directly draws solid background without infinite color stream!
        fc_parts = [
            f"[0:v]scale={CANVAS_WIDTH}:{CANVAS_HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={CANVAS_WIDTH}:{CANVAS_HEIGHT},boxblur=20:4,eq=brightness=-0.1:contrast=1.05[bg];",
            f"[0:v]crop={main_crop},scale={main_scale}[main];",
            f"[0:v]crop={sec_crop},scale={sec_scale}[sec];",
            f"[bg][main]overlay={main_pos[0]}:{main_pos[1]}[tmp1];",
            f"[tmp1]drawbox=x={sec_bg_box[0]}:y={sec_bg_box[1]}:w={sec_bg_box[2]}:h={sec_bg_box[3]}:color=0x2B2D31@1.0:t=fill[tmp_box];",
            f"[tmp_box][sec]overlay={sec_pos[0]}:{sec_pos[1]}[tmp2];",
            f"[tmp2][1:v]overlay=0:0:shortest=1[v_comp]"
        ]
        if safe_ass:
            fc_parts.append(f";[v_comp]subtitles='{safe_ass}'[v_out]")
            map_v = "[v_out]"
        else:
            map_v = "[v_comp]"

        fc = "".join(fc_parts)
        cmd = [
            FFMPEG, "-y",
            *input_args,
            *extra_inputs,
            "-filter_complex", fc,
            "-map", map_v, "-map", "0:a",
            "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            "-movflags", "+faststart",
            output_video
        ]

    else:
        raise ValueError(f"Unknown layout: {layout}")

    print(f"[Clipper] Executing FFmpeg ({layout} mode)...")
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_sec)
    if res.returncode != 0:
        print(f"[Clipper Error] FFmpeg failed:\n{res.stderr}")
        raise RuntimeError(f"FFmpeg error: {res.stderr}")

    # Clean intermediate template if created
    if layout == "split" and os.path.exists(template_png):
        try:
            os.remove(template_png)
        except:
            pass

    size_mb = os.path.getsize(output_video) / (1024 * 1024)
    print(f"[Clipper Success] Generated {output_video} ({size_mb:.2f} MB)")
    return output_video

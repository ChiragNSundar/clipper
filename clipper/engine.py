import os
import sys
import json
import tempfile
import subprocess
from .config import FFMPEG, FFPROBE, CANVAS_WIDTH, CANVAS_HEIGHT, GYAN_FFMPEG_DIR, resolve_sticker_path
from .layouts import create_banner_and_sticker_template, create_discord_game_template
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

def download_youtube_section(url: str, start_time: float, duration: float, out_path: str) -> str:
    """
    Directly download only the required section from a YouTube stream via yt-dlp.
    Avoids downloading entire multi-gigabyte vods.
    """
    end_time = start_time + duration
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--ffmpeg-location", GYAN_FFMPEG_DIR,
        "--download-sections", f"*{start_time}-{end_time}",
        "-f", "bv*[height<=1080]+ba/b",
        "--merge-output-format", "mp4",
        "-o", out_path,
        url
    ]
    print(f"[Clipper] Downloading stream section {start_time}s to {end_time}s from {url}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"yt-dlp download failed: {res.stderr}")
    return out_path

def concat_segments(segment_files: list, out_path: str) -> str:
    """Concatenate multiple video files seamlessly using FFmpeg filter complex."""
    inputs = []
    fc_parts = []
    for i, seg in enumerate(segment_files):
        inputs.extend(["-i", seg])
        fc_parts.append(f"[{i}:v][{i}:a]")
    fc = "".join(fc_parts) + f"concat=n={len(segment_files)}:v=1:a=1[v][a]"
    cmd = [
        FFMPEG, "-y",
        *inputs,
        "-filter_complex", fc,
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        out_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path

def render_reel(
    input_video: str,
    output_video: str,
    layout: str = "center",
    ass_subtitle_path: str = None,
    start_time: float = None,
    duration: float = None,
    segments: list = None,
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
    sticker_time: tuple = None,  # (start_t, end_t) for dynamic popping stickers
    sticker_pos_y: int = 420,
    crf: int = 20,
    preset: str = "veryfast",
    timeout_sec: int = 180
) -> str:
    """
    Universally render an Instagram / TikTok 9:16 Reel.
    Guarantees mobile playback compatibility via setsar=1, flags=lanczos, pix_fmt yuv420p,
    and hang prevention via -shortest and bounded drawbox.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_video)), exist_ok=True)
    if os.path.exists(output_video):
        try:
            os.remove(output_video)
        except:
            pass

    with tempfile.TemporaryDirectory() as temp_dir:
        source_to_use = input_video
        sticker_path = resolve_sticker_path(sticker_path)

        # Check if input is a YouTube URL
        is_url = input_video.startswith("http://") or input_video.startswith("https://")
        if is_url:
            temp_dl = os.path.join(temp_dir, "temp_ytdlp_cut.mp4")
            st = start_time or 0.0
            dur = duration or 30.0
            download_youtube_section(input_video, st, dur, temp_dl)
            source_to_use = temp_dl
            start_time, duration = None, None

        # Handle multi-segment cuts (e.g. combine 0:23-0:35 and 0:56-1:19 into 1 reel)
        if segments and len(segments) > 1:
            seg_files = []
            for idx, (s_start, s_dur) in enumerate(segments):
                seg_path = os.path.join(temp_dir, f"temp_seg_{idx}.mp4")
                cmd_cut = [
                    FFMPEG, "-y",
                    "-ss", str(s_start), "-t", str(s_dur),
                    "-i", source_to_use,
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-c:a", "aac", "-b:a", "192k",
                    seg_path
                ]
                subprocess.run(cmd_cut, check=True, capture_output=True)
                seg_files.append(seg_path)

            temp_concat = os.path.join(temp_dir, "temp_combined.mp4")
            concat_segments(seg_files, temp_concat)
            source_to_use = temp_concat
            start_time, duration = None, None

        # Build input args
        input_args = []
        if start_time is not None:
            input_args.extend(["-ss", str(start_time)])
        if duration is not None:
            input_args.extend(["-t", str(duration)])
        input_args.extend(["-i", source_to_use])

        # Windows safe path for subtitles in filtergraph
        safe_ass = ""
        if ass_subtitle_path and os.path.exists(ass_subtitle_path):
            safe_ass = os.path.abspath(ass_subtitle_path).replace("\\", "/").replace(":", "\\:")

        extra_inputs = []

        if layout == "center":
            # Direct 9:16 center crop with lanczos and setsar=1
            if sticker_path and os.path.exists(sticker_path) and sticker_time:
                # Dynamic popping sticker (like make_reels.py Bonnie/Mustang)
                extra_inputs = ["-i", sticker_path]
                o_start, o_end = sticker_time
                fc = (
                    f"[0:v]crop=ih*9/16:ih:(iw-ow)/2:0,scale={CANVAS_WIDTH}:{CANVAS_HEIGHT}:flags=lanczos,setsar=1[bg];"
                    f"[bg][1:v]overlay=(W-w)/2:{sticker_pos_y}:enable='between(t,{o_start},{o_end})'[v_comp]"
                )
                if safe_ass:
                    fc += f";[v_comp]subtitles='{safe_ass}'[v_out]"
                    map_v = "[v_out]"
                else:
                    map_v = "[v_comp]"
                cmd = [
                    FFMPEG, "-y",
                    *input_args,
                    *extra_inputs,
                    "-filter_complex", fc,
                    "-map", map_v, "-map", "0:a",
                    "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
                    "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart",
                    output_video
                ]
            else:
                vf = f"crop=ih*9/16:ih:(iw-ow)/2:0,scale={CANVAS_WIDTH}:{CANVAS_HEIGHT}:flags=lanczos,setsar=1"
                if safe_ass:
                    vf += f",subtitles='{safe_ass}'"
                cmd = [
                    FFMPEG, "-y",
                    *input_args,
                    "-vf", vf,
                    "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
                    "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart",
                    output_video
                ]

        elif layout == "ambient":
            # Blurred background + centered 16:9 feed with lanczos
            fc = (
                f"[0:v]scale={CANVAS_WIDTH}:{CANVAS_HEIGHT}:force_original_aspect_ratio=increase,"
                f"crop={CANVAS_WIDTH}:{CANVAS_HEIGHT},boxblur=20:4,eq=brightness=-0.1:contrast=1.05,setsar=1[bg];"
                f"[0:v]scale={CANVAS_WIDTH}:-1:flags=lanczos,setsar=1[fg];"
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
                "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart",
                output_video
            ]

        elif layout == "split":
            # Multi-crop layout (e.g. Valorant cards + Discord overlay + Header + Sticker)
            template_png = os.path.join(temp_dir, "temp_overlay_template.png")
            create_banner_and_sticker_template(
                out_path=template_png,
                top_title=top_header,
                sticker_path=sticker_path if not sticker_time else None,
                main_border_box=(main_pos[0], main_pos[1], int(main_scale.split(':')[0]), int(main_scale.split(':')[1])),
                sec_border_box=sec_bg_box
            )
            extra_inputs = ["-loop", "1", "-i", template_png]

            # Note: drawbox directly draws solid background without infinite color stream!
            fc_parts = [
                f"[0:v]scale={CANVAS_WIDTH}:{CANVAS_HEIGHT}:force_original_aspect_ratio=increase,"
                f"crop={CANVAS_WIDTH}:{CANVAS_HEIGHT},boxblur=20:4,eq=brightness=-0.1:contrast=1.05,setsar=1[bg];",
                f"[0:v]crop={main_crop},scale={main_scale}:flags=lanczos,setsar=1[main];",
                f"[0:v]crop={sec_crop},scale={sec_scale}:flags=lanczos,setsar=1[sec];",
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
                "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k",
                "-shortest",
                "-movflags", "+faststart",
                output_video
            ]

        elif layout in ("discord_game", "discord_split"):
            # Dual layout: Main gameplay on top, Discord voice card in center
            template_png = os.path.join(temp_dir, "temp_discord_game_template.png")
            g_crop = main_crop if main_crop != "640:480:320:160" else "1920:1080:0:60"
            g_scale = main_scale if main_scale != "800:600" else "960:540"
            g_pos = main_pos if main_pos != (140, 450) else (60, 130)

            d_crop = sec_crop if sec_crop != "230:250:0:15" else "360:390:15:30"
            d_scale = sec_scale if sec_scale != "440:480" else "440:476"
            d_pos = sec_pos if sec_pos != (320, 1080) else (320, 710)
            d_bg = sec_bg_box if sec_bg_box != (305, 1065, 470, 510) else (305, 695, 470, 506)

            create_discord_game_template(
                out_path=template_png,
                game_box=(g_pos[0], g_pos[1], int(g_scale.split(':')[0]), int(g_scale.split(':')[1])),
                discord_box=d_bg
            )
            extra_inputs = ["-loop", "1", "-i", template_png]

            fc_parts = [
                f"[0:v]scale={CANVAS_WIDTH}:{CANVAS_HEIGHT}:force_original_aspect_ratio=increase,"
                f"crop={CANVAS_WIDTH}:{CANVAS_HEIGHT},boxblur=20:4,eq=brightness=-0.1:contrast=1.05,setsar=1[bg];",
                f"[0:v]crop={g_crop},scale={g_scale}:flags=lanczos,setsar=1[main];",
                f"[0:v]crop={d_crop},scale={d_scale}:flags=lanczos,setsar=1[disc];",
                f"[bg][main]overlay={g_pos[0]}:{g_pos[1]}[tmp1];",
                f"[tmp1]drawbox=x={d_bg[0]}:y={d_bg[1]}:w={d_bg[2]}:h={d_bg[3]}:color=0x2B2D31@1.0:t=fill[tmp_box];",
                f"[tmp_box][disc]overlay={d_pos[0]}:{d_pos[1]}[tmp2];",
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
                "-pix_fmt", "yuv420p",
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

    size_mb = os.path.getsize(output_video) / (1024 * 1024)
    print(f"[Clipper Success] Generated {output_video} ({size_mb:.2f} MB)")
    return output_video

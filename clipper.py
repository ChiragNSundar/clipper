#!/usr/bin/env python3
"""
Universal Clipper CLI
Unified toolkit for clipping, transcribing, and rendering 9:16 vertical reels.
"""

import os
import sys
import json
import tempfile
import argparse
from clipper import (
    render_reel,
    probe_video,
    extract_audio,
    transcribe_audio,
    build_ass_script,
    CANVAS_WIDTH,
    CANVAS_HEIGHT
)

def parse_time_slice(cut_str: str):
    """
    Parse time slice string into list of (start, duration).
    Supports single cut '0:15-0:45' or multi-cut '0:23-0:35,0:56-1:19'.
    """
    if not cut_str:
        return []

    def to_seconds(t_str):
        t_str = t_str.strip()
        if ":" in t_str:
            p = t_str.split(":")
            if len(p) == 2:
                return float(p[0]) * 60 + float(p[1])
            elif len(p) == 3:
                return float(p[0]) * 3600 + float(p[1]) * 60 + float(p[2])
        return float(t_str)

    cuts = []
    parts = cut_str.split(",")
    for p in parts:
        sub = p.strip().split("-")
        if len(sub) == 2:
            st = to_seconds(sub[0])
            en = to_seconds(sub[1])
            cuts.append((st, max(0.0, en - st)))
        else:
            raise ValueError(f"Invalid cut format '{p}'. Expected 'start-end' (e.g. 0:15-0:45)")
    return cuts

def parse_sticker_time(st_str: str):
    """Parse sticker time window like '23.0-27.5'."""
    if not st_str:
        return None
    p = st_str.split("-")
    if len(p) == 2:
        return (float(p[0]), float(p[1]))
    return None

def parse_zoom(z_str: str):
    """Parse zoom window string like '23.0-26.0:450:800:650:120'."""
    if not z_str:
        return None
    parts = z_str.split(":", 1)
    time_part = parts[0]
    crop_part = parts[1] if len(parts) > 1 else "450:800:650:120"
    st, en = time_part.split("-")
    return (float(st), float(en), crop_part)

def parse_sfx_cues(sfx_str: str):
    """Parse comma-separated SFX cues like '8.0:sfx/vine_boom.mp3:0.4,23.0:sfx/vine_boom.mp3:0.45'."""
    if not sfx_str:
        return None
    cues = []
    for item in sfx_str.split(","):
        p = item.strip().split(":")
        if len(p) >= 2:
            t = float(p[0])
            path = p[1]
            vol = float(p[2]) if len(p) > 2 else 0.4
            cues.append((t, path, vol))
    return cues

def run_batch_file(config_path: str):
    """Process a batch of reels defined in a JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        reels_data = json.load(f)

    print(f"\n[Clipper Batch] Found {len(reels_data)} reels to render from {config_path}...\n")
    for idx, r in enumerate(reels_data, 1):
        print(f"🎬 Processing Reel {idx}/{len(reels_data)}: {r.get('name', f'Reel {idx}')}")
        inp = r["input"]
        out = r["out"]
        layout = r.get("layout", "center")
        cut = r.get("cut", None)
        subs = r.get("subs", None)
        header = r.get("top_header", None)
        sticker = r.get("sticker", None)
        s_time = parse_sticker_time(r.get("sticker_time", None))

        cuts = parse_time_slice(cut) if cut else []
        st, dur = cuts[0] if len(cuts) == 1 else (None, None)
        multi_segs = cuts if len(cuts) > 1 else None

        render_reel(
            input_video=inp,
            output_video=out,
            layout=layout,
            ass_subtitle_path=subs,
            start_time=st,
            duration=dur,
            segments=multi_segs,
            top_header=header,
            sticker_path=sticker,
            sticker_time=s_time
        )
    print("\n🎉 [Clipper Batch] All reels completed successfully!\n")

def main():
    parser = argparse.ArgumentParser(description="Universal Clipper for Instagram Reels & TikTok Shorts")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. info command
    p_info = subparsers.add_parser("info", help="Probe video stream details")
    p_info.add_argument("input", help="Path to video file")

    # 2. transcribe command
    p_trans = subparsers.add_parser("transcribe", help="Extract audio and generate ASS subtitles")
    p_trans.add_argument("input", help="Path to video or audio file")
    p_trans.add_argument("--out", "-o", default="subtitles.ass", help="Output .ass path")
    p_trans.add_argument("--model", "-m", default="base", help="Whisper model (base, small)")
    p_trans.add_argument("--margin-v", type=int, default=260, help="Bottom vertical margin in pixels")

    # 3. render command
    p_render = subparsers.add_parser("render", help="Render video into 9:16 vertical Reel")
    p_render.add_argument("input", help="Input video path or YouTube URL")
    p_render.add_argument("--out", "-o", required=True, help="Output reel .mp4 path")
    p_render.add_argument("--layout", "-l", choices=["center", "ambient", "split", "discord_game"], default="center", help="Layout style")
    p_render.add_argument("--cut", "-c", help="Cut time slice e.g. 0:15-0:45 or multi-cut 0:23-0:35,0:56-1:19")
    p_render.add_argument("--subs", "-s", help="Path to existing .ass subtitle file")
    p_render.add_argument("--auto-subs", action="store_true", help="Auto-transcribe and burn subtitles")
    p_render.add_argument("--top-header", help="Text for top header banner")
    p_render.add_argument("--sticker", help="Path to sticker image (e.g. actor portrait, badge)")
    p_render.add_argument("--sticker-time", help="Time window for popping sticker (e.g. 23.0-27.5)")
    p_render.add_argument("--main-crop", default="640:480:320:160", help="Crop for main video in split layout (w:h:x:y)")
    p_render.add_argument("--main-scale", default="800:600", help="Scale for main video in split layout (w:h)")
    p_render.add_argument("--sec-crop", default="230:250:0:15", help="Crop for secondary video in split layout (w:h:x:y)")
    p_render.add_argument("--sec-scale", default="440:480", help="Scale for secondary video in split layout (w:h)")
    p_render.add_argument("--zoom", help="Zoom window e.g. '23.0-26.0:450:800:650:120'")
    p_render.add_argument("--sfx", help="SFX cues e.g. '8.0:sfx/vine_boom.mp3:0.4,23.0:sfx/vine_boom.mp3:0.45'")

    # 4. batch command
    p_batch = subparsers.add_parser("batch", help="Batch render reels from a JSON configuration file")
    p_batch.add_argument("config", help="Path to JSON batch config file")

    args = parser.parse_args()

    if args.command == "info":
        info = probe_video(args.input)
        print("\n--- Video Details ---")
        print(f"File:       {args.input}")
        print(f"Resolution: {info['width']}x{info['height']}")
        print(f"Duration:   {info['duration']:.2f}s")
        print(f"Has Audio:  {info['has_audio']}")
        print(f"Size:       {info['size_bytes'] / (1024*1024):.2f} MB\n")

    elif args.command == "batch":
        run_batch_file(args.config)

    elif args.command == "transcribe":
        with tempfile.TemporaryDirectory() as temp_dir:
            audio_tmp = os.path.join(temp_dir, "temp_audio.wav")
            print(f"[Clipper] Extracting audio from {args.input}...")
            extract_audio(args.input, audio_tmp)
            print(f"[Clipper] Transcribing with Whisper '{args.model}' + Regional Slang Glossary...")
            chunks = transcribe_audio(audio_tmp, model_name=args.model)
            build_ass_script(chunks, args.out, margin_v=args.margin_v)
            print(f"[Clipper Success] Saved subtitles to {args.out}")

    elif args.command == "render":
        cuts = parse_time_slice(args.cut) if args.cut else []
        st, dur = cuts[0] if len(cuts) == 1 else (None, None)
        multi_segs = cuts if len(cuts) > 1 else None

        sub_file = args.subs
        s_time = parse_sticker_time(args.sticker_time)
        z_win = parse_zoom(args.zoom)
        sfx_c = parse_sfx_cues(args.sfx)

        with tempfile.TemporaryDirectory() as temp_dir:
            if args.auto_subs and not sub_file:
                audio_tmp = os.path.join(temp_dir, "temp_render_audio.wav")
                print(f"[Clipper] Auto-transcribing audio from {args.input}...")
                extract_audio(args.input, audio_tmp)
                chunks = transcribe_audio(audio_tmp, model_name="base")
                sub_file = os.path.join(temp_dir, "temp_auto_subs.ass")
                build_ass_script(chunks, sub_file, margin_v=260)

            render_reel(
                input_video=args.input,
                output_video=args.out,
                layout=args.layout,
                ass_subtitle_path=sub_file,
                start_time=st,
                duration=dur,
                segments=multi_segs,
                main_crop=args.main_crop,
                main_scale=args.main_scale,
                sec_crop=args.sec_crop,
                sec_scale=args.sec_scale,
                top_header=args.top_header,
                sticker_path=args.sticker,
                sticker_time=s_time,
                zoom_window=z_win,
                sfx_cues=sfx_c
            )

if __name__ == "__main__":
    main()

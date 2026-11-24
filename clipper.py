#!/usr/bin/env python3
"""
Universal Clipper CLI
Unified toolkit for clipping, transcribing, and rendering 9:16 vertical reels.
"""

import os
import sys
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
    """Parse time slice string like '0:15-0:45' or '12.5-25.0' into (start, duration)."""
    if not cut_str:
        return None, None
    parts = cut_str.split("-")
    if len(parts) != 2:
        raise ValueError(f"Invalid cut format '{cut_str}'. Expected 'start-end' (e.g. 0:15-0:45)")
    
    def to_seconds(t_str):
        t_str = t_str.strip()
        if ":" in t_str:
            p = t_str.split(":")
            if len(p) == 2:
                return float(p[0]) * 60 + float(p[1])
            elif len(p) == 3:
                return float(p[0]) * 3600 + float(p[1]) * 60 + float(p[2])
        return float(t_str)

    start = to_seconds(parts[0])
    end = to_seconds(parts[1])
    return start, max(0.0, end - start)

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
    p_render.add_argument("input", help="Input video path")
    p_render.add_argument("--out", "-o", required=True, help="Output reel .mp4 path")
    p_render.add_argument("--layout", "-l", choices=["center", "ambient", "split"], default="center", help="Layout style")
    p_render.add_argument("--cut", "-c", help="Cut time slice e.g. 0:15-0:45")
    p_render.add_argument("--subs", "-s", help="Path to existing .ass subtitle file")
    p_render.add_argument("--auto-subs", action="store_true", help="Auto-transcribe and burn subtitles")
    p_render.add_argument("--top-header", help="Text for top header banner")
    p_render.add_argument("--sticker", help="Path to sticker image (e.g. actor portrait, badge)")
    p_render.add_argument("--main-crop", default="640:480:320:160", help="Crop for main video in split layout (w:h:x:y)")
    p_render.add_argument("--main-scale", default="800:600", help="Scale for main video in split layout (w:h)")
    p_render.add_argument("--sec-crop", default="230:250:0:15", help="Crop for secondary video in split layout (w:h:x:y)")
    p_render.add_argument("--sec-scale", default="440:480", help="Scale for secondary video in split layout (w:h)")

    args = parser.parse_args()

    if args.command == "info":
        info = probe_video(args.input)
        print("\n--- Video Details ---")
        print(f"File:       {args.input}")
        print(f"Resolution: {info['width']}x{info['height']}")
        print(f"Duration:   {info['duration']:.2f}s")
        print(f"Has Audio:  {info['has_audio']}")
        print(f"Size:       {info['size_bytes'] / (1024*1024):.2f} MB\n")

    elif args.command == "transcribe":
        audio_tmp = "temp_audio.wav"
        print(f"[Clipper] Extracting audio from {args.input}...")
        extract_audio(args.input, audio_tmp)
        print(f"[Clipper] Transcribing with Whisper '{args.model}' + Regional Slang Glossary...")
        chunks = transcribe_audio(audio_tmp, model_name=args.model)
        build_ass_script(chunks, args.out, margin_v=args.margin_v)
        if os.path.exists(audio_tmp):
            os.remove(audio_tmp)
        print(f"[Clipper Success] Saved subtitles to {args.out}")

    elif args.command == "render":
        start_t, dur_t = parse_time_slice(args.cut) if args.cut else (None, None)
        sub_file = args.subs

        if args.auto_subs and not sub_file:
            audio_tmp = "temp_render_audio.wav"
            print(f"[Clipper] Auto-transcribing audio from {args.input}...")
            extract_audio(args.input, audio_tmp)
            chunks = transcribe_audio(audio_tmp, model_name="base")
            sub_file = "temp_auto_subs.ass"
            build_ass_script(chunks, sub_file, margin_v=260)
            if os.path.exists(audio_tmp):
                os.remove(audio_tmp)

        render_reel(
            input_video=args.input,
            output_video=args.out,
            layout=args.layout,
            ass_subtitle_path=sub_file,
            start_time=start_t,
            duration=dur_t,
            main_crop=args.main_crop,
            main_scale=args.main_scale,
            sec_crop=args.sec_crop,
            sec_scale=args.sec_scale,
            top_header=args.top_header,
            sticker_path=args.sticker
        )

        if args.auto_subs and sub_file and os.path.exists(sub_file):
            try:
                os.remove(sub_file)
            except:
                pass

if __name__ == "__main__":
    main()

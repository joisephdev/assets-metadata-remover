#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
from pathlib import Path

from metadata_remover.utils import IMAGE_EXTS, VIDEO_EXTS, check_tools, collect_files
from metadata_remover.metadata import read_metadata
from metadata_remover.formatters import format_table, format_json


def parse_args():
    parser = argparse.ArgumentParser(
        description="Read or remove metadata from images and videos."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    read_parser = subparsers.add_parser("read", help="Display metadata from files")
    read_parser.add_argument("input", help="Directory (or file) to inspect")
    read_parser.add_argument("--json", action="store_true", help="Output as JSON")

    clean_parser = subparsers.add_parser("clean", help="Remove metadata from files")
    clean_parser.add_argument("input", help="Directory (or file) to process")
    clean_parser.add_argument("-o", "--output", help="Output directory (default: <input>_clean)")
    clean_parser.add_argument("--dry-run", action="store_true", help="Simulate without writing")
    clean_parser.add_argument("-v", "--verbose", action="store_true", help="Per-file logging")
    clean_parser.add_argument("--verify", action="store_true", help="Re-inspect copies and report residual metadata")

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    return args


def clean_image(src, dst):
    if dst.exists():
        dst.unlink()
    cmd = ["exiftool", "-all=", "-o", str(dst), str(src)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())


def clean_video(src, dst):
    if dst.exists():
        dst.unlink()
    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-map_metadata", "-1",
        "-map_chapters", "-1",
        "-c", "copy",
        str(dst),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffmpeg error")


def verify_clean(path, category, tools):
    if category == "image":
        if not tools["exiftool"]:
            return None
        cmd = ["exiftool", str(path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        structural_prefixes = (
            "exiftool version", "file name", "directory", "file size",
            "file modification", "file access", "file inode", "file permissions",
            "file type", "mime type", "image width", "image height",
            "bits per sample", "color components", "compression", "orientation",
            "x resolution", "y resolution", "resolution unit", "exif byte order",
            "jfif version", "jfif resolution", "color space", "pixel aspect ratio",
            "duration", "avg bitrate", "bit depth", "color type", "filter",
            "interlace", "image size", "megapixels",
        )
        lines = [
            l.strip() for l in result.stdout.splitlines()
            if l.strip() and not l.lower().startswith(structural_prefixes)
        ]
        return lines
    elif category == "video":
        if not tools["ffmpeg"]:
            return None
        if not tools["ffprobe"]:
            return None
        cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format_tags:stream_tags", str(path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        structural_tags = {
            "major_brand", "minor_version", "compatible_brands",
            "handler_name", "vendor_id", "encoder", "language",
        }
        lines = []
        for l in result.stdout.splitlines():
            l = l.strip()
            if not l or l.startswith("["):
                continue
            upper = l.upper()
            if "TAG:" not in upper:
                continue
            tag_name = l.split("=", 1)[0].replace("TAG:", "").strip().lower()
            if tag_name not in structural_tags:
                lines.append(l)
        return lines
    return None


def print_summary(stats):
    print()
    print(f"  \u2714 Images cleaned: {stats['images_cleaned']}")
    print(f"  \u2714 Videos cleaned: {stats['videos_cleaned']}")

    skip_parts = []
    if stats["unsupported"] > 0:
        skip_parts.append(f"{stats['unsupported']} unsupported")
    if stats["missing_tool"] > 0:
        skip_parts.append(f"{stats['missing_tool']} missing tool")
    skip_detail = f"  ({', '.join(skip_parts)})" if skip_parts else ""
    print(f"  \u23ed Skipped:          {stats['skipped']}{skip_detail}")
    print(f"  \u2716 Errors:           {stats['errors']}")
    print(f"  \U0001F4C1 Output: {stats['output_dir']}")
    print()


def main_clean(args):
    input_path = Path(args.input).resolve()

    if not input_path.exists():
        print(f"Error: '{args.input}' does not exist.", file=sys.stderr)
        sys.exit(2)

    if args.output:
        output_path = Path(args.output).resolve()
    else:
        output_path = Path(str(input_path) + "_clean")

    tools = check_tools()

    if not tools["exiftool"]:
        print("WARNING: exiftool not found. Images will be skipped.")
        print("  Install with: brew install exiftool")
        print()
    if not tools["ffmpeg"]:
        print("WARNING: ffmpeg not found. Videos will be skipped.")
        print("  Install with: brew install ffmpeg")
        print()
    if not tools["ffprobe"]:
        if args.verify:
            print("WARNING: ffprobe not found. Video verification will not work.")
            print("  Install with: brew install ffmpeg  (includes ffprobe)")
            print()

    files = collect_files(input_path)

    input_real = os.path.realpath(str(input_path))
    output_real = os.path.realpath(str(output_path))

    if input_real.startswith(output_real + os.sep):
        print(f"Error: output directory cannot be a parent of input.", file=sys.stderr)
        print(f"  Input:  {input_real}", file=sys.stderr)
        print(f"  Output: {output_real}", file=sys.stderr)
        sys.exit(2)

    stats = {
        "images_cleaned": 0,
        "videos_cleaned": 0,
        "skipped": 0,
        "unsupported": 0,
        "missing_tool": 0,
        "errors": 0,
        "output_dir": str(output_path),
    }

    for src, category in files:
        src_resolved = os.path.realpath(str(src))

        if src_resolved.startswith(output_real + os.sep) or src_resolved == output_real:
            continue

        if category == "unsupported":
            stats["skipped"] += 1
            stats["unsupported"] += 1
            if args.verbose:
                print(f"  SKIP (unsupported): {src}")
            continue

        if category == "image" and not tools["exiftool"]:
            stats["skipped"] += 1
            stats["missing_tool"] += 1
            if args.verbose:
                print(f"  SKIP (exiftool missing): {src}")
            continue

        if category == "video" and not tools["ffmpeg"]:
            stats["skipped"] += 1
            stats["missing_tool"] += 1
            if args.verbose:
                print(f"  SKIP (ffmpeg missing): {src}")
            continue

        if input_path.is_file():
            dst = output_path / src.name
        else:
            rel = src.relative_to(input_path)
            dst = output_path / rel

        if args.dry_run:
            print(f"  WOULD CLEAN: {src} -> {dst}")
            if category == "image":
                stats["images_cleaned"] += 1
            else:
                stats["videos_cleaned"] += 1
            continue

        try:
            dst.parent.mkdir(parents=True, exist_ok=True)

            if args.verbose:
                print(f"  CLEANING: {src} -> {dst}")

            if category == "image":
                clean_image(src, dst)
                stats["images_cleaned"] += 1
            else:
                clean_video(src, dst)
                stats["videos_cleaned"] += 1

            if args.verify:
                residual = verify_clean(dst, category, tools)
                if residual is None:
                    if args.verbose:
                        print(f"    VERIFY: skipped (tool not available)")
                elif residual:
                    print(f"    VERIFY WARNING: residual metadata in {dst}:")
                    for line in residual:
                        print(f"      {line}")
                else:
                    if args.verbose:
                        print(f"    VERIFY OK: no residual metadata")

        except Exception as e:
            stats["errors"] += 1
            print(f"  ERROR: {src}: {e}", file=sys.stderr)

    print_summary(stats)


def main_read(args):
    input_path = Path(args.input).resolve()

    if not input_path.exists():
        print(f"Error: '{args.input}' does not exist.", file=sys.stderr)
        sys.exit(2)

    tools = check_tools()

    if not tools["exiftool"]:
        print("WARNING: exiftool not found. Images will be skipped.")
        print("  Install with: brew install exiftool")
        print()
    if not tools["ffprobe"]:
        print("WARNING: ffprobe not found. Videos will be skipped.")
        print("  Install with: brew install ffmpeg  (includes ffprobe)")
        print()

    files = collect_files(input_path)
    json_results = [] if args.json else None

    for src, category in files:
        if category == "unsupported":
            continue

        if category == "image" and not tools["exiftool"]:
            continue

        if category == "video" and not tools["ffprobe"]:
            continue

        try:
            metadata = read_metadata(src, category)

            if args.json:
                json_results.append({"file": str(src), "metadata": metadata})
            else:
                print(format_table(src, metadata))

        except Exception as e:
            print(f"  ERROR: {src}: {e}", file=sys.stderr)

    if args.json:
        import json
        print(json.dumps(json_results, indent=2, ensure_ascii=False))


def main():
    args = parse_args()
    if args.command == "clean":
        main_clean(args)
    elif args.command == "read":
        main_read(args)


if __name__ == "__main__":
    main()

"""Shared utilities for metadata-remover."""

import os
import shutil
from pathlib import Path

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".webp", ".heic", ".heif", ".gif", ".bmp"}
VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".m4v", ".webm", ".wmv", ".flv", ".3gp"}


def check_tools():
    """Check availability of required system tools."""
    return {
        "exiftool": shutil.which("exiftool") is not None,
        "ffmpeg": shutil.which("ffmpeg") is not None,
        "ffprobe": shutil.which("ffprobe") is not None,
    }


def collect_files(root):
    """Collect all supported image and video files from root path.
    
    Args:
        root: Path to file or directory to scan
        
    Returns:
        List of tuples (path, category) where category is 'image', 'video', or 'unsupported'
    """
    root = Path(root).resolve()
    results = []
    if root.is_file():
        ext = root.suffix.lower()
        if ext in IMAGE_EXTS:
            results.append((root, "image"))
        elif ext in VIDEO_EXTS:
            results.append((root, "video"))
        else:
            results.append((root, "unsupported"))
        return results

    for dirpath, dirnames, filenames in os.walk(str(root), followlinks=False):
        dirnames[:] = [d for d in dirnames if not os.path.islink(os.path.join(dirpath, d))]
        for fname in filenames:
            fpath = Path(dirpath) / fname
            ext = fpath.suffix.lower()
            if ext in IMAGE_EXTS:
                results.append((fpath, "image"))
            elif ext in VIDEO_EXTS:
                results.append((fpath, "video"))
            else:
                results.append((fpath, "unsupported"))
    return results

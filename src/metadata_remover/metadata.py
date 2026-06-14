"""Metadata reading functions for images and videos."""

import json
import subprocess
from pathlib import Path

STRUCTURAL_IMAGE_KEYS = {
    "SourceFile", "ExifToolVersion", "FileName", "Directory", "FileSize",
    "FileModifyDate", "FileAccessDate", "FileInodeChangeDate",
    "FilePermissions", "FileType", "FileTypeExtension", "MIMEType",
    "ImageWidth", "ImageHeight", "BitsPerSample", "ColorComponents",
    "Compression", "Orientation", "XResolution", "YResolution",
    "ResolutionUnit", "ExifByteOrder", "JFIFVersion", "JFIFResolution",
    "ColorSpace", "PixelAspectRatio", "Duration", "AvgBitrate",
    "BitDepth", "ColorType", "Filter", "Interlace", "ImageSize",
    "Megapixels",
}

STRUCTURAL_VIDEO_KEYS = {
    "major_brand", "minor_version", "compatible_brands",
    "handler_name", "vendor_id", "encoder", "language",
    "filename", "nb_streams", "nb_programs", "format_name",
    "format_long_name", "start_time", "duration", "size",
    "bit_rate", "probe_score",
}


def read_image_metadata(path):
    """Read metadata from an image file using exiftool -j.
    
    Args:
        path: Path to image file
        
    Returns:
        Dict of metadata key-value pairs (structural keys filtered out)
        
    Raises:
        RuntimeError: If exiftool fails
    """
    cmd = ["exiftool", "-j", str(path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    
    data = json.loads(result.stdout)
    if not data:
        return {}
    
    metadata = data[0]
    return {k: v for k, v in metadata.items() if k not in STRUCTURAL_IMAGE_KEYS}


def read_video_metadata(path):
    """Read metadata from a video file using ffprobe.
    
    Args:
        path: Path to video file
        
    Returns:
        Dict of metadata key-value pairs (structural keys filtered out)
        
    Raises:
        RuntimeError: If ffprobe fails
    """
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        str(path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffprobe error")
    
    data = json.loads(result.stdout)
    metadata = {}
    
    if "format" in data and "tags" in data["format"]:
        for k, v in data["format"]["tags"].items():
            if k.lower() not in STRUCTURAL_VIDEO_KEYS:
                metadata[k] = v
    
    for stream in data.get("streams", []):
        if "tags" in stream:
            for k, v in stream["tags"].items():
                if k.lower() not in STRUCTURAL_VIDEO_KEYS:
                    key = f"{k} (stream {stream.get('index', '?')})"
                    metadata[key] = v
    
    return metadata


def read_metadata(path, category):
    """Read metadata from a file based on its category.
    
    Args:
        path: Path to file
        category: 'image' or 'video'
        
    Returns:
        Dict of metadata key-value pairs
        
    Raises:
        RuntimeError: If underlying tool fails
        ValueError: If category is unsupported
    """
    path = Path(path)
    if category == "image":
        return read_image_metadata(path)
    elif category == "video":
        return read_video_metadata(path)
    else:
        raise ValueError(f"Unsupported category: {category}")

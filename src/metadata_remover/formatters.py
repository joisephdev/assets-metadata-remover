"""Output formatters for metadata display."""

import json

from metadata_remover.metadata import extract_gps_location

MAX_VALUE_LENGTH = 60


def truncate_value(value, max_length=MAX_VALUE_LENGTH):
    """Truncate a value to max_length, adding ellipsis if needed."""
    s = str(value)
    if len(s) > max_length:
        return s[:max_length - 3] + "..."
    return s


def format_table(filename, metadata):
    """Format metadata as a human-readable table with box-drawing characters.
    
    Args:
        filename: Path or name of the file
        metadata: Dict of metadata key-value pairs
        
    Returns:
        String with formatted table
    """
    if not metadata:
        return f"\nFile: {filename}\n  (no metadata found)\n"
    
    gps = extract_gps_location(metadata)
    
    key_width = max(len(str(k)) for k in metadata.keys())
    key_width = max(key_width, 3)
    
    val_width = max(len(truncate_value(v)) for v in metadata.values())
    val_width = max(val_width, 5)
    
    lines = []
    lines.append(f"\nFile: {filename}")
    
    if gps:
        lines.append(f"  📍 Location: {gps['latitude']}, {gps['longitude']}")
        lines.append(f"  🗺️  Maps: {gps['maps_link']}")
        lines.append("")
    
    lines.append("\u250c" + "\u2500" * (key_width + 2) + "\u252c" + "\u2500" * (val_width + 2) + "\u2510")
    lines.append(
        "\u2502 " + "Key".ljust(key_width) + " \u2502 " + "Value".ljust(val_width) + " \u2502"
    )
    lines.append("\u251c" + "\u2500" * (key_width + 2) + "\u253c" + "\u2500" * (val_width + 2) + "\u2524")
    
    for key, value in metadata.items():
        k = str(key).ljust(key_width)
        v = truncate_value(value).ljust(val_width)
        lines.append(f"\u2502 {k} \u2502 {v} \u2502")
    
    lines.append("\u2514" + "\u2500" * (key_width + 2) + "\u2534" + "\u2500" * (val_width + 2) + "\u2518")
    
    return "\n".join(lines)


def format_json(filename, metadata):
    """Format metadata as JSON.
    
    Args:
        filename: Path or name of the file
        metadata: Dict of metadata key-value pairs
        
    Returns:
        JSON string
    """
    gps = extract_gps_location(metadata)
    
    result = {"file": str(filename), "metadata": metadata}
    if gps:
        result["location"] = gps
    
    return json.dumps(result, indent=2, ensure_ascii=False)


def format_removal_table(filename, metadata):
    """Format metadata as a removal report table.
    
    Args:
        filename: Path or name of the file
        metadata: Dict of metadata key-value pairs that were removed
        
    Returns:
        String with formatted table showing removed metadata
    """
    if not metadata:
        return f"\n  {filename}\n    (no metadata removed)\n"
    
    key_width = max(len(str(k)) for k in metadata.keys())
    key_width = max(key_width, 3)
    
    val_width = max(len(truncate_value(v)) for v in metadata.values())
    val_width = max(val_width, 13)
    
    lines = []
    lines.append(f"\n  {filename}")
    lines.append(f"  Metadata removed:")
    lines.append("  \u250c" + "\u2500" * (key_width + 2) + "\u252c" + "\u2500" * (val_width + 2) + "\u2510")
    lines.append(
        "  \u2502 " + "Key".ljust(key_width) + " \u2502 " + "Removed Value".ljust(val_width) + " \u2502"
    )
    lines.append("  \u251c" + "\u2500" * (key_width + 2) + "\u253c" + "\u2500" * (val_width + 2) + "\u2524")
    
    for key, value in metadata.items():
        k = str(key).ljust(key_width)
        v = truncate_value(value).ljust(val_width)
        lines.append(f"  \u2502 {k} \u2502 {v} \u2502")
    
    lines.append("  \u2514" + "\u2500" * (key_width + 2) + "\u2534" + "\u2500" * (val_width + 2) + "\u2518")
    
    return "\n".join(lines)

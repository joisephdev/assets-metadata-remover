"""Output formatters for metadata display."""

import json

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
    
    key_width = max(len(str(k)) for k in metadata.keys())
    key_width = max(key_width, 3)
    
    val_width = max(len(truncate_value(v)) for v in metadata.values())
    val_width = max(val_width, 5)
    
    lines = []
    lines.append(f"\nFile: {filename}")
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
    return json.dumps({"file": str(filename), "metadata": metadata}, indent=2, ensure_ascii=False)

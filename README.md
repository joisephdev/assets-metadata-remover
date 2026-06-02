# metadata-remover

Command-line tool that removes metadata from images and videos recursively, generating clean copies in an output folder that mirrors the original structure. Original files are **never** modified.

## Requirements

- **Python 3.9+** (uses only the standard library, no pip dependencies)
- **ffmpeg** — required for video processing
- **exiftool** — required for image processing

Install with Homebrew:

```bash
brew install ffmpeg exiftool
```

> If a tool is missing, the script detects it at startup and processes only the files it can, showing a clear warning.

## Basic usage

```bash
python3 metadata_remover.py /path/to/your_files
```

This creates `/path/to/your_files_clean/` with the same folder structure and metadata-free files.

### Options

```
usage: metadata_remover.py [-h] [-o OUTPUT] [--dry-run] [-v] [--verify] input

positional:
  input              Directory (or file) to process

options:
  -o, --output DIR   Output directory (default: <input>_clean)
  --dry-run          Simulate without writing
  -v, --verbose      Per-file logging
  --verify           Re-inspect copies and report residual metadata
```

### Examples

Process a directory with custom output:

```bash
python3 metadata_remover.py ~/Photos -o ~/Photos_clean
```

Simulate without writing (dry run):

```bash
python3 metadata_remover.py ~/Photos --dry-run
```

Verbose mode with cleanup verification:

```bash
python3 metadata_remover.py ~/Photos -v --verify
```

Process a single file:

```bash
python3 metadata_remover.py ~/photo.jpg -o ~/clean/
```

## Safety

Original files are **never** modified. The script always writes to a separate output folder.

## Supported formats

**Images:** JPG, JPEG, PNG, TIFF, TIF, WebP, HEIC, HEIF, GIF, BMP

**Videos:** MP4, MOV, MKV, AVI, M4V, WebM, WMV, FLV, 3GP

Extension comparison is case-insensitive (`.JPG` and `.jpg` are equivalent).

## Limitations

- Videos are copied without re-encoding (`-c copy`), which is fast and lossless, but some exotic formats may not be compatible with the output container.
- Some metadata embedded in proprietary formats may not be fully removed by `exiftool`.
- Directory symlinks are not followed to avoid loops.

# assets-metadata-remover

Command-line tool that removes metadata from images and videos recursively, generating clean copies in an output folder that mirrors the original structure. Original files are **never** modified.

## Installation

### With pipx (recommended)

```bash
pipx install assets-metadata-remover
```

### With pip

```bash
pip install assets-metadata-remover
```

### System dependencies

- **ffmpeg** — required for video processing
- **exiftool** — required for image processing

Install with Homebrew:

```bash
brew install ffmpeg exiftool
```

> If a tool is missing, the script detects it at startup and processes only the files it can, showing a clear warning.

## Commands

### clean — Remove metadata

```bash
assets-metadata-remover clean /path/to/your_files
```

This creates `/path/to/your_files_clean/` with the same folder structure and metadata-free files.

#### Options

```
usage: assets-metadata-remover clean [-h] [-o OUTPUT] [--dry-run] [-v] [--verify] [--report] input

positional:
  input              Directory (or file) to process

options:
  -o, --output DIR   Output directory (default: <input>_clean)
  --dry-run          Simulate without writing
  -v, --verbose      Per-file logging
  --verify           Re-inspect copies and report residual metadata
  --report           Show table of metadata removed from each file
```

#### Examples

Process a directory with custom output:

```bash
assets-metadata-remover clean ~/Photos -o ~/Photos_clean
```

Simulate without writing (dry run):

```bash
assets-metadata-remover clean ~/Photos --dry-run
```

Verbose mode with cleanup verification:

```bash
assets-metadata-remover clean ~/Photos -v --verify
```

Show metadata removal report:

```bash
assets-metadata-remover clean ~/Photos --report
```

Process a single file:

```bash
assets-metadata-remover clean ~/photo.jpg -o ~/clean/
```

### read — Display metadata

```bash
assets-metadata-remover read /path/to/your_files
```

Displays metadata from images and videos in a human-readable table format.

#### Options

```
usage: assets-metadata-remover read [-h] [--json] input

positional:
  input              Directory (or file) to inspect

options:
  --json             Output as JSON
```

#### Examples

Read metadata from a single file:

```bash
assets-metadata-remover read ~/photo.jpg
```

Read metadata from a directory:

```bash
assets-metadata-remover read ~/Photos
```

Output as JSON for programmatic use:

```bash
assets-metadata-remover read ~/Photos --json
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

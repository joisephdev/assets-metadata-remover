# assets-metadata-remover

[![PyPI version](https://img.shields.io/pypi/v/assets-metadata-remover.svg)](https://pypi.org/project/assets-metadata-remover/)
[![Python versions](https://img.shields.io/pypi/pyversions/assets-metadata-remover.svg)](https://pypi.org/project/assets-metadata-remover/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line tool to **read and remove metadata** from images and videos recursively. Generates clean copies in an output folder that mirrors the original structure. Original files are **never** modified.

## Features

- **Read metadata** — Display metadata from images and videos in table or JSON format
- **Remove metadata** — Strip all metadata (EXIF, XMP, IPTC, GPS, etc.) from files
- **Removal reports** — Show detailed tables of what metadata was removed from each file
- **Recursive processing** — Process entire directory trees while preserving folder structure
- **Safety first** — Original files are never modified; always writes to separate output folder
- **Graceful degradation** — Continues processing even if some tools are missing

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

- **exiftool** — required for image processing
- **ffmpeg** — required for video processing

**macOS:**
```bash
brew install exiftool ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install libimage-exiftool-perl ffmpeg
```

**Fedora:**
```bash
sudo dnf install perl-Image-ExifTool ffmpeg
```

> If a tool is missing, the script detects it at startup and processes only the files it can handle, showing a clear warning.

## Quick start

```bash
# Read metadata from a photo
assets-metadata-remover read ~/photo.jpg

# Remove metadata from a directory
assets-metadata-remover clean ~/Photos

# Show what was removed
assets-metadata-remover clean ~/Photos --report
```

## Commands

### `read` — Display metadata

Display metadata from images and videos in a human-readable table or JSON format.

```bash
assets-metadata-remover read <path> [--json]
```

**Options:**
- `--json` — Output as JSON (useful for scripting)

**Examples:**

Read metadata from a single file:
```bash
$ assets-metadata-remover read ~/photo.jpg

File: /Users/you/photo.jpg
┌─────────────────────┬──────────────────────────────┐
│ Key                 │ Value                        │
├─────────────────────┼──────────────────────────────┤
│ Make                │ Canon                        │
│ Model               │ Canon EOS 5D Mark IV         │
│ DateTimeOriginal    │ 2024:03:15 14:23:45          │
│ GPSLatitude         │ 40 deg 42' 46.08" N          │
│ GPSLongitude        │ 74 deg 0' 21.60" W           │
└─────────────────────┴──────────────────────────────┘
```

Read metadata from a directory:
```bash
assets-metadata-remover read ~/Photos
```

Output as JSON for programmatic use:
```bash
assets-metadata-remover read ~/Photos --json | jq '.[] | select(.metadata.GPSLatitude)'
```

### `clean` — Remove metadata

Remove all metadata from images and videos, creating clean copies in an output folder.

```bash
assets-metadata-remover clean <path> [options]
```

**Options:**
- `-o, --output DIR` — Output directory (default: `<input>_clean`)
- `--dry-run` — Simulate without writing files
- `-v, --verbose` — Show per-file logging
- `--verify` — Re-inspect copies and report residual metadata
- `--report` — Show table of metadata removed from each file

**Examples:**

Process a directory with custom output:
```bash
assets-metadata-remover clean ~/Photos -o ~/Photos_clean
```

Simulate without writing (dry run):
```bash
assets-metadata-remover clean ~/Photos --dry-run
```

Show metadata removal report:
```bash
$ assets-metadata-remover clean ~/Photos --report

/Users/you/Photos/vacation.jpg
  Metadata removed:
  ┌─────────────────────┬──────────────────────────────┐
  │ Key                 │ Removed Value                │
  ├─────────────────────┼──────────────────────────────┤
  │ Make                │ Canon                        │
  │ Model               │ Canon EOS 5D Mark IV         │
  │ GPSLatitude         │ 40 deg 42' 46.08" N          │
  │ GPSLongitude        │ 74 deg 0' 21.60" W           │
  │ DateTimeOriginal    │ 2024:03:15 14:23:45          │
  └─────────────────────┴──────────────────────────────┘

  ✔ Images cleaned: 1
  ✔ Videos cleaned: 0
  ⏭ Skipped:          0
  ✖ Errors:           0
  📊 Total metadata fields removed: 5
  📁 Output: /Users/you/Photos_clean
```

Verbose mode with verification:
```bash
assets-metadata-remover clean ~/Photos -v --verify
```

Process a single file:
```bash
assets-metadata-remover clean ~/photo.jpg -o ~/clean/
```

## Supported formats

**Images:** JPG, JPEG, PNG, TIFF, TIF, WebP, HEIC, HEIF, GIF, BMP

**Videos:** MP4, MOV, MKV, AVI, M4V, WebM, WMV, FLV, 3GP

Extension comparison is case-insensitive (`.JPG` and `.jpg` are equivalent).

## Safety

Original files are **never** modified. The script always writes to a separate output folder.

- The `clean` command creates copies in `<input>_clean/` by default
- Use `-o` to specify a custom output directory
- Use `--dry-run` to preview what would be processed without writing files
- Directory symlinks are not followed to avoid infinite loops

## Limitations

- Videos are copied without re-encoding (`-c copy`), which is fast and lossless, but some exotic formats may not be compatible with the output container
- Some metadata embedded in proprietary formats may not be fully removed by `exiftool`
- Reading metadata before cleaning (with `--report` or `-v`) doubles the number of tool calls per file

## Development

### Setup

```bash
git clone https://github.com/synapsync/assets-metadata-remover.git
cd assets-metadata-remover
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Build and publish

```bash
make build          # Build wheel and sdist
make publish        # Upload to PyPI
make publish-test   # Upload to TestPyPI
make test           # Run smoke tests
```

### CI/CD

This project uses GitHub Actions for automated releases:

1. **Push to main** → Triggers the release workflow
2. **Semantic Release** → Analyzes conventional commits and determines version bump
3. **Build & Publish** → Builds package and publishes to PyPI
4. **GitHub Release** → Creates a new release with changelog

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` → Minor version bump (1.0.0 → 1.1.0)
- `fix:` → Patch version bump (1.0.0 → 1.0.1)
- `feat!:` or `BREAKING CHANGE:` → Major version bump (1.0.0 → 2.0.0)

## License

MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.

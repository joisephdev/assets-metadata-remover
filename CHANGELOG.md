# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v1.5.0 (2026-06-14)

### Features
- Added GPS location extraction with consolidated coordinates in decimal format
- Display Google Maps link for photos with GPS data
- Enhanced `read` command output with location summary
- Added `location` field to JSON output with latitude, longitude, and maps link

## v1.4.0 (2026-06-14)

### Features
- Improved README with badges, multi-platform installations, and real output examples
- Added comprehensive changelog
- Enhanced documentation with quick start guide

## v1.3.0 (2026-06-14)

### Features
- Added `--report` flag to `clean` command to show metadata removal tables
- Added total metadata fields removed count in summary

### Bug Fixes
- Filter out `_original` backup files from directory scans

## v1.2.0 (2026-06-14)

### Features
- Added `read` command to display metadata from files
- Support for table and JSON output formats
- Graceful handling of missing tools

## v1.1.0 (2026-06-14)

### Features
- Refactored to subcommand architecture (`read` and `clean`)
- Extracted shared utilities to separate module

## v1.0.0 (2026-06-14)

### Features
- Initial release
- Remove metadata from images and videos recursively
- Support for exiftool and ffmpeg

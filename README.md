# Firmware Diff Tool

A simple firmware-aware comparison tool written in Python.

## Features

- Text file diff
- Binary file diff
- Directory diff
- Changed regions detection
- Region summary
- JSON output
- Quiet mode for automation
- Exit code control with `--fail-if-different`
- Ignore `0xFF` padding differences
- Ignore `0x00` padding differences
- Filter regions by minimum size

## Usage

### Text mode

    python main.py text file1 file2 [output_file]

### Binary mode

    python main.py bin file1 file2 [output_file] [options]

Binary mode options:

    --fail-if-different
    --ignore-ff
    --ignore-00
    --max-diffs N
    --regions-only
    --json
    --quiet
    --min-region-size N

### Directory mode

    python main.py dir dir1 dir2 [output_file]

## Examples

### Text diff

    python main.py text samples\text\old.txt samples\text\new.txt output\result.diff

### Binary diff

    python main.py bin samples\binary\a.bin samples\binary\b.bin output\bin_result.txt

### Binary diff with ignored padding

    python main.py bin samples\binary\a.bin samples\binary\b.bin --ignore-ff --ignore-00

### Binary diff with region filtering

    python main.py bin samples\binary\a.bin samples\binary\b.bin --regions-only --min-region-size 2

### Binary diff as JSON

    python main.py bin samples\binary\a.bin samples\binary\b.bin output\bin_result.json --json

### Binary diff for automation

    python main.py bin samples\binary\a.bin samples\binary\b.bin --fail-if-different --quiet

### Directory diff

    python main.py dir samples\dir\dirA samples\dir\dirB output\dir_result.txt

## Notes

This tool is currently an early prototype focused on firmware-oriented binary comparison and analysis.

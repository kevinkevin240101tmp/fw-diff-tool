[English](#english) | [繁體中文](#繁體中文)

---

## English

Quickly understand what changed between firmware versions — with region-level analysis, padding-aware diff, and automation-friendly output.

---

## 繁體中文

快速了解兩個 firmware 版本之間的差異 — 透過區段分析、忽略 padding 雜訊，以及支援自動化流程的輸出。

---

### 🔍 Region-level insight
Group byte differences into meaningful regions so you can quickly identify modified areas instead of scanning raw byte diffs.

### 🧹 Padding-aware diff
Ignore `0xFF` and `0x00` noise commonly found in firmware images.

### ⚙️ Automation-ready
CLI-first design with JSON output and proper exit codes for scripting and CI pipelines.

---

## Why this tool?

### ❌ Traditional byte diff (hard to read)

    offset 0x00000001 : 0x02 -> 0xFF
    offset 0x00000002 : 0x03 -> 0x88
    offset 0x00000003 : 0x04 -> 0x99

Hard to understand what actually changed.

---

### ✅ Region-based diff (this tool)

    Changed regions:
      0x00000001 - 0x00000003 (3 bytes)

    Region summary:
      total changed bytes : 3
      total regions       : 1
      largest region size : 3 bytes

Quickly see where the change is.

---

## Demo

### Input

    python main.py bin samples\binary\a.bin samples\binary\b.bin --regions-only

### Output

    Binary diff result
    File 1: samples\binary\a.bin (5 bytes)
    File 2: samples\binary\b.bin (6 bytes)

    File sizes differ: samples\binary\a.bin=5 bytes, samples\binary\b.bin=6 bytes

    Changed regions:
      0x00000001 - 0x00000001 (1 bytes)
      0x00000003 - 0x00000003 (1 bytes)

    Region summary:
      total changed bytes : 2
      total regions       : 2
      largest region size : 1 bytes

### JSON Output

    python main.py bin samples\binary\a.bin samples\binary\b.bin --json

    {
      "mode": "bin",
      "file1": "...",
      "regions": [...],
      "region_summary": {
        "total_changed_bytes": 2,
        "total_regions": 2,
        "largest_region_size": 1
      }
    }

---

## Use Cases

### 🔧 Firmware comparison during development
Quickly identify what changed between firmware builds without scanning raw byte diffs.

### 🧪 Regression / release verification
Use `--fail-if-different` in scripts to detect unintended changes between firmware versions.

### 🧹 Ignore padding noise
Filter out `0xFF` / `0x00` differences to focus on meaningful changes in flash images.

### ⚙️ Automation / CI integration
Generate JSON output and integrate with build pipelines or testing scripts.

### 🔍 Reverse engineering / analysis
Locate modified regions in binary files for further inspection.

---

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

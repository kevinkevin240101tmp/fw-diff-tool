# Firmware Diff Tool

Quickly understand what changed between firmware versions — with region-level analysis, padding-aware diff, and automation-friendly output.

[English](#english) | [繁體中文](#繁體中文)

---

# English

## 🔍 Region-level insight

Group byte differences into meaningful regions so you can quickly identify modified areas instead of scanning raw byte diffs.

## 🧹 Padding-aware diff

Ignore `0xFF` and `0x00` noise commonly found in firmware images.

## ⚙️ Automation-ready

CLI-first design with JSON output and proper exit codes for scripting and CI pipelines.

---

## Why this tool?

### ❌ Traditional byte diff (hard to read)

```
offset 0x00000001 : 0x02 -> 0xFF
offset 0x00000002 : 0x03 -> 0x88
offset 0x00000003 : 0x04 -> 0x99
```

Hard to understand what actually changed.

---

### ✅ Region-based diff (this tool)

```
Changed regions:
  0x00000001 - 0x00000003 (3 bytes)

Region summary:
  total changed bytes : 3
  total regions       : 1
  largest region size : 3 bytes
```

Quickly see where the change is.

---

## Demo

### Input

```
python main.py bin samples\binary\a.bin samples\binary\b.bin --regions-only
```

### Output

```
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
```

### JSON Output

```
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
```

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

# 繁體中文

## 🔍 區段分析

將 byte 差異整理為有意義的區段，讓你快速掌握修改範圍，而不是逐一查看 offset。

## 🧹 忽略 padding 雜訊

過濾 firmware 常見的 `0xFF` / `0x00` 填充資料，專注於實際變動。

## ⚙️ 支援自動化

CLI 設計，支援 JSON 輸出與 exit code，可整合至 script 或 CI 流程。

---

## 為什麼需要這個工具？

### ❌ 傳統 byte diff（難以閱讀）

```
offset 0x00000001 : 0x02 -> 0xFF
offset 0x00000002 : 0x03 -> 0x88
offset 0x00000003 : 0x04 -> 0x99
```

很難快速理解實際改動位置。

---

### ✅ 區段分析（本工具）

```
Changed regions:
  0x00000001 - 0x00000003 (3 bytes)

Region summary:
  total changed bytes : 3
  total regions       : 1
  largest region size : 3 bytes
```

可以快速看出變動區段。

---

## 使用情境

### 🔧 Firmware 開發比對

快速比較不同版本 firmware 差異，不需逐一檢視 byte diff。

### 🧪 回歸測試 / 發佈驗證

搭配 `--fail-if-different` 自動檢測版本差異。

### 🧹 忽略 padding 雜訊

過濾 `0xFF` / `0x00` 差異，專注實際變動。

### ⚙️ 自動化 / CI 整合

透過 JSON 與 exit code 整合至 build pipeline。

### 🔍 逆向工程 / 分析

快速定位 binary 中被修改的區段。

---

# Technical Details

## Features

* Text file diff
* Binary file diff
* Directory diff
* Changed regions detection
* Region summary
* JSON output
* Quiet mode for automation
* Exit code control with `--fail-if-different`
* Ignore `0xFF` padding differences
* Ignore `0x00` padding differences
* Filter regions by minimum size

## Usage

### Text mode

```
python main.py text file1 file2 [output_file]
```

### Binary mode

```
python main.py bin file1 file2 [output_file] [options]
```

Options:

```
--fail-if-different
--ignore-ff
--ignore-00
--max-diffs N
--regions-only
--json
--quiet
--min-region-size N
```

### Directory mode

```
python main.py dir dir1 dir2 [output_file]
```

## Examples

### Text diff

```
python main.py text samples\text\old.txt samples\text\new.txt output\result.diff
```

### Binary diff

```
python main.py bin samples\binary\a.bin samples\binary\b.bin output\bin_result.txt
```

### Binary diff with ignored padding

```
python main.py bin samples\binary\a.bin samples\binary\b.bin --ignore-ff --ignore-00
```

### Binary diff with region filtering

```
python main.py bin samples\binary\a.bin samples\binary\b.bin --regions-only --min-region-size 2
```

### Binary diff as JSON

```
python main.py bin samples\binary\a.bin samples\binary\b.bin output\bin_result.json --json
```

### Binary diff for automation

```
python main.py bin samples\binary\a.bin samples\binary\b.bin --fail-if-different --quiet
```

### Directory diff

```
python main.py dir samples\dir\dirA samples\dir\dirB output\dir_result.txt
```

## Notes

This tool is an evolving firmware-oriented binary analysis utility.

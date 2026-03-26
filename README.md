# Firmware Diff Tool

Quickly understand what changed between firmware versions — with region-level analysis, padding-aware diff, and automation-friendly output.

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

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

## Use Cases

* Firmware comparison during development
* Regression / release verification
* Ignore padding noise
* Automation / CI integration
* Reverse engineering

---

# 简体中文

## 🔍 区段分析

将 byte 差异整理为区段，快速掌握修改范围。

## 🧹 忽略 padding 噪声

过滤 `0xFF` / `0x00`，专注真实变动。

## ⚙️ 支持自动化

支持 JSON 与 exit code，可整合 CI / script。

---

## 为什么需要这个工具？

### ❌ 传统 byte diff（难以阅读）

```
offset 0x00000001 : 0x02 -> 0xFF
offset 0x00000002 : 0x03 -> 0x88
offset 0x00000003 : 0x04 -> 0x99
```

难以快速理解实际变动。

---

### ✅ 区段分析（本工具）

```
Changed regions:
  0x00000001 - 0x00000003 (3 bytes)

Region summary:
  total changed bytes : 3
  total regions       : 1
  largest region size : 3 bytes
```

快速看出变化区域。

---

# 繁體中文

## 🔍 區段分析

將 byte 差異整理為區段，快速掌握修改範圍。

## 🧹 忽略 padding 雜訊

過濾 `0xFF` / `0x00`，專注真正變動。

## ⚙️ 支援自動化

支援 JSON 與 exit code，可整合 CI / script。

---

## 為什麼需要這個工具？

### ❌ 傳統 byte diff（難以閱讀）

```
offset 0x00000001 : 0x02 -> 0xFF
offset 0x00000002 : 0x03 -> 0x88
offset 0x00000003 : 0x04 -> 0x99
```

很難快速理解實際改動。

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

快速看出變動區段。

---

# Technical Details

## Features

* Text file diff
* Binary file diff
* Directory diff
* Changed regions detection
* Region summary
* JSON output
* Quiet mode
* `--fail-if-different`
* Ignore `0xFF` / `0x00`

## Usage

```
python main.py [mode] [args]
```

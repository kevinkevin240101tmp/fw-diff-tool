# Firmware Diff Tool

Understand firmware (binary) changes instantly — without reading raw hex.

A lightweight CLI tool focused on **firmware / binary comparison**, with additional text and directory diff modes.

Designed for engineers who need fast, scriptable, and reliable diff results.

---

## 🚀 Features

**Primary (Firmware / Binary):**

* Binary comparison (byte-level + regions)
* Changed region detection
* Summary report (size, count, largest region)
* JSON output (for automation / CI)

**Additional:**

* Text file comparison (unified diff)
* Directory comparison

---

## ⚙️ Usage

### Show help

```bash
python main.py -h
```

---

## 🧩 Modes

```
bin   Compare two binary files and show byte differences / regions
text  Compare two text files and output unified diff
dir   Compare two directories and list changed / added / removed files
```

👉 For detailed usage of each mode:

```bash
python main.py bin -h
python main.py text -h
python main.py dir -h
```

---

## 🔧 Binary mode (Primary)

Compare binary files at byte level, with region detection and summary.

Compare two binary files:

```bash
python main.py bin old.bin new.bin
```

Save result:

```bash
python main.py bin old.bin new.bin result.txt
```

JSON output (for automation / CI):

```bash
python main.py bin old.bin new.bin --json
```

Common options:

```bash
--ignore-ff          Ignore differences where either byte is 0xFF
--ignore-00          Ignore differences where either byte is 0x00
--regions-only       Show only changed regions
--min-region-size N  Only show regions >= N bytes
--fail-if-different  Exit with code 1 if differences exist
--max-diffs N        Limit number of differences (default: 100)
```

---

## 📝 Text mode (Additional)

Compare two text files:

```bash
python main.py text old.txt new.txt
```

Save result:

```bash
python main.py text old.txt new.txt result.diff
```

---

## 📂 Directory mode (Additional)

Compare two directories:

```bash
python main.py dir dirA dirB
```

Save result:

```bash
python main.py dir dirA dirB dir_result.txt
```

---

## 🧪 Quick test (recommended)

After unzip, run this command to verify everything works:

```bash
python main.py bin samples/binary/a.bin samples/binary/b.bin
```

---

## 📦 What you get

* `main.py`
* `README.md`
* `samples/`

---

## 🎯 Use cases

* Firmware comparison
* Binary diff inspection
* Embedded system analysis
* File system comparison

---

## ⚠️ Notes

* CLI tool (no GUI)
* Designed for practical and scriptable usage
* Lightweight and easy to modify

---

## 🔧 Requirements

* Python 3.x


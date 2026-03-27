# Firmware Diff Tool

A lightweight CLI tool for comparing text files, binary files, and directories.

---

## 🚀 Features

* Text file comparison (unified diff)
* Binary comparison (byte-level + regions)
* Directory comparison
* Changed region detection
* Summary report
* JSON output (binary mode)

---

## ⚙️ Usage

### Show help

```bash
python main.py -h
```

---

## 🧩 Modes

```
text  Compare two text files and output unified diff
bin   Compare two binary files and show byte differences / regions
dir   Compare two directories and list changed / added / removed files
```

👉 For detailed usage of each mode:

```bash
python main.py text -h
python main.py bin -h
python main.py dir -h
```

---

## 📝 Text mode

Compare two text files:

```bash
python main.py text old.txt new.txt
```

Save result:

```bash
python main.py text old.txt new.txt result.diff
```

---

## 🔧 Binary mode

Compare two binary files:

```bash
python main.py bin old.bin new.bin
```

Save result:

```bash
python main.py bin old.bin new.bin result.txt
```

JSON output:

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

## 📂 Directory mode

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

After unzip, try:

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
* Embedded system analysis
* Binary diff inspection
* File system comparison

---

## ⚠️ Notes

* CLI tool (no GUI)
* Designed for practical and scriptable usage
* Lightweight and easy to modify

---

## 🔧 Requirements

* Python 3.x

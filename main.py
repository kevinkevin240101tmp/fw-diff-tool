# Firmware Diff Tool - main.py
# (Paste or edit your code here)

import sys
import difflib
from pathlib import Path
import filecmp
import argparse
import json


def print_help():
    print("Firmware Diff Tool")
    print("")
    print("Usage:")
    print("  Text mode     : python main.py file1 file2 [output_file]")
    print("  Binary mode   : python main.py --bin file1 file2 [output_file]")
    print("  Directory mode: python main.py --dir dir1 dir2 [output_file]")
    print("")
    print("Examples:")
    print("  python main.py old.txt new.txt")
    print("  python main.py old.txt new.txt result.diff")
    print("  python main.py --bin a.bin b.bin")
    print("  python main.py --bin a.bin b.bin bin_result.txt")
    print("  python main.py --dir dirA dirB")
    print("  python main.py --dir dirA dirB dir_result.txt")


def read_text_file(path):
    with open(path, 'r', errors='ignore') as f:
        return f.readlines()


def diff_text_files(file1, file2):
    f1 = read_text_file(file1)
    f2 = read_text_file(file2)

    return difflib.unified_diff(
        f1, f2,
        fromfile=file1,
        tofile=file2,
        lineterm=''
    )


def read_binary_file(path):
    with open(path, 'rb') as f:
        return f.read()


def diff_binary_files(file1, file2, max_diffs=100, ignore_ff=False, ignore_00=False):
    b1 = read_binary_file(file1)
    b2 = read_binary_file(file2)

    len1 = len(b1)
    len2 = len(b2)
    min_len = min(len1, len2)

    diffs = []
    for i in range(min_len):
        if b1[i] != b2[i]:
            if ignore_ff and (b1[i] == 0xFF or b2[i] == 0xFF):
                continue

            if ignore_00 and (b1[i] == 0x00 or b2[i] == 0x00):
                continue

            diffs.append((i, b1[i], b2[i]))
            if len(diffs) >= max_diffs:
                break

    extra_info = None
    if len1 != len2:
        extra_info = f"File sizes differ: {file1}={len1} bytes, {file2}={len2} bytes"

    return diffs, extra_info, len1, len2


def build_changed_regions(diffs):
    regions = []
    if not diffs:
        return regions

    start = diffs[0][0]
    end = diffs[0][0]

    for offset, _, _ in diffs[1:]:
        if offset == end + 1:
            end = offset
        else:
            regions.append((start, end))
            start = offset
            end = offset

    regions.append((start, end))
    return regions


def format_changed_regions(regions):
    lines = []
    lines.append("Changed regions:")

    if not regions:
        lines.append("  None")
        return lines

    for start, end in regions:
        size = end - start + 1
        lines.append(f"  0x{start:08X} - 0x{end:08X} ({size} bytes)")

    return lines


def format_binary_diff(file1, file2, diffs, extra_info, len1, len2, max_diffs, regions_only=False, min_region_size=1):
    lines = []
    lines.append("Binary diff result")
    lines.append(f"File 1: {file1} ({len1} bytes)")
    lines.append(f"File 2: {file2} ({len2} bytes)")
    lines.append("")

    if not diffs and not extra_info:
        lines.append("Files are identical.")
        return lines

    if diffs and not regions_only:
        lines.append(f"Showing up to {max_diffs} byte differences:")
        for offset, v1, v2 in diffs:
            lines.append(f"offset 0x{offset:08X} : 0x{v1:02X} -> 0x{v2:02X}")
        lines.append("")

    if extra_info:
        lines.append(extra_info)

        lines.append("")
        regions = build_changed_regions(diffs)

        regions = [
            (start, end)
            for start, end in regions
            if (end - start + 1) >= min_region_size
        ]

        lines.extend(format_changed_regions(regions))

        lines.append("")
        lines.extend(format_region_summary(regions))

    return lines


def compare_directories(dir1, dir2):
    dcmp = filecmp.dircmp(dir1, dir2)
    lines = []
    lines.append("Directory diff result")
    lines.append(f"Dir 1: {dir1}")
    lines.append(f"Dir 2: {dir2}")
    lines.append("")

    summary = {
        "left_only": 0,
        "right_only": 0,
        "diff_files": 0,
        "same_files": 0,
    }

    def walk_diff(dcmp_obj, rel_path=""):
        current = rel_path if rel_path else "."

        lines.append(f"[{current}]")

        if dcmp_obj.left_only:
            lines.append("  Only in dir1:")
            for name in dcmp_obj.left_only:
                lines.append(f"    {name}")
            summary["left_only"] += len(dcmp_obj.left_only)

        if dcmp_obj.right_only:
            lines.append("  Only in dir2:")
            for name in dcmp_obj.right_only:
                lines.append(f"    {name}")
            summary["right_only"] += len(dcmp_obj.right_only)

        if dcmp_obj.diff_files:
            lines.append("  Changed files:")
            for name in dcmp_obj.diff_files:
                lines.append(f"    {name}")
            summary["diff_files"] += len(dcmp_obj.diff_files)

        if dcmp_obj.same_files:
            lines.append("  Identical files:")
            for name in dcmp_obj.same_files:
                lines.append(f"    {name}")
            summary["same_files"] += len(dcmp_obj.same_files)

        if (not dcmp_obj.left_only and not dcmp_obj.right_only and
                not dcmp_obj.diff_files and not dcmp_obj.same_files):
            lines.append("  No file differences found.")

        lines.append("")

        for subdir_name, sub_dcmp in dcmp_obj.subdirs.items():
            sub_rel_path = f"{rel_path}/{subdir_name}" if rel_path else subdir_name
            walk_diff(sub_dcmp, sub_rel_path)

    walk_diff(dcmp)

    lines.append("Summary")
    lines.append(f"  only in dir1   : {summary['left_only']}")
    lines.append(f"  only in dir2   : {summary['right_only']}")
    lines.append(f"  changed files  : {summary['diff_files']}")
    lines.append(f"  identical files: {summary['same_files']}")

    return lines


def save_or_print(lines, output_file=None, saved_message="Result saved to"):
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + '\n')
        print(f"{saved_message}: {output_file}")
    else:
        for line in lines:
            print(line)


def parse_args():
    description = """Firmware Diff Tool

Compare text files, binary files, and directories from the command line.

Modes:
  text  Compare two text files and output unified diff
  bin   Compare two binary files and show byte differences / regions
  dir   Compare two directories and list changed / added / removed files
"""

    epilog = """Examples:
  python main.py -h
  python main.py text file1.txt file2.txt
  python main.py text file1.txt file2.txt result.diff
  python main.py bin old.bin new.bin
  python main.py bin old.bin new.bin result.txt
  python main.py bin old.bin new.bin --json
  python main.py bin old.bin new.bin --ignore-ff --ignore-00
  python main.py bin old.bin new.bin --regions-only --min-region-size 16
  python main.py bin old.bin new.bin --fail-if-different
  python main.py dir dirA dirB
  python main.py dir dirA dirB dir_result.txt

Tip:
  Use 'python main.py <mode> -h' for mode-specific help.
  Examples:
    python main.py text -h
    python main.py bin -h
    python main.py dir -h
"""

    parser = argparse.ArgumentParser(
        prog="main.py",
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        dest="mode",
        required=True,
        title="modes",
        metavar="{text,bin,dir}",
        help="Available comparison modes. Use '<mode> -h' for more details.",
    )

    # -------------------------
    # text mode
    # -------------------------
    parser_text = subparsers.add_parser(
        "text",
        help="Compare two text files",
        description="""Text mode

Compare two text files and output unified diff to screen or file.
""",
        epilog="""Examples:
  python main.py text old.txt new.txt
  python main.py text old.txt new.txt result.diff
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser_text.add_argument("file1", help="Path to first text file")
    parser_text.add_argument("file2", help="Path to second text file")
    parser_text.add_argument(
        "output_file",
        nargs="?",
        help="Optional output file to save diff result",
    )


    # -------------------------
    # binary mode
    # -------------------------
    parser_bin = subparsers.add_parser(
        "bin",
        help="Compare two binary files",
        description="""Binary mode

Compare two binary files and show byte differences, changed regions, or JSON output.
""",
        epilog="""Examples:
  python main.py bin old.bin new.bin
  python main.py bin old.bin new.bin result.txt
  python main.py bin old.bin new.bin --json
  python main.py bin old.bin new.bin --ignore-ff --ignore-00
  python main.py bin old.bin new.bin --regions-only --min-region-size 16
  python main.py bin old.bin new.bin --fail-if-different
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser_bin.add_argument("file1", help="Path to first binary file")
    parser_bin.add_argument("file2", help="Path to second binary file")
    parser_bin.add_argument(
        "output_file",
        nargs="?",
        help="Optional output file to save result",
    )

    parser_bin.add_argument(
        "--fail-if-different", 
        action="store_true",
        help="Exit with code 1 if any difference is found"
    )
    parser_bin.add_argument(
        "--ignore-ff", 
        action="store_true",
        help="Ignore differences where either byte is 0xFF"
    )
    parser_bin.add_argument(
        "--ignore-00", 
        action="store_true",
        help="Ignore differences where either byte is 0x00"
    )
    parser_bin.add_argument(
        "--max-diffs", 
        type=int, 
        default=100,
        help="Maximum number of differences to record (default: 100)"
    )
    parser_bin.add_argument(
        "--regions-only", 
        action="store_true",
        help="Show only changed regions (hide per-byte diffs)"
    )
    parser_bin.add_argument(
        "--json", 
        action="store_true",
        help="Output result in JSON format"
    )
    parser_bin.add_argument(
        "--quiet", 
        action="store_true",
        help="Suppress console output"
    )
    parser_bin.add_argument(
        "--min-region-size", 
        type=int, 
        default=1,
        help="Only show regions >= this size (default: 1)"
    )


    # -------------------------
    # directory mode
    # -------------------------
    parser_dir = subparsers.add_parser(
        "dir",
        help="Compare two directories",
        description="""Directory mode

Compare two directories and list added, removed, changed, and identical files.
""",
        epilog="""Examples:
  python main.py dir dirA dirB
  python main.py dir dirA dirB dir_result.txt
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser_dir.add_argument("dir1", help="Path to first directory")
    parser_dir.add_argument("dir2", help="Path to second directory")
    parser_dir.add_argument(
        "output_file",
        nargs="?",
        help="Optional output file to save result",
    )

    return parser.parse_args()


def build_binary_json_result(file1, file2, diffs, extra_info, len1, len2):
    regions = build_changed_regions(diffs)
    region_sizes = [end - start + 1 for start, end in regions]

    return {
        "mode": "bin",
        "file1": file1,
        "file2": file2,
        "len1": len1,
        "len2": len2,
        "diffs": [
            {
                "offset": offset,
                "from": v1,
                "to": v2
            }
            for offset, v1, v2 in diffs
        ],
        "regions": [
            {
                "start": start,
                "end": end,
                "size": end - start + 1
            }
            for start, end in regions
        ],
        "region_summary": {
            "total_changed_bytes": sum(region_sizes) if region_sizes else 0,
            "total_regions": len(regions),
            "largest_region_size": max(region_sizes) if region_sizes else 0
        },
        "extra_info": extra_info
    }


def format_region_summary(regions):
    lines = []
    lines.append("Region summary:")

    if not regions:
        lines.append("  total changed bytes : 0")
        lines.append("  total regions       : 0")
        lines.append("  largest region size : 0 bytes")
        return lines

    sizes = [end - start + 1 for start, end in regions]
    total_changed_bytes = sum(sizes)
    total_regions = len(regions)
    largest_region = max(sizes)

    lines.append(f"  total changed bytes : {total_changed_bytes}")
    lines.append(f"  total regions       : {total_regions}")
    lines.append(f"  largest region size : {largest_region} bytes")

    return lines


def check_file_exists(path):
    p = Path(path)
    if not p.exists():
        print(f"Error: file not found: {path}")
        sys.exit(1)
    if not p.is_file():
        print(f"Error: not a file: {path}")
        sys.exit(1)


def check_dir_exists(path):
    p = Path(path)
    if not p.exists():
        print(f"Error: directory not found: {path}")
        sys.exit(1)
    if not p.is_dir():
        print(f"Error: not a directory: {path}")
        sys.exit(1)


def check_parent_dir_for_output(path):
    p = Path(path)
    parent = p.parent
    if str(parent) and str(parent) != "." and not parent.exists():
        print(f"Error: output directory not found: {parent}")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()

    if args.mode == "text":
        check_file_exists(args.file1)
        check_file_exists(args.file2)

        if args.output_file:
            check_parent_dir_for_output(args.output_file)

        diff = list(diff_text_files(args.file1, args.file2))

        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                for line in diff:
                    f.write(line + '\n')
            print(f"Diff result saved to: {args.output_file}")
        else:
            for line in diff:
                print(line)

    elif args.mode == "bin":
        check_file_exists(args.file1)
        check_file_exists(args.file2)

        if args.output_file:
            check_parent_dir_for_output(args.output_file)

        max_diffs = args.max_diffs
        if max_diffs <= 0:
            print("Error: --max-diffs must be greater than 0")
            sys.exit(1)

        if args.min_region_size <= 0:
            print("Error: --min-region-size must be greater than 0")
            sys.exit(1)

        diffs, extra_info, len1, len2 = diff_binary_files(
            args.file1,
            args.file2,
            max_diffs,
            ignore_ff=args.ignore_ff,
            ignore_00=args.ignore_00
        )

        if args.json:
            result = build_binary_json_result(
                args.file1,
                args.file2,
                diffs,
                extra_info,
                len1,
                len2
            )

            json_text = json.dumps(result, indent=2)

            if args.output_file:
                with open(args.output_file, "w", encoding="utf-8") as f:
                    f.write(json_text + "\n")
                if not args.quiet:
                    print(f"Binary JSON result saved to: {args.output_file}")
            else:
                if not args.quiet:
                    print(json_text)
        else:
            lines = format_binary_diff(
                args.file1,
                args.file2,
                diffs,
                extra_info,
                len1,
                len2,
                max_diffs,
                regions_only=args.regions_only,
                min_region_size=args.min_region_size
            )

            if args.quiet:
                if args.output_file:
                    with open(args.output_file, 'w', encoding='utf-8') as f:
                        for line in lines:
                            f.write(line + '\n')
            else:
                save_or_print(lines, args.output_file, "Binary diff result saved to")

        has_diff = bool(diffs) or (extra_info is not None)
        if args.fail_if_different and has_diff:
            sys.exit(1)

    elif args.mode == "dir":
        check_dir_exists(args.dir1)
        check_dir_exists(args.dir2)

        if args.output_file:
            check_parent_dir_for_output(args.output_file)

        lines = compare_directories(args.dir1, args.dir2)
        save_or_print(lines, args.output_file, "Directory diff result saved to")

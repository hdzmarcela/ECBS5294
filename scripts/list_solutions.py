#!/usr/bin/env python3
"""
List Solutions Status

This script shows the status of all solutions in the repository:
- Which solutions exist as encrypted ZIPs
- Which solutions exist as unencrypted files (WARNING!)
- Encryption log history

Usage:
    python scripts/list_solutions.py
"""

import os
import glob
from pathlib import Path


def find_solution_files():
    """Find all solution files in the repository."""
    solution_files = []

    # Search for *_solution.ipynb files
    patterns = [
        '**/*_solution.ipynb',
        '**/*_solution.py',
        'assignments/**/*solution*',
    ]

    for pattern in patterns:
        matches = glob.glob(pattern, recursive=True)
        solution_files.extend(matches)

    return sorted(set(solution_files))


def find_encrypted_zips():
    """Find all encrypted ZIP files."""
    zip_files = glob.glob('solutions/solutions-*.zip')
    return sorted(zip_files)


def read_encryption_log():
    """Read the encryption log."""
    log_file = 'solutions/.encryption_log.txt'

    if not os.path.exists(log_file):
        return []

    with open(log_file, 'r') as f:
        return f.readlines()


def format_file_size(size_bytes):
    """Format file size in human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f} KB"
    else:
        return f"{size_bytes/(1024*1024):.1f} MB"


def main():
    print("="*70)
    print("SOLUTIONS STATUS CHECK")
    print("="*70)

    # Find encrypted solutions
    encrypted = find_encrypted_zips()

    print(f"\n📦 Encrypted Solutions (safe to commit): {len(encrypted)}")
    print("-" * 70)

    if encrypted:
        for zip_file in encrypted:
            size = os.path.getsize(zip_file)
            print(f"  ✅ {zip_file} ({format_file_size(size)})")
    else:
        print("  (none found)")

    # Find unencrypted solutions
    unencrypted = find_solution_files()

    print(f"\n⚠️  Unencrypted Solutions (DO NOT COMMIT): {len(unencrypted)}")
    print("-" * 70)

    if unencrypted:
        for solution_file in unencrypted:
            size = os.path.getsize(solution_file)
            print(f"  ❌ {solution_file} ({format_file_size(size)})")
        print(f"\n  ⚠️  WARNING: These files should NOT be committed!")
        print(f"  Run encrypt_solutions.py to create encrypted versions.")
    else:
        print("  ✅ None found (good!)")

    # Show encryption log
    log_entries = read_encryption_log()

    print(f"\n📝 Encryption Log: {len(log_entries)} entries")
    print("-" * 70)

    if log_entries:
        # Show last 10 entries
        for entry in log_entries[-10:]:
            print(f"  {entry.strip()}")
        if len(log_entries) > 10:
            print(f"  ... ({len(log_entries)-10} earlier entries)")
    else:
        print("  (no encryption history)")

    # Summary
    print("\n" + "="*70)

    if unencrypted:
        print("⚠️  ACTION REQUIRED:")
        print("   - Encrypt unencrypted solutions before committing")
        print("   - Or move them outside the repository")
        print(f"\n   Command:")
        print(f"   python scripts/encrypt_solutions.py <file> --password <pwd> --day X --block Y")
    else:
        print("✅ All solutions are encrypted or outside repository")

    print("="*70)


if __name__ == '__main__':
    main()

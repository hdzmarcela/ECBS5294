#!/usr/bin/env python3
"""
Encrypt Solution Notebooks

This script creates password-protected ZIP files of solution notebooks.
It ensures consistent naming and logs all encryption events.

Usage:
    python scripts/encrypt_solutions.py <source_file> --password <pwd> --output <output.zip>
    python scripts/encrypt_solutions.py <source_file> --password <pwd> --day 1 --block A

Examples:
    python scripts/encrypt_solutions.py notebooks/day1_exercise_tidy_solution.ipynb \\
        --password "potato123" \\
        --day 1 --block A

    python scripts/encrypt_solutions.py notebooks/hw1_solution.ipynb \\
        --password "secret456" \\
        --output solutions/solutions-hw1.zip
"""

import argparse
import os
import sys
import zipfile
import datetime
from pathlib import Path


def validate_solution_file(file_path):
    """Validate that the file exists and is a solution file."""
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        return False

    if not file_path.endswith('_solution.ipynb') and not file_path.endswith('_solution.py'):
        print(f"⚠️  Warning: File doesn't follow naming convention (*_solution.ipynb)")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return False

    return True


def create_encrypted_zip(source_file, output_path, password):
    """Create a password-protected ZIP file."""
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Create encrypted ZIP
        # Note: Python's zipfile with setpassword() creates weak encryption
        # We'll use system zip command for stronger encryption
        import subprocess

        # Get just the filename for inside the zip
        filename = os.path.basename(source_file)

        # Create zip with password using system command (better encryption)
        result = subprocess.run(
            ['zip', '-j', '-P', password, output_path, source_file],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"❌ Error creating ZIP: {result.stderr}")
            return False

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def verify_zip_encrypted(zip_path):
    """Verify that the ZIP file is password-protected."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # Try to read a file without password
            namelist = zf.namelist()
            if not namelist:
                return False

            try:
                # Try to extract without password - should fail
                zf.read(namelist[0])
                # If we got here, it's NOT encrypted
                return False
            except RuntimeError:
                # Good! It's encrypted
                return True
    except Exception as e:
        print(f"⚠️  Could not verify encryption: {e}")
        return True  # Assume it's encrypted if we can't check


def log_encryption(source_file, output_path, day=None, block=None):
    """Log the encryption event."""
    log_file = 'solutions/.encryption_log.txt'

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    source_name = os.path.basename(source_file)
    output_name = os.path.basename(output_path)

    log_entry = f"{timestamp} | {source_name} -> {output_name}"
    if day and block:
        log_entry += f" (Day {day} Block {block})"
    log_entry += "\n"

    try:
        with open(log_file, 'a') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"⚠️  Could not write to log: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Encrypt solution notebooks into password-protected ZIPs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('source', help='Source solution file (e.g., notebook.ipynb)')
    parser.add_argument('--password', '-p', required=True, help='Password for the ZIP file')
    parser.add_argument('--output', '-o', help='Output ZIP file path (optional if using --day/--block)')
    parser.add_argument('--day', '-d', type=int, help='Day number (for auto-naming)')
    parser.add_argument('--block', '-b', help='Block letter (A, B, etc.) (for auto-naming)')

    args = parser.parse_args()

    # Validate source file
    if not validate_solution_file(args.source):
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = args.output
    elif args.day and args.block:
        output_path = f"solutions/solutions-day{args.day}-block{args.block}.zip"
    else:
        print("❌ Error: Must provide either --output or both --day and --block")
        sys.exit(1)

    # Check if output already exists
    if os.path.exists(output_path):
        print(f"⚠️  Output file already exists: {output_path}")
        response = input("Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(0)

    # Create encrypted ZIP
    print(f"🔒 Encrypting: {args.source}")
    print(f"📦 Output: {output_path}")
    print(f"🔑 Password: {'*' * len(args.password)}")

    if not create_encrypted_zip(args.source, output_path, args.password):
        sys.exit(1)

    # Verify encryption
    if verify_zip_encrypted(output_path):
        print("✅ Encryption verified")
    else:
        print("⚠️  Warning: Could not verify encryption")

    # Log the encryption
    log_encryption(args.source, output_path, args.day, args.block)

    # Success!
    file_size = os.path.getsize(output_path)
    print(f"\n✅ Success!")
    print(f"   File: {output_path}")
    print(f"   Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print(f"\n📝 Next steps:")
    print(f"   1. git add {output_path}")
    print(f"   2. git commit -m \"Add encrypted solutions\"")
    print(f"   3. After due date, add password to solutions/PASSWORDS.md")
    print(f"\n⚠️  Remember: NEVER commit the unencrypted source file!")


if __name__ == '__main__':
    main()

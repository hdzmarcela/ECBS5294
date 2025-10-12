#!/usr/bin/env python3
"""
Encrypt Solution Notebooks - FOOLPROOF VERSION

This script creates password-protected ZIP files AND automatically documents passwords.
PASSWORDS ARE NEVER LOST because they're written to multiple locations automatically.

Usage:
    python scripts/encrypt_solutions_v2.py <source_file> --password <pwd> --output <output.zip> --description "What this is"
    python scripts/encrypt_solutions_v2.py <source_file> --password <pwd> --day 1 --block A --description "Day 1 exercise"

Examples:
    python scripts/encrypt_solutions_v2.py notebooks/day1_exercise_tidy_solution.ipynb \\
        --password "TidyData2024!" \\
        --day 1 --block A \\
        --description "Day 1 in-class exercise: Tidy data principles"

    python scripts/encrypt_solutions_v2.py notebooks/hw1_solution.ipynb \\
        --password "SQL2024DuckDB!" \\
        --output solutions/solutions-hw1.zip \\
        --description "Homework 1: SQL Foundations with DuckDB"
"""

import argparse
import os
import sys
import zipfile
import datetime
import subprocess
import json
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


def verify_password_works(zip_path, password):
    """Verify that the password actually works by trying to decrypt."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            namelist = zf.namelist()
            if not namelist:
                return False

            # Try to read with the password
            zf.read(namelist[0], pwd=password.encode())
            return True
    except Exception as e:
        print(f"❌ Password verification failed: {e}")
        return False


def update_passwords_md(output_path, password, description, day=None, block=None):
    """AUTOMATICALLY update PASSWORDS.md with the new password."""
    passwords_file = 'solutions/PASSWORDS.md'

    # Create PASSWORDS.md if it doesn't exist
    if not os.path.exists(passwords_file):
        create_passwords_template()

    # Read current content
    with open(passwords_file, 'r') as f:
        content = f.read()

    # Prepare the new entry
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d')
    zip_name = os.path.basename(output_path)

    # Determine the section to add to
    if 'hw' in zip_name.lower():
        # It's a homework
        hw_num = ''.join(filter(str.isdigit, zip_name))
        section_marker = f"### HW{hw_num}:"
        new_entry = f"""
### HW{hw_num}: {description}
- File: `{zip_name}`
- Password: `{password}`
- Created: {timestamp}
- Description: {description}
"""
    elif day and block:
        # It's a day/block exercise
        section_marker = f"### Day {day} Block {block}:"
        new_entry = f"""
### Day {day} Block {block}: {description}
- File: `{zip_name}`
- Password: `{password}`
- Created: {timestamp}
- Description: {description}
"""
    else:
        # Generic entry
        section_marker = f"### {zip_name}:"
        new_entry = f"""
### {zip_name}
- File: `{zip_name}`
- Password: `{password}`
- Created: {timestamp}
- Description: {description}
"""

    # Find where to insert (in the Homework or Exercise section)
    if 'hw' in zip_name.lower():
        insert_marker = "## Homework Solutions"
    else:
        insert_marker = "## In-Class Exercise Solutions"

    # Insert the entry
    if insert_marker in content:
        # Find the position after the section header
        pos = content.find(insert_marker)
        # Find the next line
        next_line = content.find('\n', pos) + 1
        # Insert the new entry
        content = content[:next_line] + new_entry + content[next_line:]
    else:
        # Just append at the end
        content += "\n" + new_entry

    # Write back
    with open(passwords_file, 'w') as f:
        f.write(content)

    print(f"✅ Password documented in {passwords_file}")


def create_passwords_template():
    """Create PASSWORDS.md if it doesn't exist."""
    template = """# Solution Passwords

**⚠️ DO NOT COMMIT THIS FILE TO GIT**

This file is AUTO-UPDATED by encrypt_solutions_v2.py
Passwords are documented immediately when solutions are encrypted.

---

## Homework Solutions

## In-Class Exercise Solutions

---

## Password Release Schedule

- Release passwords on Moodle only after assignment deadlines
- Never share passwords via email or Slack
- Always test decryption before distributing

---

## Backup

This file is backed up to: solutions/.password_backup.json
"""
    os.makedirs('solutions', exist_ok=True)
    with open('solutions/PASSWORDS.md', 'w') as f:
        f.write(template)


def backup_password_to_json(output_path, password, description, day=None, block=None):
    """Create a machine-readable backup of passwords."""
    backup_file = 'solutions/.password_backup.json'

    # Load existing backup
    if os.path.exists(backup_file):
        with open(backup_file, 'r') as f:
            backup = json.load(f)
    else:
        backup = {}

    # Add this password
    zip_name = os.path.basename(output_path)
    backup[zip_name] = {
        'password': password,
        'description': description,
        'created': datetime.datetime.now().isoformat(),
        'day': day,
        'block': block,
        'source_file': output_path
    }

    # Save backup
    with open(backup_file, 'w') as f:
        json.dump(backup, f, indent=2)

    print(f"✅ Password backed up to {backup_file}")


def log_encryption(source_file, output_path, password, day=None, block=None):
    """Log the encryption event WITH PASSWORD."""
    log_file = 'solutions/.encryption_log.txt'

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    source_name = os.path.basename(source_file)
    output_name = os.path.basename(output_path)

    log_entry = f"{timestamp} | {source_name} -> {output_name} | PASSWORD: {password}"
    if day and block:
        log_entry += f" (Day {day} Block {block})"
    log_entry += "\n"

    try:
        with open(log_file, 'a') as f:
            f.write(log_entry)
        print(f"✅ Encryption logged to {log_file}")
    except Exception as e:
        print(f"⚠️  Could not write to log: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='Encrypt solution notebooks AND auto-document passwords (FOOLPROOF)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('source', help='Source solution file (e.g., notebook.ipynb)')
    parser.add_argument('--password', '-p', required=True, help='Password for the ZIP file')
    parser.add_argument('--description', required=True, help='Description of what this solution is for')
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
    print(f"\n🔒 Encrypting: {args.source}")
    print(f"📦 Output: {output_path}")
    print(f"🔑 Password: {args.password}")
    print(f"📝 Description: {args.description}")

    if not create_encrypted_zip(args.source, output_path, args.password):
        sys.exit(1)

    # CRITICAL: Verify the password actually works
    print("\n🔐 Verifying password works...")
    if not verify_password_works(output_path, args.password):
        print("❌ CRITICAL: Password verification failed! Something went wrong.")
        print("Cleaning up failed encryption...")
        os.remove(output_path)
        sys.exit(1)
    print("✅ Password verified - decryption works!")

    # AUTOMATICALLY document the password (NEVER FORGET AGAIN!)
    print("\n📝 Auto-documenting password...")
    update_passwords_md(output_path, args.password, args.description, args.day, args.block)
    backup_password_to_json(output_path, args.password, args.description, args.day, args.block)
    log_encryption(args.source, output_path, args.password, args.day, args.block)

    # Success!
    file_size = os.path.getsize(output_path)
    print(f"\n✅ SUCCESS! EVERYTHING DOCUMENTED AUTOMATICALLY!")
    print(f"   File: {output_path}")
    print(f"   Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print(f"\n📋 Password documented in 3 places:")
    print(f"   1. solutions/PASSWORDS.md (human-readable)")
    print(f"   2. solutions/.password_backup.json (machine-readable)")
    print(f"   3. solutions/.encryption_log.txt (full history)")
    print(f"\n📝 Next steps:")
    print(f"   1. git add {output_path}")
    print(f"   2. git commit -m \"Add encrypted solutions\"")
    print(f"   3. git push")
    print(f"\n✅ Password is SAFE - documented in PASSWORDS.md immediately!")
    print(f"⚠️  Remember: NEVER commit the unencrypted source file!")


if __name__ == '__main__':
    main()

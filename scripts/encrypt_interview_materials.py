#!/usr/bin/env python3
"""
Encrypt Interview Materials - Directory-based Encryption

This script encrypts an entire directory of interview materials into ONE
password-protected ZIP file and automatically documents the password.

Usage:
    python scripts/encrypt_interview_materials.py \\
        --directory interviews/scenario_1_ecommerce \\
        --password "YourPassword123" \\
        --output solutions/interview-materials.zip \\
        --description "SQL Interview Simulation Materials"

Or encrypt all scenarios at once:
    python scripts/encrypt_interview_materials.py \\
        --directory interviews \\
        --exclude-patterns "README.md,STUDENT_*,student_prep*,google_sheet*" \\
        --password "YourPassword123" \\
        --output solutions/interview-materials.zip \\
        --description "SQL Interview Simulation Materials (All 3 Scenarios)"

The script will:
1. Create password-protected ZIP with all files
2. Auto-document password in solutions/PASSWORDS.md
3. Auto-backup password in solutions/.password_backup.json
4. Log encryption event
5. **REMIND YOU TO EMAIL YOURSELF THE PASSWORD**
"""

import argparse
import os
import sys
import zipfile
import datetime
import subprocess
import json
from pathlib import Path


def should_exclude(file_path, exclude_patterns):
    """Check if file matches any exclude pattern."""
    if not exclude_patterns:
        return False

    filename = os.path.basename(file_path)
    for pattern in exclude_patterns:
        if pattern in filename:
            return True
    return False


def create_encrypted_zip_from_directory(directory, output_path, password, exclude_patterns=None):
    """Create a password-protected ZIP file from an entire directory."""
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Remove output file if it exists
        if os.path.exists(output_path):
            os.remove(output_path)

        # Build list of files to include
        files_to_zip = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)

                # Skip excluded files
                if should_exclude(file_path, exclude_patterns):
                    print(f"  ⏭️  Skipping: {file_path}")
                    continue

                files_to_zip.append(file_path)

        if not files_to_zip:
            print(f"❌ Error: No files found in {directory}")
            return False

        print(f"\n📦 Creating encrypted ZIP with {len(files_to_zip)} files...")

        # Create encrypted ZIP using system zip command
        # We'll add files maintaining directory structure
        cmd = ['zip', '-r', '-P', password, output_path] + files_to_zip

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd='.'
        )

        if result.returncode != 0:
            print(f"❌ Error creating ZIP: {result.stderr}")
            return False

        print(f"✅ Created: {output_path}")
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


def update_passwords_md(output_path, password, description):
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

    # Interview materials section
    section_marker = "## Interview Materials"
    new_entry = f"""
### {zip_name}
- File: `{zip_name}`
- Password: `{password}`
- Created: {timestamp}
- Description: {description}
- **⚠️ EMAIL THIS PASSWORD TO YOURSELF NOW!**
"""

    # Insert the entry in Interview Materials section
    if section_marker in content:
        # Find the position after the section header
        pos = content.find(section_marker)
        # Find the next line
        next_line = content.find('\n', pos) + 1
        # Insert the new entry
        content = content[:next_line] + new_entry + content[next_line:]
    else:
        # Add section if it doesn't exist
        content += f"\n{section_marker}\n" + new_entry

    # Write back
    with open(passwords_file, 'w') as f:
        f.write(content)

    print(f"✅ Password documented in {passwords_file}")


def create_passwords_template():
    """Create PASSWORDS.md if it doesn't exist."""
    template = """# Solution Passwords

**⚠️ DO NOT COMMIT THIS FILE TO GIT**

This file is AUTO-UPDATED by encryption scripts.
Passwords are documented immediately when solutions are encrypted.

---

## Homework Solutions

## In-Class Exercise Solutions

## Interview Materials

---

## Password Release Schedule

- Release passwords on Moodle only after assignment deadlines
- Never share passwords via email or Slack
- Always test decryption before distributing

---

## Backup

This file is backed up to: solutions/.password_backup.json
**ALSO: Email all interview/critical passwords to yourself!**
"""
    os.makedirs('solutions', exist_ok=True)
    with open('solutions/PASSWORDS.md', 'w') as f:
        f.write(template)


def backup_password_to_json(output_path, password, description):
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
        'type': 'interview_materials',
        'source_file': output_path
    }

    # Save backup
    with open(backup_file, 'w') as f:
        json.dump(backup, f, indent=2)

    print(f"✅ Password backed up to {backup_file}")


def log_encryption(directory, output_path, password):
    """Log the encryption event WITH PASSWORD."""
    log_file = 'solutions/.encryption_log.txt'

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    output_name = os.path.basename(output_path)

    log_entry = f"{timestamp} | {directory} -> {output_name} | PASSWORD: {password} | TYPE: interview_materials\n"

    try:
        with open(log_file, 'a') as f:
            f.write(log_entry)
        print(f"✅ Encryption logged to {log_file}")
    except Exception as e:
        print(f"⚠️  Could not write to log: {e}")


def print_email_reminder(password, output_path):
    """Print a BIG reminder to email the password."""
    print("\n" + "=" * 70)
    print("📧 EMAIL THIS PASSWORD TO YOURSELF RIGHT NOW!")
    print("=" * 70)
    print()
    print(f"Password: {password}")
    print()
    print("Suggested email:")
    print(f"  To: {os.environ.get('USER', 'yourself')}@ceu.edu")
    print(f"  Subject: ECBS5294 - SQL Interview Materials Password")
    print(f"  Body:")
    print(f"    Password for {os.path.basename(output_path)}: {password}")
    print()
    print("Why email yourself?")
    print("  - Searchable forever")
    print("  - Backed up by email provider")
    print("  - Accessible from any device")
    print("  - Takes 10 seconds")
    print()
    print("=" * 70)
    print()


def main():
    parser = argparse.ArgumentParser(
        description='Encrypt entire directory of interview materials into ONE password-protected ZIP',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('--directory', '-d', required=True,
                        help='Directory to encrypt (e.g., interviews/)')
    parser.add_argument('--password', '-p', required=True,
                        help='Password for the ZIP file')
    parser.add_argument('--output', '-o', required=True,
                        help='Output ZIP file path (e.g., solutions/interview-materials.zip)')
    parser.add_argument('--description', required=True,
                        help='Description of what this is for')
    parser.add_argument('--exclude-patterns', '-e',
                        help='Comma-separated patterns to exclude (e.g., "README.md,*.txt")')

    args = parser.parse_args()

    # Validate directory exists
    if not os.path.exists(args.directory):
        print(f"❌ Error: Directory not found: {args.directory}")
        sys.exit(1)

    if not os.path.isdir(args.directory):
        print(f"❌ Error: Not a directory: {args.directory}")
        sys.exit(1)

    # Parse exclude patterns
    exclude_patterns = None
    if args.exclude_patterns:
        exclude_patterns = [p.strip() for p in args.exclude_patterns.split(',')]
        print(f"📋 Exclude patterns: {exclude_patterns}")

    # Check if output already exists
    if os.path.exists(args.output):
        print(f"⚠️  Output file already exists: {args.output}")
        response = input("Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(0)

    # Create encrypted ZIP
    print(f"\n🔒 Encrypting directory: {args.directory}")
    print(f"📦 Output: {args.output}")
    print(f"🔑 Password: {args.password}")
    print(f"📝 Description: {args.description}")

    if not create_encrypted_zip_from_directory(
        args.directory, args.output, args.password, exclude_patterns
    ):
        sys.exit(1)

    # CRITICAL: Verify the password actually works
    print("\n🔐 Verifying password works...")
    if not verify_password_works(args.output, args.password):
        print("❌ CRITICAL: Password verification failed! Something went wrong.")
        print("Cleaning up failed encryption...")
        os.remove(args.output)
        sys.exit(1)
    print("✅ Password verified - decryption works!")

    # AUTOMATICALLY document the password (NEVER FORGET AGAIN!)
    print("\n📝 Auto-documenting password...")
    update_passwords_md(args.output, args.password, args.description)
    backup_password_to_json(args.output, args.password, args.description)
    log_encryption(args.directory, args.output, args.password)

    # Success!
    file_size = os.path.getsize(args.output)
    file_count = len([f for f in zipfile.ZipFile(args.output).namelist()])

    print(f"\n✅ SUCCESS! {file_count} files encrypted!")
    print(f"   File: {args.output}")
    print(f"   Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print(f"\n📋 Password documented in 3 places:")
    print(f"   1. solutions/PASSWORDS.md (human-readable)")
    print(f"   2. solutions/.password_backup.json (machine-readable)")
    print(f"   3. solutions/.encryption_log.txt (full history)")

    # BIG REMINDER
    print_email_reminder(args.password, args.output)

    print(f"📝 Next steps:")
    print(f"   1. **EMAIL THE PASSWORD TO YOURSELF** (seriously, do it now!)")
    print(f"   2. git add {args.output}")
    print(f"   3. git commit -m \"Add encrypted interview materials\"")
    print(f"   4. git push")
    print(f"\n✅ To decrypt later:")
    print(f"   unzip -P \"{args.password}\" {args.output}")
    print(f"\n⚠️  Remember: NEVER commit unencrypted interview materials!")


if __name__ == '__main__':
    main()

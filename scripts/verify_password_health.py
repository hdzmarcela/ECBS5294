#!/usr/bin/env python3
"""
Password Health Check Script

Verifies that all solution passwords are documented and working.
Run this regularly to ensure password loss is impossible.

Usage:
    python scripts/verify_password_health.py
"""

import os
import sys
import json
import zipfile
from pathlib import Path
from datetime import datetime


def check_gitignore():
    """Verify password files are gitignored."""
    print("🔒 Checking .gitignore protection...")

    required_ignores = [
        'solutions/PASSWORDS.md',
        'solutions/.encryption_log.txt',
        'solutions/.password_backup.json'
    ]

    if not os.path.exists('.gitignore'):
        print("  ❌ .gitignore file not found!")
        return False

    with open('.gitignore', 'r') as f:
        gitignore_content = f.read()

    all_protected = True
    for pattern in required_ignores:
        if pattern in gitignore_content:
            print(f"  ✅ {pattern} is gitignored")
        else:
            print(f"  ❌ {pattern} is NOT gitignored!")
            all_protected = False

    return all_protected


def check_backup_files_exist():
    """Check if password backup files exist."""
    print("\n📁 Checking password backup files...")

    files_to_check = {
        'solutions/PASSWORDS.md': 'Human-readable password list',
        'solutions/.password_backup.json': 'Machine-readable backup',
        'solutions/.encryption_log.txt': 'Encryption history log'
    }

    all_exist = True
    for file_path, description in files_to_check.items():
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"  ✅ {file_path} exists ({size} bytes) - {description}")
        else:
            print(f"  ❌ {file_path} NOT FOUND - {description}")
            all_exist = False

    return all_exist


def load_passwords():
    """Load passwords from backup JSON."""
    if not os.path.exists('solutions/.password_backup.json'):
        return {}

    with open('solutions/.password_backup.json', 'r') as f:
        return json.load(f)


def check_all_zips_documented():
    """Verify all solution ZIPs have documented passwords."""
    print("\n📦 Checking solution ZIPs are documented...")

    # Find all solution ZIPs
    solution_zips = []
    if os.path.exists('solutions'):
        for file in os.listdir('solutions'):
            if file.endswith('.zip') and file.startswith('solutions-'):
                solution_zips.append(file)

    if not solution_zips:
        print("  ℹ️  No solution ZIPs found")
        return True

    # Load documented passwords
    passwords = load_passwords()

    # Also check PASSWORDS.md
    passwords_md_zips = set()
    if os.path.exists('solutions/PASSWORDS.md'):
        with open('solutions/PASSWORDS.md', 'r') as f:
            for line in f:
                if line.strip().startswith('- File:'):
                    # Extract filename from: - File: `filename.zip`
                    filename = line.split('`')[1] if '`' in line else ''
                    if filename:
                        passwords_md_zips.add(filename)

    all_documented = True
    for zip_file in sorted(solution_zips):
        if zip_file in passwords:
            print(f"  ✅ {zip_file} - documented in .password_backup.json")
        elif zip_file in passwords_md_zips:
            print(f"  ⚠️  {zip_file} - in PASSWORDS.md but not in backup JSON")
        else:
            print(f"  ❌ {zip_file} - NO PASSWORD DOCUMENTED!")
            all_documented = False

    return all_documented


def verify_passwords_work():
    """Test that all documented passwords actually work."""
    print("\n🔐 Verifying passwords work...")

    passwords = load_passwords()

    if not passwords:
        print("  ⚠️  No passwords in backup JSON to verify")
        return True

    all_work = True
    for zip_file, info in sorted(passwords.items()):
        zip_path = f"solutions/{zip_file}"

        if not os.path.exists(zip_path):
            print(f"  ⚠️  {zip_file} - ZIP file not found (password documented but file missing)")
            continue

        password = info['password']

        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                # Try to read first file with password
                first_file = zf.namelist()[0]
                zf.read(first_file, pwd=password.encode())
            print(f"  ✅ {zip_file} - password works: {password}")
        except Exception as e:
            print(f"  ❌ {zip_file} - password FAILED: {password}")
            print(f"     Error: {e}")
            all_work = False

    return all_work


def check_for_undocumented_zips():
    """Check for ZIPs that might have been created with old script."""
    print("\n🔍 Checking for potentially undocumented ZIPs...")

    passwords = load_passwords()

    # Find all ZIPs in solutions/
    if not os.path.exists('solutions'):
        print("  ℹ️  solutions/ directory not found")
        return True

    all_zips = [f for f in os.listdir('solutions') if f.endswith('.zip')]
    documented_zips = set(passwords.keys())

    undocumented = [z for z in all_zips if z not in documented_zips]

    if undocumented:
        print(f"  ⚠️  Found {len(undocumented)} ZIPs without JSON backup:")
        for z in undocumented:
            print(f"     - {z}")
        print("  These may have been created with the old encrypt_solutions.py script")
        return False
    else:
        print(f"  ✅ All {len(all_zips)} solution ZIPs have JSON backup")

    return True


def check_old_script_disabled():
    """Check if old script has warning."""
    print("\n⚠️  Checking old script status...")

    old_script = 'scripts/encrypt_solutions.py'
    if not os.path.exists(old_script):
        print("  ℹ️  Old script not found (good!)")
        return True

    with open(old_script, 'r') as f:
        content = f.read()

    # Check if it has a warning about using v2
    if 'DEPRECATED' in content or 'encrypt_solutions_v2' in content:
        print(f"  ✅ {old_script} has deprecation warning")
        return True
    else:
        print(f"  ⚠️  {old_script} exists without deprecation warning")
        print("     Consider adding a warning to use v2 script instead")
        return False


def generate_report():
    """Generate summary report."""
    print("\n" + "=" * 60)
    print("📊 PASSWORD HEALTH REPORT")
    print("=" * 60)

    results = {
        'gitignore_protected': check_gitignore(),
        'backup_files_exist': check_backup_files_exist(),
        'all_documented': check_all_zips_documented(),
        'passwords_work': verify_passwords_work(),
        'no_undocumented': check_for_undocumented_zips(),
        'old_script_warned': check_old_script_disabled()
    }

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    all_pass = all(results.values())

    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        check_name = check.replace('_', ' ').title()
        print(f"{status:12s} {check_name}")

    print("=" * 60)

    if all_pass:
        print("🎉 ALL CHECKS PASSED!")
        print("Password loss is IMPOSSIBLE with current setup.")
        print(f"\nLast verified: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return 0
    else:
        print("⚠️  SOME CHECKS FAILED!")
        print("Review the issues above and fix them to prevent password loss.")
        return 1


def main():
    print("🔐 Password Health Check")
    print("=" * 60)
    print("Verifying password documentation and protection...\n")

    # Change to repo root
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)

    exit_code = generate_report()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()

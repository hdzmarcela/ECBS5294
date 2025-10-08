#!/usr/bin/env python3
"""
Clear Jupyter Notebook Outputs

This script removes all output cells from Jupyter notebooks while preserving
code and markdown content. Useful for keeping teaching materials clean and
ensuring students run notebooks themselves.

Usage:
    python scripts/clear_notebook_outputs.py <notebook.ipynb>
    python scripts/clear_notebook_outputs.py notebooks/*.ipynb
    python scripts/clear_notebook_outputs.py --all

Examples:
    # Clear single notebook
    python scripts/clear_notebook_outputs.py notebooks/day1_setup_check.ipynb

    # Clear multiple notebooks
    python scripts/clear_notebook_outputs.py notebooks/*.ipynb

    # Clear all teaching notebooks (excludes solutions)
    python scripts/clear_notebook_outputs.py --all

    # Dry run (show what would be cleared)
    python scripts/clear_notebook_outputs.py --all --dry-run
"""

import argparse
import json
import os
import sys
from pathlib import Path


def is_solution_notebook(file_path):
    """Check if this is a solution notebook (which we should skip)."""
    path_str = str(file_path).lower()
    return (
        '_solution' in path_str or
        '/solution' in path_str or
        'solutions/' in path_str
    )


def clear_notebook_outputs(notebook_path, dry_run=False):
    """
    Clear all outputs from a Jupyter notebook.

    Args:
        notebook_path: Path to the notebook file
        dry_run: If True, don't write changes, just report what would happen

    Returns:
        True if outputs were cleared, False if no outputs found or error
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {notebook_path}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading {notebook_path}: {e}")
        return False

    # Check notebook structure
    if 'cells' not in notebook:
        print(f"⚠️  Warning: {notebook_path} doesn't have 'cells' key (not a notebook?)")
        return False

    # Count outputs before clearing
    output_count = 0
    execution_count_found = False

    for cell in notebook['cells']:
        # Code cells have outputs and execution_count
        if cell.get('cell_type') == 'code':
            if cell.get('outputs'):
                output_count += len(cell['outputs'])
            if cell.get('execution_count') is not None:
                execution_count_found = True

    # If no outputs found, skip
    if output_count == 0 and not execution_count_found:
        return None

    # Clear outputs from code cells
    for cell in notebook['cells']:
        if cell.get('cell_type') == 'code':
            cell['outputs'] = []
            cell['execution_count'] = None

    # Reset notebook metadata execution count
    if 'metadata' in notebook:
        if 'language_info' in notebook['metadata']:
            # Keep language_info but clear version-specific details
            pass
        if 'kernelspec' in notebook['metadata']:
            # Keep kernelspec but clear session details
            pass

    if dry_run:
        print(f"🔍 Would clear {output_count} outputs from {notebook_path}")
        return True

    # Write back to file
    try:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
            f.write('\n')  # Add trailing newline

        print(f"✅ Cleared {output_count} outputs from {notebook_path}")
        return True

    except Exception as e:
        print(f"❌ Error writing {notebook_path}: {e}")
        return False


def find_all_notebooks(exclude_solutions=True):
    """
    Find all notebooks in the repository.

    Args:
        exclude_solutions: If True, skip solution notebooks

    Returns:
        List of Path objects for notebooks
    """
    repo_root = Path(__file__).parent.parent
    notebooks = []

    # Search in common directories
    search_dirs = [
        repo_root / 'notebooks',
        repo_root / 'assignments',
    ]

    for search_dir in search_dirs:
        if search_dir.exists():
            for notebook in search_dir.rglob('*.ipynb'):
                # Skip checkpoint files
                if '.ipynb_checkpoints' in str(notebook):
                    continue

                # Skip solution notebooks if requested
                if exclude_solutions and is_solution_notebook(notebook):
                    continue

                notebooks.append(notebook)

    return sorted(notebooks)


def main():
    parser = argparse.ArgumentParser(
        description="Clear outputs from Jupyter notebooks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        'notebooks',
        nargs='*',
        help='Notebook files to clear (or use --all)'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Clear all teaching notebooks (excludes solutions)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be cleared without making changes'
    )

    parser.add_argument(
        '--include-solutions',
        action='store_true',
        help='Include solution notebooks (use with caution!)'
    )

    args = parser.parse_args()

    # Determine which notebooks to process
    notebooks_to_process = []

    if args.all:
        print("🔍 Finding all teaching notebooks...")
        notebooks_to_process = find_all_notebooks(
            exclude_solutions=not args.include_solutions
        )
        print(f"📚 Found {len(notebooks_to_process)} notebooks")
    elif args.notebooks:
        # Use provided notebook paths
        for notebook_pattern in args.notebooks:
            path = Path(notebook_pattern)
            if path.exists():
                notebooks_to_process.append(path)
            else:
                print(f"⚠️  Warning: {notebook_pattern} not found")
    else:
        parser.print_help()
        print("\n❌ Error: Provide notebook files or use --all")
        return 1

    if not notebooks_to_process:
        print("❌ No notebooks to process")
        return 1

    # Filter out solution notebooks if not explicitly included
    if not args.include_solutions:
        original_count = len(notebooks_to_process)
        notebooks_to_process = [
            nb for nb in notebooks_to_process
            if not is_solution_notebook(nb)
        ]
        if len(notebooks_to_process) < original_count:
            skipped = original_count - len(notebooks_to_process)
            print(f"⏭️  Skipped {skipped} solution notebook(s)")

    # Process each notebook
    print("")
    cleared_count = 0
    skipped_count = 0
    error_count = 0

    for notebook in notebooks_to_process:
        result = clear_notebook_outputs(notebook, dry_run=args.dry_run)
        if result is True:
            cleared_count += 1
        elif result is False:
            error_count += 1
        elif result is None:
            skipped_count += 1

    # Summary
    print("")
    if args.dry_run:
        print(f"🔍 Dry run complete:")
        print(f"   Would clear: {cleared_count}")
        print(f"   Would skip: {skipped_count} (no outputs)")
        if error_count > 0:
            print(f"   Errors: {error_count}")
    else:
        print(f"✅ Done:")
        print(f"   Cleared: {cleared_count}")
        print(f"   Skipped: {skipped_count} (no outputs)")
        if error_count > 0:
            print(f"   Errors: {error_count}")
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())

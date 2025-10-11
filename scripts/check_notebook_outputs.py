#!/usr/bin/env python3
"""
Check Notebook Outputs - Verify executed notebooks for teaching quality

This script inspects EXECUTED Jupyter notebooks and reports:
- Empty DataFrames (0 rows) that would confuse students
- Code cells without outputs (likely didn't execute)
- Execution errors
- Summary statistics

Usage:
    python scripts/check_notebook_outputs.py notebooks/day1_block_a.ipynb
    python scripts/check_notebook_outputs.py notebooks/day*_block_*.ipynb

Exit codes:
    0 - All notebooks clean (all queries return data)
    1 - Issues found (empty results, missing outputs, errors)
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any
import argparse


class NotebookInspector:
    def __init__(self, notebook_path: str):
        self.path = Path(notebook_path)
        self.notebook = self._load_notebook()
        self.issues = []

    def _load_notebook(self) -> Dict[str, Any]:
        """Load notebook JSON"""
        with open(self.path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def inspect(self) -> Dict[str, Any]:
        """Run all inspections and return report"""
        cells = self.notebook.get('cells', [])

        code_cells = [c for c in cells if c.get('cell_type') == 'code']
        cells_with_outputs = []
        cells_without_outputs = []
        empty_result_cells = []
        error_cells = []

        for idx, cell in enumerate(cells):
            if cell.get('cell_type') != 'code':
                continue

            cell_id = cell.get('id', f'cell-{idx}')
            outputs = cell.get('outputs', [])
            source = ''.join(cell.get('source', []))

            # Check for outputs
            if not outputs:
                # Skip if cell is just a comment or whitespace
                if source.strip() and not source.strip().startswith('#'):
                    cells_without_outputs.append({
                        'index': idx,
                        'id': cell_id,
                        'source_preview': source[:100].strip()
                    })
                continue

            cells_with_outputs.append(cell_id)

            # Check for errors
            for output in outputs:
                if output.get('output_type') == 'error':
                    error_cells.append({
                        'index': idx,
                        'id': cell_id,
                        'error_name': output.get('ename', 'Unknown'),
                        'error_value': output.get('evalue', 'No message'),
                        'source_preview': source[:100].strip()
                    })

            # Check for empty DataFrames
            for output in outputs:
                if output.get('output_type') in ['execute_result', 'display_data']:
                    data = output.get('data', {})
                    text_plain = data.get('text/plain', '')

                    # Convert list to string if needed
                    if isinstance(text_plain, list):
                        text_plain = ''.join(text_plain)

                    # Check for empty results
                    if ('Empty DataFrame' in text_plain or
                        '[0 rows' in text_plain or
                        'shape: (0,' in text_plain):
                        empty_result_cells.append({
                            'index': idx,
                            'id': cell_id,
                            'output_preview': text_plain[:200],
                            'source_preview': source[:100].strip()
                        })

        return {
            'notebook_path': str(self.path),
            'total_code_cells': len(code_cells),
            'cells_with_outputs': len(cells_with_outputs),
            'cells_without_outputs': len(cells_without_outputs),
            'empty_result_cells': len(empty_result_cells),
            'error_cells': len(error_cells),
            'issues': {
                'no_output': cells_without_outputs,
                'empty_results': empty_result_cells,
                'errors': error_cells
            }
        }

    def print_report(self, report: Dict[str, Any], verbose: bool = False):
        """Print human-readable report"""
        print(f"\n{'='*70}")
        print(f"📊 Notebook: {self.path.name}")
        print(f"{'='*70}")
        print(f"  Total code cells: {report['total_code_cells']}")
        print(f"  Cells with outputs: {report['cells_with_outputs']}")
        print(f"  Cells without outputs: {report['cells_without_outputs']}")
        print(f"  Cells with empty results: {report['empty_result_cells']}")
        print(f"  Cells with errors: {report['error_cells']}")

        has_issues = (report['cells_without_outputs'] > 0 or
                     report['empty_result_cells'] > 0 or
                     report['error_cells'] > 0)

        if not has_issues:
            print(f"\n✅ CLEAN: All queries return data, no errors!")
            return True

        # Report issues
        print(f"\n{'⚠️ ISSUES FOUND':-^70}")

        if report['issues']['errors']:
            print(f"\n🚨 EXECUTION ERRORS ({len(report['issues']['errors'])}):")
            for err in report['issues']['errors']:
                print(f"\n  Cell {err['index']} ({err['id']}):")
                print(f"    Error: {err['error_name']}: {err['error_value']}")
                if verbose:
                    print(f"    Source: {err['source_preview']}")

        if report['issues']['empty_results']:
            print(f"\n🚨 EMPTY RESULTS ({len(report['issues']['empty_results'])}):")
            print("    (Students will think THEY made a mistake!)")
            for empty in report['issues']['empty_results']:
                print(f"\n  Cell {empty['index']} ({empty['id']}):")
                if verbose:
                    print(f"    Source: {empty['source_preview']}")
                    print(f"    Output: {empty['output_preview']}")

        if report['issues']['no_output']:
            print(f"\n⚠️ CELLS WITHOUT OUTPUT ({len(report['issues']['no_output'])}):")
            print("    (May not have been executed)")
            for no_out in report['issues']['no_output']:
                print(f"\n  Cell {no_out['index']} ({no_out['id']}):")
                if verbose:
                    print(f"    Source: {no_out['source_preview']}")

        print(f"\n{'='*70}\n")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Check executed Jupyter notebooks for teaching quality issues'
    )
    parser.add_argument(
        'notebooks',
        nargs='+',
        help='Notebook file(s) to check'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed output (source code, full errors)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )

    args = parser.parse_args()

    all_clean = True
    all_reports = []

    for notebook_path in args.notebooks:
        path = Path(notebook_path)

        if not path.exists():
            print(f"❌ ERROR: Notebook not found: {notebook_path}", file=sys.stderr)
            all_clean = False
            continue

        try:
            inspector = NotebookInspector(notebook_path)
            report = inspector.inspect()
            all_reports.append(report)

            if not args.json:
                clean = inspector.print_report(report, verbose=args.verbose)
                if not clean:
                    all_clean = False

        except Exception as e:
            print(f"❌ ERROR inspecting {notebook_path}: {e}", file=sys.stderr)
            all_clean = False

    # JSON output
    if args.json:
        import json
        print(json.dumps(all_reports, indent=2))
        # Check if any have issues
        for report in all_reports:
            if (report['cells_without_outputs'] > 0 or
                report['empty_result_cells'] > 0 or
                report['error_cells'] > 0):
                all_clean = False

    # Summary for multiple notebooks
    if len(args.notebooks) > 1 and not args.json:
        total_cells = sum(r['total_code_cells'] for r in all_reports)
        total_empty = sum(r['empty_result_cells'] for r in all_reports)
        total_errors = sum(r['error_cells'] for r in all_reports)

        print(f"\n{'SUMMARY':-^70}")
        print(f"  Notebooks checked: {len(all_reports)}")
        print(f"  Total code cells: {total_cells}")
        print(f"  Total empty results: {total_empty}")
        print(f"  Total errors: {total_errors}")

        if all_clean:
            print(f"\n✅ ALL NOTEBOOKS CLEAN!")
        else:
            print(f"\n⚠️ ISSUES FOUND - See details above")
        print(f"{'='*70}\n")

    sys.exit(0 if all_clean else 1)


if __name__ == '__main__':
    main()

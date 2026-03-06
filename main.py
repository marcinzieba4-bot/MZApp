"""
Pivot Opportunity Framework — CLI entry point

Usage:
  python main.py                  # Run all example analyses
  python main.py --example mirbud # Run specific example
  python main.py --list           # List available examples
"""

import argparse
import sys


EXAMPLES = {
    "mirbud": {
        "module": "examples.mirbud_analysis",
        "description": "Mirbud S.A. (WSE: MRB) — Polish construction / asset release play",
    },
    "sp500_inclusion": {
        "module": "examples.sp500_inclusion",
        "description": "S&P 500 inclusion strategy — pre-announcement alpha + momentum screen",
    },
    "msci_wig_inclusion": {
        "module": "examples.msci_wig_inclusion",
        "description": "MSCI inclusion for WIG companies — Polish stocks approaching MSCI thresholds",
    },
    "msci_ftse_candidates": {
        "module": "examples.msci_ftse_candidates_2025",
        "description": "WIG stocks near MSCI/FTSE thresholds + momentum filter + historical backtest",
    },
    "walkforward_backtest": {
        "module": "examples.walkforward_backtest_run",
        "description": "Honest walk-forward MSCI Poland backtest 2018-2026, no look-ahead bias, FP handling",
    },
    "generate_pdf_report": {
        "module": "examples.generate_pdf_report",
        "description": "Generate PDF trade log + performance report for the walk-forward backtest",
    },
    "candidates_2026": {
        "module": "examples.candidates_2026",
        "description": "2026 MSCI Poland prospective trade candidates with momentum filter",
    },
    "generate_2026_pdf": {
        "module": "examples.generate_2026_pdf",
        "description": "Generate PDF with 2026 MSCI Poland prospective trade ideas",
    },
}


def main():
    parser = argparse.ArgumentParser(
        description="Pivot Opportunity Framework — identify companies at inflection points",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--example", "-e",
        metavar="NAME",
        help="Run a specific example analysis",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available example analyses",
    )
    args = parser.parse_args()

    if args.list:
        print("\nAvailable example analyses:")
        for name, meta in EXAMPLES.items():
            print(f"  {name:20s} {meta['description']}")
        print()
        return

    if args.example:
        if args.example not in EXAMPLES:
            print(f"Unknown example '{args.example}'. Use --list to see options.")
            sys.exit(1)
        _run_example(args.example)
    else:
        # Run all examples
        print("\n=== PIVOT OPPORTUNITY FRAMEWORK ===\n")
        for name in EXAMPLES:
            _run_example(name)


def _run_example(name: str) -> None:
    import importlib
    meta   = EXAMPLES[name]
    module = importlib.import_module(meta["module"])
    module.run()


if __name__ == "__main__":
    main()

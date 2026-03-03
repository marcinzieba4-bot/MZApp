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

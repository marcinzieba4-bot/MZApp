"""
Run the honest walk-forward MSCI Poland backtest (2018–Mar 2026).
No look-ahead bias: every decision uses only data observable at screen date (T-45).
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from framework.walkforward_backtest import (
    build_screen_events,
    simulate_portfolio,
    print_walkforward_report,
)


def run() -> None:
    positions = build_screen_events()

    all_stats  = simulate_portfolio(positions, use_momentum_filter=False)
    filt_stats = simulate_portfolio(positions, use_momentum_filter=True)

    print_walkforward_report(positions, all_stats, filt_stats)


if __name__ == "__main__":
    run()

"""One-time patient accumulation + a real-money slippage log (design spec B.6, C.3).

Because the strategy buys once and holds a year, illiquidity is a far smaller
enemy than in active trading: each position is built with passive limit orders
worked over days/weeks rather than crossed at once. ``accumulation_plan`` turns a
sized book into a per-name tranche schedule. ``log_fill`` appends realized fills
to a CSV so paper marks can be compared against actual capture (the C.3 bridge).
"""

from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from datetime import date
from typing import Optional

from ..config import SETTINGS, Settings
from .sizing import Position

_SLIPPAGE_HEADER = [
    "date", "ticker", "side", "target_price", "fill_price",
    "shares", "dollars", "slippage_bps", "note",
]


@dataclass
class Tranche:
    ticker: str
    shares: int
    limit_price: float
    day_offset: int  # trading-day offset from accumulation start

    def to_dict(self) -> dict:
        return {
            "ticker": self.ticker,
            "shares": self.shares,
            "limit_price": round(self.limit_price, 4),
            "day_offset": self.day_offset,
        }


def accumulation_plan(
    positions: list[Position],
    tranches: int = 5,
    limit_discount: float = 0.0,
) -> dict[str, list[Tranche]]:
    """Split each position into ``tranches`` passive child orders over time.

    ``limit_discount`` shaves the limit below the anchor price (e.g. 0.01 = 1%
    below) so orders sit on the bid rather than lift the offer.
    """
    plan: dict[str, list[Tranche]] = {}
    for p in positions:
        if p.shares <= 0:
            continue
        base = p.shares // tranches
        remainder = p.shares - base * tranches
        limit = p.target_price * (1.0 - limit_discount)
        children: list[Tranche] = []
        for i in range(tranches):
            qty = base + (1 if i < remainder else 0)
            if qty <= 0:
                continue
            children.append(Tranche(ticker=p.ticker, shares=qty, limit_price=limit, day_offset=i))
        plan[p.ticker] = children
    return plan


def log_fill(
    ticker: str,
    side: str,
    target_price: float,
    fill_price: float,
    shares: int,
    note: str = "",
    settings: Settings = SETTINGS,
    path: Optional[str] = None,
) -> str:
    """Append a realized fill to the slippage log; returns the file path.

    Slippage is measured in basis points vs the target (limit anchor) price, the
    quantity C.3 exists to calibrate: how much of the paper return survives
    contact with real, thin markets.
    """
    path = path or os.path.join(settings.output_dir, "slippage_log.csv")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    slippage_bps = 0.0
    if target_price:
        slippage_bps = (fill_price - target_price) / target_price * 10_000
    new_file = not os.path.exists(path)
    with open(path, "a", newline="") as fh:
        writer = csv.writer(fh)
        if new_file:
            writer.writerow(_SLIPPAGE_HEADER)
        writer.writerow([
            date.today().isoformat(), ticker, side, round(target_price, 4),
            round(fill_price, 4), shares, round(fill_price * shares, 2),
            round(slippage_bps, 2), note,
        ])
    return path

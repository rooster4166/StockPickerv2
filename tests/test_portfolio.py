"""Ranking, sizing, book assembly, and execution."""

import pytest

from microcap_engine.config import Settings
from microcap_engine.portfolio.build import build_book
from microcap_engine.portfolio.execution import accumulation_plan, log_fill
from microcap_engine.portfolio.ranking import rank_candidates
from microcap_engine.portfolio.sizing import size_book


def _result(ticker, median, confidence=1.0, p_catalyst=0.0):
    return {"ticker": ticker, "action": "analyzed", "confidence": confidence,
            "p_catalyst": p_catalyst,
            "fair_value": {"low": median * 0.8, "median": median, "high": median * 1.2}}


def test_ranking_filters_by_margin_of_safety():
    s = Settings(margin_of_safety=0.30)
    results = [_result("AAA", 14.0), _result("BBB", 5.5)]  # vs price 5: gaps 1.8 and 0.1
    pool = rank_candidates(results, {"AAA": 5.0, "BBB": 5.0}, s)
    assert [c.ticker for c in pool] == ["AAA"]
    assert pool[0].gap == pytest.approx(1.8)


def test_ranking_orders_by_score():
    s = Settings(margin_of_safety=0.30)
    # Same gap, different confidence -> higher confidence ranks first.
    results = [_result("LOW", 10.0, confidence=0.4), _result("HI", 10.0, confidence=0.9)]
    pool = rank_candidates(results, {"LOW": 5.0, "HI": 5.0}, s)
    assert [c.ticker for c in pool] == ["HI", "LOW"]


def test_ranking_skips_dropped_and_no_price():
    s = Settings(margin_of_safety=0.30)
    results = [{"ticker": "DRP", "action": "drop", "fair_value": None},
               _result("NOPX", 10.0)]
    pool = rank_candidates(results, {"NOPX": None}, s)
    assert pool == []


def test_sizing_respects_liquidity_and_position_caps():
    s = Settings(adv_fraction=0.10, max_position_fraction=0.05)
    results = [_result("AAA", 14.0)]
    pool = rank_candidates(results, {"AAA": 5.0}, s)
    # capital 100k -> max_position cap 5k; adv 1M -> liquidity cap 100k
    book = size_book(pool, 100_000, {"AAA": 1_000_000}, s)
    assert book[0].dollars == pytest.approx(5_000)  # max_position binds first
    assert book[0].capped_by == "max_position"


def test_sizing_liquidity_binds_when_tighter():
    s = Settings(adv_fraction=0.10, max_position_fraction=0.50)
    results = [_result("AAA", 14.0)]
    pool = rank_candidates(results, {"AAA": 5.0}, s)
    book = size_book(pool, 100_000, {"AAA": 50_000}, s)  # liquidity cap = 5k
    assert book[0].dollars == pytest.approx(5_000)
    assert book[0].capped_by == "liquidity"


def test_build_book_summary():
    s = Settings(margin_of_safety=0.30, max_position_fraction=0.05)
    results = [_result("AAA", 14.0), _result("BBB", 50.0)]
    book = build_book(results, {"AAA": 5.0, "BBB": 50.0}, {"AAA": 1e6, "BBB": 1e6},
                      100_000, s)
    assert book["n_candidates"] == 1
    assert book["n_positions"] == 1
    assert book["deployed"] <= book["capital"]


def test_accumulation_plan_splits_shares():
    from microcap_engine.portfolio.sizing import Position

    p = Position(ticker="AAA", dollars=5000, weight=0.05, target_price=5.0, shares=1000,
                 capped_by="max_position", score=1.0, gap=1.8, confidence=1.0)
    plan = accumulation_plan([p], tranches=5)
    assert sum(t.shares for t in plan["AAA"]) == 1000
    assert len(plan["AAA"]) == 5


def test_log_fill_writes_csv(tmp_path):
    path = log_fill("AAA", "buy", target_price=5.0, fill_price=5.05, shares=100,
                    path=str(tmp_path / "slip.csv"))
    content = open(path).read()
    assert "AAA" in content and "slippage_bps" in content
    # 5.05 vs 5.00 = +100 bps
    assert "100.0" in content

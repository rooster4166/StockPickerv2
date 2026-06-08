"""Offline tests for the edge pre-screener's deterministic scoring.

Locks the calibration: the complexity-barrier prior, the analyst-count-driven
coverage gap, and the multiplicative edge prior must separate the validated
high-edge archetypes (biotech / quantum / under-covered insurer) from the
low-edge ones (well-covered REIT, simple retail, heavily-covered insurer).
"""

from __future__ import annotations

from microcap_engine.schemas.edge import EdgeSignals
from microcap_engine.screen.complexity import complexity_prior
from microcap_engine.screen.prescreen import coverage_gap, prior_score


def test_complexity_prior_separates_sectors():
    assert complexity_prior("Healthcare", "Biotechnology") >= 0.9
    assert complexity_prior("Technology", "Semiconductors") >= 0.9
    assert complexity_prior("Financial Services", "Insurance - Property & Casualty") >= 0.6
    # well-trodden / efficiently-covered kinds score low even in a mid sector
    assert complexity_prior("Real Estate", "REIT - Mortgage") <= 0.25
    assert complexity_prior("Consumer Cyclical", "Specialty Retail") <= 0.25


def test_coverage_gap_decreases_with_analysts():
    assert coverage_gap(2, 70) > coverage_gap(6, 70) > coverage_gap(13, 150)
    # thin coverage => high gap; heavy coverage => low gap
    assert coverage_gap(2, 70) > 0.7
    assert coverage_gap(14, 200) < 0.15


def _sig(tkr, sector, industry, n_an, n_inst, pre=False, evs=None):
    return EdgeSignals(ticker=tkr, sector=sector, industry=industry, n_analysts=n_an,
                       n_institutions=n_inst, is_pre_revenue=pre, ev_to_sales=evs)


def test_edge_prior_ranks_validation_set():
    # Synthetic signals approximating the real FMP values for the 6 validated names.
    sigs = {
        "ARQQ": _sig("ARQQ", "Technology", "Software - Infrastructure", 2, 69, pre=True, evs=150),
        "ANIX": _sig("ANIX", "Healthcare", "Biotechnology", 6, 67),
        "KINS": _sig("KINS", "Financial Services", "Insurance - Property & Casualty", 4, 106),
        "FLWS": _sig("FLWS", "Consumer Cyclical", "Specialty Retail", 11, 121),
        "ACRE": _sig("ACRE", "Real Estate", "REIT - Mortgage", 13, 150),
        "ROOT": _sig("ROOT", "Financial Services", "Insurance - Property & Casualty", 14, 203),
    }
    scores = {t: prior_score(s).edge_prior for t, s in sigs.items()}
    high = ["ARQQ", "ANIX", "KINS"]
    low = ["FLWS", "ACRE", "ROOT"]
    # every high-edge name outranks every low-edge name with clear separation
    assert min(scores[h] for h in high) > 3 * max(scores[low_t] for low_t in low)

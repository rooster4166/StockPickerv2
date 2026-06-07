"""Shared test fixtures: an offline fake LLM and a fake data provider.

These let the full pipeline run deterministically with no network and no API
key. The FakeLLM inspects the schema/system of each call and returns canned,
internally-consistent outputs; the FakeProvider serves fixture CompanyData.
"""

from __future__ import annotations

import pytest

from microcap_engine.config import Settings
from microcap_engine.data.types import CompanyData, Filing, NewsItem, PriceData


# A DCF assumption set that yields ~$14.46/share at 10M shares (see test math).
_DCF_BASE = {
    "fcf_base_m": 10.0,
    "stage1_growth": 0.05,
    "stage1_years": 5,
    "terminal_growth": 0.02,
    "discount_rate": 0.10,
    "net_debt_m": 0.0,
}
_DCF_BEAR = {**_DCF_BASE, "fcf_base_m": 8.0, "stage1_growth": 0.02, "discount_rate": 0.12}
_DCF_BULL = {**_DCF_BASE, "fcf_base_m": 12.0, "stage1_growth": 0.08, "discount_rate": 0.09}


class FakeLLM:
    """Deterministic stand-in implementing complete / complete_json."""

    def __init__(self, gate_verdict: str = "plausible", gate_confidence: float = 0.9,
                 would_buy: bool = True, baseline_fv: float = 14.46):
        self.gate_verdict = gate_verdict
        self.gate_confidence = gate_confidence
        self.would_buy = would_buy
        self.baseline_fv = baseline_fv
        self.calls: list[str] = []

    def complete(self, *, system, messages, model=None, effort=None,
                 max_tokens=16000, thinking=True, cache_system=True) -> str:
        self.calls.append("complete")
        return "Specialist brief: trends are stable; balance sheet clean; cited to filings."

    def complete_json(self, *, system, messages, schema=None, model=None, effort=None,
                      max_tokens=16000, thinking=True, cache_system=True) -> dict:
        self.calls.append("complete_json")
        props = (schema or {}).get("properties", {}) if schema else {}

        if "verdict" in props and "obvious_no" in str(props.get("verdict", {})):
            return {"verdict": self.gate_verdict, "confidence": self.gate_confidence,
                    "reason": "fixture gate"}
        if "recommended_method" in props:
            return {
                "recommended_method": "dcf",
                "method_rationale": "stable cash generator",
                "assumption_summary": "normalized FCF ~$10M, modest growth",
                "key_drivers": ["FCF", "margins"],
                "financial_quality": "clean",
                "catalyst": {"present": True, "description": "buyback",
                             "probability": 0.4, "within_holding_year": True},
            }
        if "fair_value_adjustment" in props:
            return {"disconfirming_findings": [], "thesis_breakers": [],
                    "fair_value_adjustment": 1.0, "verdict": "thesis_intact",
                    "summary": "fixture red-team"}
        if "would_buy" in props:
            return {"would_buy": self.would_buy, "fair_value_per_share": self.baseline_fv,
                    "confidence": 0.8, "thesis": "fixture baseline"}
        # schema is None -> the valuation phase
        return {
            "method": "dcf",
            "scenario_sets": {"bear": _DCF_BEAR, "base": _DCF_BASE, "bull": _DCF_BULL},
            "valuation_notes": "fixture valuation",
        }


class FakeProvider:
    """Serves fixture CompanyData keyed by ticker, with configurable prices."""

    def __init__(self, prices: dict[str, float], shares: float = 10_000_000.0,
                 adv: float = 1_000_000.0):
        self.prices = prices
        self.shares = shares
        self.adv = adv

    def _price(self, ticker: str) -> PriceData:
        px = self.prices.get(ticker)
        return PriceData(
            ticker=ticker, price=px,
            market_cap=(px * self.shares) if px else None,
            shares_outstanding=self.shares, avg_dollar_volume=self.adv,
        )

    def get_price(self, ticker: str) -> PriceData:
        return self._price(ticker)

    def get_company_data(self, ticker: str) -> CompanyData:
        c = CompanyData(ticker=ticker, name=f"{ticker} Inc", sector="Industrials",
                        industry="Widgets", description="Makes widgets.")
        c.financials = {"income_annual": {"2024-12-31": {"Total Revenue": 100.0}}}
        c.filings = [Filing(form="10-K", filed_date="2025-02-01", text="Annual report text.")]
        c.news = [NewsItem(title="Q4 results", publisher="Wire")]
        c.price = self._price(ticker)
        return c

    def screen_universe(self, tickers=None, limit=None):
        return list(self.prices.keys())[: (limit or len(self.prices))]


@pytest.fixture
def settings():
    # ensemble_n=2 keeps offline tests fast but still exercises blending.
    return Settings(ensemble_n=2)


@pytest.fixture
def fake_llm():
    return FakeLLM()


@pytest.fixture
def fake_provider():
    # A: deeply undervalued (price 5 vs ~14.46 FV). B: overvalued (price 50).
    return FakeProvider(prices={"AAA": 5.0, "BBB": 50.0})

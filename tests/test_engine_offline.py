"""Gate, ensemble, orchestrator, and the full pipeline — offline with fakes."""

import pytest

from microcap_engine.config import Settings
from microcap_engine.engine.ensemble import (
    confidence_from_dispersion,
    ensemble_deepdive,
)
from microcap_engine.engine.gate import cheap_gate, should_drop
from microcap_engine.engine.orchestrator import Orchestrator
from microcap_engine.pipeline import analyze_name, run_pipeline


def test_gate_keeps_plausible(fake_llm, fake_provider, settings):
    company = fake_provider.get_company_data("AAA")
    g = cheap_gate(company, fake_llm, settings)
    assert g["verdict"] == "plausible"
    assert should_drop(g, settings) is False


def test_gate_drops_only_high_confidence_obvious_no(fake_provider, settings):
    from tests.conftest import FakeLLM

    company = fake_provider.get_company_data("AAA")
    # Below the drop threshold -> kept despite obvious_no.
    low = cheap_gate(company, FakeLLM(gate_verdict="obvious_no", gate_confidence=0.6), settings)
    assert should_drop(low, settings) is False
    # At/above threshold -> dropped.
    high = cheap_gate(company, FakeLLM(gate_verdict="obvious_no", gate_confidence=0.95), settings)
    assert should_drop(high, settings) is True


def test_confidence_identical_runs_is_max():
    assert confidence_from_dispersion([14.46, 14.46, 14.46]) == pytest.approx(1.0)


def test_confidence_single_run_is_neutral():
    assert confidence_from_dispersion([14.46]) == pytest.approx(0.5)


def test_orchestrator_produces_price_blinded_fair_value(fake_llm, fake_provider, settings):
    company = fake_provider.get_company_data("AAA")
    result = Orchestrator(company, fake_llm).analyze()
    assert result["method"] == "dcf"
    assert result["fair_value"]["median"] == pytest.approx(14.46, rel=0.03)
    # Red-team adjustment of 1.0 leaves it unchanged.
    assert result["fair_value"]["red_team_adjustment"] == pytest.approx(1.0)


def test_ensemble_blends_and_scores_confidence(fake_llm, fake_provider, settings):
    company = fake_provider.get_company_data("AAA")
    out = ensemble_deepdive(company, fake_llm, n=2, settings=settings)
    assert out["action"] == "analyzed"
    assert out["n_usable"] == 2
    assert out["confidence"] == pytest.approx(1.0)  # identical fixture runs
    assert out["fair_value"]["median"] == pytest.approx(14.46, rel=0.03)


def test_analyze_name_drops_on_obvious_no(fake_provider, settings):
    from tests.conftest import FakeLLM

    company = fake_provider.get_company_data("AAA")
    llm = FakeLLM(gate_verdict="obvious_no", gate_confidence=0.95)
    out = analyze_name(company, llm, settings)
    assert out["action"] == "drop"


def test_full_pipeline_builds_book(fake_llm, fake_provider, settings):
    out = run_pipeline(["AAA", "BBB"], fake_provider, fake_llm, capital=100_000,
                       mode="heavy", settings=settings)
    book = out["book"]
    # AAA undervalued (5 vs ~14.46), BBB overvalued (50) -> exactly one position.
    assert book["n_candidates"] == 1
    assert book["positions"][0]["ticker"] == "AAA"
    assert book["deployed"] <= book["capital"]


def test_baseline_pipeline_builds_book(fake_llm, fake_provider, settings):
    out = run_pipeline(["AAA", "BBB"], fake_provider, fake_llm, capital=100_000,
                       mode="baseline", settings=settings)
    assert out["mode"] == "baseline"
    assert out["book"]["n_candidates"] == 1
    assert out["book"]["positions"][0]["ticker"] == "AAA"

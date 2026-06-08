"""The consolidation gate.

``AssumptionSet`` is the single grounded object the PM produces by fusing all four
phase briefs. It is the *code-enforced* gate: a valuation engine accepts only a
typed assumption block, and the block can only be reached through a validated
``AssumptionSet``. There is no path to a fair value that bypasses this object.

Judgment lives here (the LLM picks the method and fills the numbers); the
arithmetic that turns these into a fair value lives in ``valuation/engines/``.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from microcap_engine.schemas.briefs import Citation


class ValuationMethod(str, Enum):
    DCF = "dcf"
    RNPV = "rnpv"
    NAV = "nav"
    COMPS = "comps"
    EXCESS_RETURNS = "excess_returns"  # book x warranted return multiple (insurers/banks)
    WORKED = "worked"  # any framework: key_inputs + a formula, evaluated in code
    COMPOSITE = "composite"  # probability-weighted mix of methods across scenarios


class DCFAssumptions(BaseModel):
    """Multi-stage discounted cash flow. One entry per explicit-forecast year."""

    base_revenue: float = Field(description="Most recent annual revenue, USD.")
    revenue_growth: list[float] = Field(description="Per-year growth rate, e.g. 0.10 = 10%.")
    ebit_margin: list[float] = Field(description="Per-year EBIT margin 0-1; matches growth length.")
    tax_rate: float = Field(ge=0, le=1)
    capex_pct_revenue: list[float]
    nwc_pct_revenue: list[float] = Field(description="Net working capital change as % of revenue.")
    da_pct_revenue: list[float] = Field(description="Depreciation & amortization as % of revenue.")
    terminal_growth: float = Field(description="Perpetuity growth rate after the forecast horizon.")
    wacc: float = Field(gt=0, description="Discount rate.")
    shares_outstanding: float = Field(gt=0)
    net_debt: float = Field(description="Total debt minus cash; subtracted from EV to get equity.")

    @model_validator(mode="after")
    def _equal_length_series(self) -> DCFAssumptions:
        n = len(self.revenue_growth)
        for name in ("ebit_margin", "capex_pct_revenue", "nwc_pct_revenue", "da_pct_revenue"):
            if len(getattr(self, name)) != n:
                raise ValueError(f"DCF series '{name}' must match revenue_growth length ({n}).")
        if not 0 < self.terminal_growth < self.wacc:
            raise ValueError("Require 0 < terminal_growth < wacc for a finite terminal value.")
        return self


class Scenario(BaseModel):
    name: str
    probability: float = Field(ge=0, le=1)
    value_per_share: float = Field(
        description="Equity value per share IF this scenario realizes, AT the realization date "
                    "(undiscounted). The engine discounts it to today using years_to_realization.")
    years_to_realization: float = Field(
        default=0.0, ge=0,
        description="Years from today until this scenario's value is realized (e.g. trial readout "
                    "/ catalyst date). The engine discounts value_per_share over this horizon.")


class RNPVAssumptions(BaseModel):
    """Probability-weighted, TIME-DISCOUNTED scenarios for catalyst/milestone names.

    Real rNPV: the model supplies judgment (each scenario's probability, the value if it
    realizes, and WHEN), and the code does the time value — expected present value =
    Σ p_i × value_i / (1+r)^years_i. The discount rate should reflect SYSTEMATIC risk only
    (the idiosyncratic/technical risk is already captured in the probabilities — do not
    double-count it with a venture-style rate).
    """

    scenarios: list[Scenario] = Field(min_length=2)
    discount_rate: float = Field(
        default=0.0, ge=0, lt=1,
        description="Systematic-risk discount rate applied to the probability-weighted, time-"
                    "dated scenario values. Build it up (rf + beta×ERP + micro-cap size premium); "
                    "do NOT add a venture premium on top of the probabilities.")

    @model_validator(mode="after")
    def _probabilities_sum_to_one(self) -> RNPVAssumptions:
        total = sum(s.probability for s in self.scenarios)
        if abs(total - 1.0) > 1e-6:
            raise ValueError(f"rNPV scenario probabilities must sum to 1 (got {total}).")
        # Guard the silent no-discount trap: if a discount rate is set but EVERY scenario
        # left years_to_realization at its default 0, no time-discounting happens at all
        # (the headline collapses to a plain probability-weighted average). That is almost
        # always the PM forgetting to date the catalysts.
        if self.discount_rate > 0 and all(s.years_to_realization == 0 for s in self.scenarios):
            raise ValueError(
                "discount_rate is set but every scenario has years_to_realization=0, so nothing "
                "is discounted. Set each scenario's years_to_realization (when the value is "
                "realized) so the rNPV actually time-discounts.")
        return self


class AssetLine(BaseModel):
    name: str
    fair_value: float
    realization_haircut: float = Field(default=0.0, ge=0, le=1)


class NAVAssumptions(BaseModel):
    """Net asset value / sum-of-the-parts for asset-heavy names."""

    assets: list[AssetLine] = Field(min_length=1)
    total_liabilities: float
    shares_outstanding: float = Field(gt=0)


_MULTIPLE_ALIASES = {
    "ev_ebitda": "ev_ebitda", "ev/ebitda": "ev_ebitda", "ev_to_ebitda": "ev_ebitda",
    "evebitda": "ev_ebitda", "ev_ebit": "ev_ebitda",
    "ev_sales": "ev_sales", "ev/sales": "ev_sales", "ev_to_sales": "ev_sales",
    "ev_revenue": "ev_sales", "ev/revenue": "ev_sales",
    "ps": "p_s", "p_s": "p_s", "p/s": "p_s", "price_sales": "p_s",  # equity-level
    "p_e": "p_e", "p/e": "p_e", "pe": "p_e", "price_earnings": "p_e",
    "p_b": "p_b", "p/b": "p_b", "pb": "p_b", "price_book": "p_b", "p_tbv": "p_b",
    "p/tbv": "p_b", "p_ffo": "p_ffo", "p/ffo": "p_ffo",  # REIT funds-from-ops (equity-level)
}


class CompsAssumptions(BaseModel):
    """Multiples-based valuation against a clean peer set."""

    peer_set: list[str] = Field(min_length=1, description="Peer tickers.")
    multiple_type: str = Field(
        description="Canonical multiple: ev_ebitda, ev_sales (EV-level, net-debt bridged) or "
                    "p_e, p_b, p_ffo (equity-level). Common synonyms are normalized.")
    target_multiple: float = Field(gt=0, description="Multiple to apply (justify vs peer range).")
    metric_value: float = Field(description="The company's metric the multiple applies to.")
    shares_outstanding: float = Field(gt=0)
    net_debt: float = Field(default=0.0, description="Used to bridge EV-based multiples to equity.")

    @field_validator("multiple_type")
    @classmethod
    def _normalize_multiple(cls, val: str) -> str:
        key = (val or "").strip().lower().replace(" ", "").replace("-", "_")
        if key in _MULTIPLE_ALIASES:
            return _MULTIPLE_ALIASES[key]
        raise ValueError(
            f"unrecognized multiple_type {val!r}; use one of ev_ebitda, ev_sales, p_e, p_b, p_ffo "
            "(EV-level multiples are net-debt bridged to equity automatically)")


class ExcessReturnsAssumptions(BaseModel):
    """Book value x warranted return multiple — the right frame for financial firms.

    Warranted P/B = (sustainable_return - growth) / (cost_of_equity - growth); equity
    value = book x warranted P/B. Covers insurers (through-cycle ROE) and banks (ROTE)
    with no sector branching. Use ``tangible`` book for banks.
    """

    book_value: float = Field(description="Total common (tangible) book equity, not per share.")
    shares_outstanding: float = Field(gt=0)
    sustainable_return: float = Field(description="Through-cycle ROE/ROTE, e.g. 0.12 = 12%.")
    cost_of_equity: float = Field(gt=0)
    growth: float = Field(description="Sustainable book/earnings growth; must be < cost_of_equity.")

    @model_validator(mode="after")
    def _coe_gt_growth(self) -> ExcessReturnsAssumptions:
        if not self.growth < self.cost_of_equity:
            raise ValueError("Require growth < cost_of_equity for a finite warranted multiple.")
        # Warranted P/B = (sustainable_return - growth)/(cost_of_equity - growth); if the
        # firm cannot out-earn its own growth rate (sustainable_return <= growth) the numerator
        # goes negative and the model yields a nonsensical NEGATIVE fair value. A firm growing
        # book faster than the ROE that funds it is internally inconsistent — lower growth.
        if not self.sustainable_return > self.growth:
            raise ValueError(
                "Require sustainable_return > growth (else warranted P/B is negative). A firm "
                "cannot durably grow book faster than the ROE that funds it; lower the growth "
                "assumption or raise the through-cycle return.")
        return self


class WorkedValuationAssumptions(BaseModel):
    """Any valuation framework the PM judges correct for THIS business.

    The PM supplies named numeric inputs and a formula over them; CODE evaluates the
    formula (see valuation/safe_eval). This keeps math-in-code for un-enumerated
    methods (REIT cap-rate NAV, miner reserve NPV, AUM x fee, embedded value, ...)
    without forcing any pre-baked method. The formula must yield FAIR VALUE PER SHARE.
    """

    framework: str = Field(description="Name the method, e.g. 'P/TBV x ROTE'.")
    key_inputs: dict[str, float] = Field(description="Named numeric inputs used by the formula.")
    formula: str = Field(description="Arithmetic over key_inputs; yields value PER SHARE.")

    @model_validator(mode="after")
    def _formula_evaluates(self) -> WorkedValuationAssumptions:
        from microcap_engine.valuation.safe_eval import FormulaError, safe_eval

        try:
            safe_eval(self.formula, self.key_inputs)
        except FormulaError as e:
            raise ValueError(f"worked formula invalid: {e}") from e
        return self


class CompositeScenario(BaseModel):
    """One event-conditional branch of a composite valuation.

    Each scenario picks the sub-method that fits *if that scenario happens* — e.g.
    "turnaround succeeds -> value the cash flows by DCF" vs "stalls -> book-value
    NAV floor". Exactly one sub-block (or a direct per-share value) is populated;
    the composite engine computes each branch and probability-weights them.
    """

    name: str
    probability: float = Field(ge=0, le=1)
    sub_method: Literal["dcf", "comps", "nav", "excess_returns", "worked", "direct"] = Field(
        description="The valuation method for THIS event branch.",
    )
    rationale: str = ""
    dcf: DCFAssumptions | None = None
    comps: CompsAssumptions | None = None
    nav: NAVAssumptions | None = None
    excess_returns: ExcessReturnsAssumptions | None = None
    worked: WorkedValuationAssumptions | None = None
    value_per_share: float | None = Field(
        default=None, description="Equity value per share when sub_method is 'direct'."
    )

    @model_validator(mode="after")
    def _one_subblock(self) -> CompositeScenario:
        if self.sub_method == "direct":
            if self.value_per_share is None:
                raise ValueError(f"Scenario '{self.name}': direct requires value_per_share.")
            return self
        block = getattr(self, self.sub_method)
        if block is None:
            raise ValueError(
                f"Scenario '{self.name}': sub_method '{self.sub_method}' requires its block."
            )
        return self


class CompositeAssumptions(BaseModel):
    """A probability-weighted mix of methods across event scenarios."""

    scenarios: list[CompositeScenario] = Field(min_length=2)

    @model_validator(mode="after")
    def _probs_sum_to_one(self) -> CompositeAssumptions:
        total = sum(s.probability for s in self.scenarios)
        if abs(total - 1.0) > 1e-6:
            raise ValueError(f"Composite scenario probabilities must sum to 1 (got {total}).")
        return self


class AssumptionSet(BaseModel):
    """The gate object. Exactly one method block is populated, matching ``method``."""

    method: ValuationMethod
    rationale: str = Field(description="Why this method fits this business.")
    horizon_years: int = Field(default=5, ge=1, le=20)
    key_risks: list[str] = Field(default_factory=list)
    citations: list[Citation] = Field(min_length=1)

    dcf: DCFAssumptions | None = None
    rnpv: RNPVAssumptions | None = None
    nav: NAVAssumptions | None = None
    comps: CompsAssumptions | None = None
    excess_returns: ExcessReturnsAssumptions | None = None
    worked: WorkedValuationAssumptions | None = None
    composite: CompositeAssumptions | None = None

    @model_validator(mode="after")
    def _exactly_one_block_matching_method(self) -> AssumptionSet:
        blocks = {
            ValuationMethod.DCF: self.dcf,
            ValuationMethod.RNPV: self.rnpv,
            ValuationMethod.NAV: self.nav,
            ValuationMethod.COMPS: self.comps,
            ValuationMethod.EXCESS_RETURNS: self.excess_returns,
            ValuationMethod.WORKED: self.worked,
            ValuationMethod.COMPOSITE: self.composite,
        }
        populated = [m for m, b in blocks.items() if b is not None]
        if populated != [self.method]:
            raise ValueError(
                f"AssumptionSet must populate exactly the '{self.method.value}' block "
                f"(populated: {[m.value for m in populated]})."
            )
        return self

    def active_block(self) -> BaseModel:
        """Return the single populated assumption block."""
        block = getattr(self, self.method.value)
        assert block is not None  # guaranteed by the validator
        return block

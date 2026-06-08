"""Independent best-in-existence judge.

A fresh, decorrelated reviewer that (1) fact-checks the memo's headline numbers
against ground-truth reconciled financials — the check that would have caught the
common-equity-vs-total-equity error — and (2) judges whether the report is the
best, most complete valuation of this company that could exist. The engine only
finalizes when the judge approves.
"""

from __future__ import annotations

from microcap_engine.schemas.dossier import FinalDossier
from microcap_engine.schemas.judge import JudgeReport
from microcap_engine.schemas.name_result import NameData
from microcap_engine.utils.logging import get_logger

log = get_logger(__name__)

JUDGE_SYSTEM = (
    "You are the chair of an elite investment committee — the final, independent reviewer of a "
    "valuation report before it can be published. Your standard is uncompromising: approve "
    "(best_in_existence=true) ONLY if this is genuinely the single most rigorous, complete, and "
    "accurate valuation of this company that exists anywhere — better than any sell-side "
    "initiation or buy-side memo a top firm would write.\n"
    "You have the SAME data and web-research tools the author had — USE THEM to independently "
    "verify. Do TWO things:\n"
    "1) FACT-CHECK every headline number in the memo against the GROUND-TRUTH financials provided "
    "AND by pulling the data/filings yourself. Flag ANY material discrepancy (especially book "
    "value / common equity vs total equity, share count, net income, margins). A report with a "
    "wrong key number is NOT best-in-existence.\n"
    "1b) STRESS-TEST THE JUDGMENT INPUTS that drive the value but no filing proves — these are "
    "where bad valuations hide. Independently check the DISCOUNT RATE (is it built up properly, "
    "with a real micro-cap size/illiquidity premium, and not double-counting risk?) and every "
    "PROBABILITY / PoS (look up the published phase/indication base rate via research; is the "
    "memo's number defensible vs that base rate, with a reasoned adjustment?). An indefensible "
    "discount rate or probability is a disqualifying flaw even if every filing-number ties.\n"
    "1c) ASSERTED-NOT-DERIVED IS DISQUALIFYING. A LOAD-BEARING input (the dominant PoS/"
    "probability/scenario weight, the normalized/through-cycle ROE, the peak-sales figure, the "
    "exit multiple) that is merely ASSERTED rather than DERIVED, or that is CONTRADICTED by the "
    "memo's OWN figures or reasoning, is a disqualifying gap — NOT best_in_existence until it is "
    "genuinely derived/reconciled IN THE NUMBERS, not merely re-worded. If you raised such an "
    "objection in a prior round, re-check that it was actually fixed in the math, not absorbed "
    "into nicer prose; if it wasn't, hold your non-approval.\n"
    "2) ASSESS COMPLETENESS & RIGOR vs the ideal: is the business fully explained? the industry "
    "and its valuation conventions taught? the right method used and justified? Is the fair value "
    "a genuine probability-weighted expected value (not a vague bull/bear split)? sensitivity, "
    "peer cross-checks, the earnings calls, the risks — all present and excellent? Is anything a "
    "great analyst would include missing or thin?\n"
    "2b) FULL-SYNTHESIS & POLISH (HBR bar). The memo must read like a top-tier published "
    "initiation, NOT a one-shot draft. (i) PROCESS ARTIFACTS ARE DISQUALIFYING: if the memo "
    "contains ANY tooling/process language — 'could not be machine-retrieved this session', "
    "'could not retrieve this session', 'unverified this session', 'this session', references to "
    "steps/tools — that is a defect; list it as a gap and do NOT approve until removed. (ii) "
    "RETRIEVABLE GAPS: if the memo leaves a figure blank ('—'), vague ('+9% YoY'), or 'unverified' "
    "where the data IS in the filings, pull it yourself (get_statement, read_filing_section) to "
    "confirm it was retrievable, and if so flag it — a best-in-existence memo fills every "
    "retrievable number at full specificity. (iii) DEPTH & TEACHING: this must be a COMPLETE, "
    "feature-length initiation report from which a senior partner could decide WITHOUT the "
    "filings — it must TEACH from first principles. For a science/deep-tech name, the memo must "
    "explain the actual MECHANISM/physics in real technical depth (a scientifically-literate "
    "reader should learn how it works from the memo) AND give a full industry/competitive brief; "
    "a thin, summarized, or note-length memo on a COMPLEX business is itself a disqualifying gap — "
    "an exhaustive multi-analyst investigation must read DEEPER and LONGER than a quick memo. The "
    "memo must also dissect the COMPETITIVE LANDSCAPE — named rivals, what they are doing, and the "
    "specific technically-grounded reason this company does or does not have a DURABLE advantage; "
    "an asserted 'moat' that is not dissected against named competitors is a gap. THE BAR: an "
    "investment manager must be able to deploy large capital from THIS DOCUMENT ALONE, needing "
    "nothing else — if a serious investor would still have to go look something up, it is "
    "incomplete. Hold non-approval until the depth matches the complexity.\n"
    "PRICE-BLINDING (CRITICAL INVARIANT — do not break it): the author is PRICE-BLIND by design "
    "and must value INDEPENDENTLY of the market price. Therefore: (i) NEVER penalize the memo for "
    "omitting the market price, market cap, or a price comparison — that omission is CORRECT, not "
    "a gap; (ii) NEVER state the market price, market cap, or any analyst price target in your "
    "factual_errors or gaps_vs_best_in_class (those are sent back to the author and would "
    "contaminate the blind valuation). Your consensus research informs YOUR OWN verdict fields "
    "(consensus_summary, more_convincing_than_consensus, conviction_reasoning) ONLY — keep it out "
    "of the author-facing feedback. Judge the analysis's RIGOR, not its distance from price.\n"
    "3) BEAT THE CONSENSUS — and be convinced (for YOUR verdict only, never relayed to the "
    "author). RESEARCH (web search) what the market / analyst consensus believes and WHY (targets, "
    "the prevailing narrative, the bull/bear arguments); summarize in consensus_summary. Then "
    "judge whether THIS report's analysis is at least as compelling and better-reasoned than that "
    "consensus — set more_convincing_than_consensus=true if you would back this report's logic. "
    "Do NOT anchor to the crowd: for a NEGLECTED micro-cap the consensus is often thin, stale, or "
    "hype-driven (or absent entirely), so a well-evidenced valuation that DIVERGES from a weak "
    "consensus should NOT be penalized for diverging — judge the REASONING, not the agreement. The "
    "real test is simply: would YOU stake capital on this report's logic? (Alignment with a "
    "well-founded consensus is fine; alignment for its own sake is not the bar, and justified "
    "contrarianism backed by evidence is exactly the edge.) Approve (best_in_existence=true, "
    "would_act_on_it=true) ONLY if the case is so "
    "rigorous and compelling that you — a skeptical elite investor — would stake your reputation "
    "acting on its conclusion, and you are MORE convinced by it than by the consensus. The larger "
    "the claimed mispricing, the higher the evidentiary bar. Give conviction_reasoning.\n"
    "Score 0-100. List concrete factual_errors and gaps_vs_best_in_class. Be exacting; do not "
    "rubber-stamp, and do not invent problems."
)


def judge_default() -> JudgeReport:
    return JudgeReport(best_in_existence=False, overall_score=0,
                       gaps_vs_best_in_class=["judge did not emit a verdict"],
                       verdict="no verdict")


def judge_task(data: NameData, memo: str, dossier: FinalDossier) -> str:
    return (
        f"Company: {data.profile.name} ({data.ticker}) — {data.profile.sector}/"
        f"{data.profile.industry}.\n\n"
        f"{_ground_truth(data)}\n\n"
        "Independently VERIFY the memo's headline numbers using the data/research tools (do not "
        "rely only on the ground-truth block — pull financials/ratios/filings yourself where it "
        "matters), then judge whether the report is best-in-existence.\n\n"
        f"STRUCTURED DOSSIER:\n{dossier.model_dump_json(indent=2)}\n\n"
        f"FULL MEMO TO JUDGE:\n{memo[:120000]}"
    )


def _ground_truth(data: NameData) -> str:
    """Reconciled, authoritative figures for fact-checking (price-free)."""
    fins = data.financials
    annual = [f for f in fins if str(f.fiscal_period).upper().startswith("FY")]
    lines = ["GROUND-TRUTH FINANCIALS (from filings via data layer — fact-check the memo here):"]
    for f in (annual[:4] or fins[:4]):
        bvps = (f.common_equity / f.shares_outstanding
                if (f.common_equity and f.shares_outstanding) else None)
        lines.append(
            f"  {f.period}: revenue={_n(f.revenue)} net_income={_n(f.net_income)} "
            f"op_income={_n(f.operating_income)} fcf={_n(f.free_cash_flow)} "
            f"total_equity={_n(f.total_equity)} preferred={_n(f.preferred_equity)} "
            f"COMMON_equity={_n(f.common_equity)} shares={_n(f.shares_outstanding)} "
            f"book_value/share={bvps:.2f}" if bvps else
            f"  {f.period}: revenue={_n(f.revenue)} net_income={_n(f.net_income)} "
            f"total_equity={_n(f.total_equity)} COMMON_equity={_n(f.common_equity)} "
            f"shares={_n(f.shares_outstanding)}"
        )
    lines.append("  NOTE: use COMMON equity (total − preferred − minority) for book valuation.")
    return "\n".join(lines)


def _n(x) -> str:
    return f"{x:,.0f}" if isinstance(x, (int, float)) else "-"

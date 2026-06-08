"""The PM's toolbox — capabilities, not prescribed logic.

The agentic orchestrator (PM) drives its own investigation by calling these tools
in whatever order, as many times as it needs. They give it the leverage a default
chatbot lacks (live financials, filings, peers, web research, deterministic
valuation, a decorrelated red-team) WITHOUT dictating how to value the business.

All tools are price-blind: none returns the market quote or market cap-derived
price. The valuation tool is the code-enforced gate (only an AssumptionSet in).
``reject_early`` and ``submit_final`` are terminal and handled by the loop.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from microcap_engine.data.edgar import EdgarFilingsProvider
from microcap_engine.data.fmp import FMPProvider
from microcap_engine.llm.client import LLMClient
from microcap_engine.orchestrator import digest
from microcap_engine.orchestrator.research import research
from microcap_engine.schemas.assumptions import AssumptionSet
from microcap_engine.schemas.dossier import FinalDossier
from microcap_engine.schemas.name_result import NameData
from microcap_engine.utils.logging import get_logger
from microcap_engine.valuation.dispatch import run_valuation

log = get_logger(__name__)


@dataclass
class ToolContext:
    ticker: str
    data: NameData
    fmp: FMPProvider
    edgar: EdgarFilingsProvider
    client: LLMClient
    run_id: str
    model: str
    last_valuation: Any = None  # ValuationResult
    valuations: list = field(default_factory=list)
    analysts: dict = field(default_factory=dict)  # analyst_id -> Analyst (persistent team)


@dataclass
class ToolReply:
    content: str
    terminal: str | None = None  # None | "reject" | "submit"
    payload: dict = field(default_factory=dict)


# ── tool schemas exposed to the model ──────────────────────────────────────
def tool_specs() -> list[dict]:
    return [
        {
            "name": "get_financials",
            "description": "Multi-period financial statements (income, balance, cash flow) "
                           "as a table. Use to study trends.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "period": {"type": "string", "enum": ["annual", "quarter"]},
                    "years": {"type": "integer", "description": "How many periods (default 5)."},
                },
            },
        },
        {
            "name": "get_ratios",
            "description": "TTM ratios & key metrics for this company: P/B, P/E, ROE, ROIC, "
                           "margins, leverage, EV multiples, book value per share, etc.",
            "input_schema": {"type": "object", "properties": {}},
        },
        {
            "name": "get_peers",
            "description": "Sector/industry peer companies with their TTM multiples (P/B, P/E, "
                           "EV/EBITDA, ROE) for relative valuation.",
            "input_schema": {
                "type": "object",
                "properties": {"max_peers": {"type": "integer"}},
            },
        },
        {
            "name": "get_segments",
            "description": "Product/geographic revenue segmentation for the most recent period.",
            "input_schema": {"type": "object", "properties": {}},
        },
        {
            "name": "get_statement",
            "description": "The FULL as-reported financial statement with EVERY line item "
                           "(balance sheet: cash, receivables, inventory, goodwill, current vs "
                           "long-term assets/liabilities, debt, deferred revenue, equity detail; "
                           "income; or cash flow). Use this whenever you need a specific balance-"
                           "sheet/income/cash-flow figure — do NOT web-search for financial "
                           "statement numbers, pull them here.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "statement": {"type": "string",
                                  "description": "balance_sheet | income | cash_flow"},
                    "period": {"type": "string", "description": "annual (default) or quarter"},
                    "limit": {"type": "integer", "description": "how many periods (default 4)"},
                },
                "required": ["statement"],
            },
        },
        {
            "name": "get_insider_activity",
            "description": "Recent insider (Form 4) transactions — who bought/sold, when, how "
                           "many shares, and resulting holdings. Use to gauge insider "
                           "conviction/selling pressure instead of web-searching.",
            "input_schema": {"type": "object", "properties": {}},
        },
        {
            "name": "get_ownership",
            "description": "Institutional (13F) ownership summary — number of holders, share "
                           "count, and net change. Use to gauge institutional vs retail backing.",
            "input_schema": {"type": "object", "properties": {}},
        },
        {
            "name": "read_filing_section",
            "description": "Read a section of an SEC filing. forms: 10-K, 10-Q, DEF 14A (proxy, "
                           "for capital structure / dilution / comp). section examples: "
                           "'Item 1', 'Item 1A', 'Item 7', 'Item 8', or a keyword to search for.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "form": {"type": "string"},
                    "section": {"type": "string"},
                },
                "required": ["form", "section"],
            },
        },
        {
            "name": "get_news",
            "description": "Recent news headlines and snippets for this company.",
            "input_schema": {"type": "object", "properties": {}},
        },
        {
            "name": "get_transcripts",
            "description": "Recent earnings-call transcript text (management commentary, Q&A).",
            "input_schema": {"type": "object", "properties": {}},
        },
        {
            "name": "research",
            "description": "Spawn a research subagent with WEB SEARCH to answer a focused "
                           "question — e.g. how this kind of business should be valued and which "
                           "metrics matter, an industry/supply-chain question, or a competitor "
                           "fact. Use this to determine the RIGHT valuation approach for THIS "
                           "business rather than defaulting to one.",
            "input_schema": {
                "type": "object",
                "properties": {"question": {"type": "string"}},
                "required": ["question"],
            },
        },
        {
            "name": "spawn_analyst",
            "description": "Delegate a deep sub-investigation to a PERSISTENT specialist analyst "
                           "on your desk. Unlike a quick question, this analyst pulls the primary "
                           "record ITSELF (historical 10-K/10-Q sections, earnings-call "
                           "transcripts, financials, ratios, peers, segments) and the web, and "
                           "CONSOLIDATES it into a decision-useful answer. Use it to parallelize "
                           "depth — e.g. 'consolidate 3 years of 10-Ks + the last 4 earnings calls "
                           "into the revenue/margin/dilution story', 'work up the competitive "
                           "landscape', 'reconstruct the clinical pipeline and trial readouts'. "
                           "Returns its analysis AND an analyst_id you can follow up with.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "role": {"type": "string",
                             "description": "e.g. 'forensic accountant', 'biotech analyst', "
                                            "'insurance specialist'."},
                    "question": {"type": "string", "description": "The deep task to investigate."},
                    "context": {"type": "string",
                                "description": "Optional framing/facts to point the analyst."},
                },
                "required": ["role", "question"],
            },
        },
        {
            "name": "ask_analyst",
            "description": "Follow up with an analyst already on your desk (by analyst_id). It "
                           "retains its FULL prior context and can pull more data — this is the "
                           "back-and-forth a real PM has with the team: probe, challenge, ask for "
                           "the number it missed, until the conclusion is definitive. You don't "
                           "always need a follow-up, but the analyst is there when you do.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "analyst_id": {"type": "string",
                                   "description": "The id returned by spawn_analyst."},
                    "question": {"type": "string", "description": "Your follow-up question."},
                    "context": {"type": "string", "description": "Optional extra framing."},
                },
                "required": ["analyst_id", "question"],
            },
        },
        {
            "name": "compute_valuation",
            "description": "Compute a fair value by submitting a valuation AssumptionSet. The "
                           "ARITHMETIC runs in code (you provide judgment/inputs, not the number). "
                           "Pick the method that truly fits this business (dcf, comps, nav, rnpv, "
                           "excess_returns for financials, worked=any framework via a formula, or "
                           "composite across event scenarios). Call repeatedly to test approaches.",
            "input_schema": AssumptionSet.model_json_schema(),
        },
        {
            "name": "reject_early",
            "description": "End the analysis early — ONLY when there is genuinely no plausible "
                           "case this could be materially undervalued (no viable business AND no "
                           "asset value, or imminent insolvency with nothing to recover). When in "
                           "doubt, keep working instead.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "reason": {"type": "string"},
                    "confidence": {"type": "number"},
                },
                "required": ["reason"],
            },
        },
        {
            "name": "submit_final",
            "description": "Submit your FINAL valuation: an extremely in-depth markdown investment "
                           "memo justifying the value from start to finish, PLUS the structured "
                           "dossier. After you submit, a red-team will attack it; if it finds "
                           "valuation-changing flaws you will be sent back to fix or rebut them. "
                           "Only submit when your valuation is rock-solid.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "markdown_memo": {
                        "type": "string",
                        "description": "The FULL feature-length memo (markdown, ~2,500-5,000+ "
                                       "words), explanatory like a Harvard Business Review piece: "
                                       "exec summary; business deep-dive; industry & competition; "
                                       "financial analysis (with sector metrics explained); what "
                                       "management said on the calls; valuation (why this method, "
                                       "fully worked, with the discount-rate build-up, "
                                       "sensitivity, a cross-check); the probability-weighted "
                                       "distribution (NOT a bull/bear split); risks; conclusion. "
                                       "Teach the reader — do not be terse. Write CLEAN GitHub-"
                                       "flavored markdown: for approximations use the '≈' symbol "
                                       "or the word 'about' — do NOT use a '~' tilde, which GitHub "
                                       "renders as strikethrough.",
                    },
                    "dossier": FinalDossier.model_json_schema(),
                },
                "required": ["markdown_memo", "dossier"],
            },
        },
    ]


# Read/verify tools a REVIEWER may use to independently check the memo's numbers
# and claims (no compute_valuation/reject/submit — reviewers verify, they don't value).
_VERIFICATION_TOOLS = {
    "get_financials", "get_ratios", "get_peers", "get_segments", "get_statement",
    "get_insider_activity", "get_ownership",
    "read_filing_section", "get_news", "get_transcripts", "research",
}


def verification_tool_specs() -> list[dict]:
    return [s for s in tool_specs() if s["name"] in _VERIFICATION_TOOLS]


# ── executors ──────────────────────────────────────────────────────────────
def execute(ctx: ToolContext, name: str, tool_input: dict) -> ToolReply:
    try:
        handler = _HANDLERS[name]
    except KeyError:
        return ToolReply(content=f"[unknown tool {name}]")
    try:
        return handler(ctx, tool_input or {})
    except Exception as e:  # pragma: no cover - tool robustness
        log.warning("[%s] tool %s failed: %s", ctx.ticker, name, e)
        return ToolReply(content=f"[tool {name} error: {e}]")


def _h_financials(ctx, inp) -> ToolReply:
    return ToolReply(content=digest.financials_block(ctx.data))


def _h_ratios(ctx, inp) -> ToolReply:
    r = ctx.fmp.get_ratios(ctx.ticker)
    if not r:
        return ToolReply(content="No ratios available.")
    lines = [f"{k}: {round(v, 4) if isinstance(v, float) else v}" for k, v in r.items()]
    return ToolReply(content="TTM RATIOS & KEY METRICS:\n" + "\n".join(lines))


def _h_peers(ctx, inp) -> ToolReply:
    peers = ctx.fmp.get_peers(ctx.data.profile, max_peers=int(inp.get("max_peers", 12)))
    if not peers:
        return ToolReply(content="No peers found.")
    return ToolReply(content="PEERS (TTM multiples):\n" + json.dumps(peers, indent=1, default=str))


def _h_segments(ctx, inp) -> ToolReply:
    segs = ctx.fmp.get_segments(ctx.ticker)
    if not segs:
        return ToolReply(content="No segment data available.")
    return ToolReply(content="SEGMENT REVENUE:\n" + json.dumps(segs, indent=1, default=str))


_STMT_SKIP = {"symbol", "reportedCurrency", "cik", "filingDate", "acceptedDate", "link",
              "finalLink", "calendarYear"}


def _h_statement(ctx, inp) -> ToolReply:
    """Full as-reported statement (every line item) — so the PM never web-searches for a
    balance sheet / income / cash-flow number that FMP serves directly."""
    which = (inp.get("statement") or "balance_sheet").lower().replace("-", "_").replace(" ", "_")
    if which in ("balancesheet", "balance"):
        which = "balance_sheet"
    if which in ("cashflow", "cash"):
        which = "cash_flow"
    period = "quarter" if str(inp.get("period", "annual")).lower().startswith("q") else "annual"
    rows = ctx.fmp.get_statement(ctx.ticker, which, period=period, limit=int(inp.get("limit", 4)))
    if not rows:
        return ToolReply(content=f"No {which} data available for {ctx.ticker}.")
    out = [f"{which.upper().replace('_', ' ')} ({period}, most recent first) — full line items:"]
    for r in rows:
        per = f"{r.get('fiscalYear', '?')}-{r.get('period', '')}".strip("-")
        lines = [f"  {k}={v}" for k, v in r.items()
                 if k not in _STMT_SKIP and k not in ("date", "fiscalYear", "period")
                 and isinstance(v, (int, float))]
        out.append(f"\n[{per}] ({r.get('date', '')})\n" + "\n".join(lines))
    return ToolReply(content="\n".join(out))


def _h_insider(ctx, inp) -> ToolReply:
    trades = ctx.fmp.get_insider_trades(ctx.ticker, limit=int(inp.get("limit", 25)))
    if not trades:
        return ToolReply(content=f"No insider-transaction data for {ctx.ticker}.")
    lines = ["RECENT INSIDER TRANSACTIONS (Form 4):"]
    for t in trades[:25]:
        lines.append(
            f"  {t.get('transactionDate')} {t.get('reportingName')} "
            f"({t.get('typeOfOwner', '')}): {t.get('transactionType')} "
            f"{t.get('securitiesTransacted')} @ {t.get('price')} "
            f"-> owns {t.get('securitiesOwned')}")
    return ToolReply(content="\n".join(lines))


def _h_ownership(ctx, inp) -> ToolReply:
    s = ctx.fmp.get_institutional_summary(ctx.ticker)
    if not s:
        return ToolReply(content=f"No institutional-ownership data for {ctx.ticker}.")
    return ToolReply(content=(
        f"INSTITUTIONAL (13F) OWNERSHIP for {ctx.ticker} (as of {s.get('date')}):\n"
        f"  holders={s.get('investorsHolding')} (prev {s.get('lastInvestorsHolding')}, "
        f"change {s.get('investorsHoldingChange')})\n"
        f"  13F shares={s.get('numberOf13Fshares')} (change {s.get('numberOf13FsharesChange')})\n"
        f"  total invested=${s.get('totalInvested')}; ownership%={s.get('ownershipPercent')}"))


def _h_news(ctx, inp) -> ToolReply:
    return ToolReply(content=digest.news_text(ctx.data))


def _h_transcripts(ctx, inp) -> ToolReply:
    return ToolReply(content=digest.transcripts_block(ctx.data, per_call_cap=12000))


def _h_read_filing(ctx, inp) -> ToolReply:
    form = (inp.get("form") or "").upper()
    section = inp.get("section") or ""
    # Try already-loaded filings (10-K/10-Q) first.
    for f in ctx.data.filings:
        if f.form.upper() == form:
            if section in f.sections:
                return ToolReply(content=f"{form} {f.filed_date} — {section}:\n"
                                         + f.sections[section][:30000])
            # keyword search within full text
            txt = f.full_text
            idx = txt.lower().find(section.lower())
            if idx >= 0:
                return ToolReply(content=f"{form} {f.filed_date} — '{section}':\n"
                                         + txt[max(0, idx - 500):idx + 8000])
            # fall back to whatever sections exist
            avail = ", ".join(f.sections.keys())
            return ToolReply(content=f"Section '{section}' not found in {form}. "
                                     f"Available: {avail}. Head:\n" + txt[:8000])
    # Not loaded (e.g. DEF 14A proxy) — fetch on demand.
    cik = ctx.data.profile.cik
    if cik:
        try:
            refs = ctx.edgar.list_filings(cik, [form], 1)
            if refs:
                doc = ctx.edgar.fetch_filing(refs[0])
                txt = doc.full_text
                idx = txt.lower().find(section.lower()) if section else -1
                snippet = txt[max(0, idx - 500):idx + 8000] if idx >= 0 else txt[:12000]
                return ToolReply(content=f"{form} {doc.filed_date} (fetched):\n" + snippet)
        except Exception as e:  # pragma: no cover
            return ToolReply(content=f"[could not fetch {form}: {e}]")
    return ToolReply(content=f"No {form} available for {ctx.ticker}.")


def _h_research(ctx, inp) -> ToolReply:
    q = inp.get("question", "")
    ans = research(ctx.client, q, ticker=ctx.ticker, model=ctx.model)
    return ToolReply(content=f"RESEARCH — {q}\n{ans}")


def _h_spawn_analyst(ctx, inp) -> ToolReply:
    """Stand up a persistent, tool-capable analyst, delegate the question, return its
    analysis + a reusable analyst_id the PM can follow up with via ask_analyst."""
    from microcap_engine.orchestrator.analyst import Analyst

    role = inp.get("role", "analyst")
    analyst_id = f"a{len(ctx.analysts) + 1}-{role.split()[0].lower()[:12]}"
    analyst = Analyst(ctx.client, ctx, analyst_id=analyst_id, role=role, model=ctx.model)
    ctx.analysts[analyst_id] = analyst
    out = analyst.ask(inp.get("question", ""), context=inp.get("context", ""))
    return ToolReply(
        content=f"ANALYST [{analyst_id}] ({role}):\n{out}\n\n"
                f"(This analyst remembers everything; use ask_analyst with analyst_id="
                f"'{analyst_id}' to follow up.)")


def _h_ask_analyst(ctx, inp) -> ToolReply:
    """Follow up with an analyst already on the desk — it retains its full context."""
    analyst_id = inp.get("analyst_id", "")
    analyst = ctx.analysts.get(analyst_id)
    if analyst is None:
        avail = ", ".join(ctx.analysts) or "(none yet — use spawn_analyst first)"
        return ToolReply(content=f"[no analyst '{analyst_id}'. On the desk: {avail}]")
    out = analyst.ask(inp.get("question", ""), context=inp.get("context", ""))
    return ToolReply(content=f"ANALYST [{analyst_id}] ({analyst.role}) follow-up:\n{out}")


def _h_compute_valuation(ctx, inp) -> ToolReply:
    try:
        aset = AssumptionSet.model_validate(inp)
    except Exception as e:
        return ToolReply(content=f"VALUATION REJECTED (invalid AssumptionSet): {e}\n"
                                 f"Fix the inputs/constraints and call compute_valuation again.")
    result = run_valuation(aset)
    ctx.last_valuation = result
    ctx.valuations.append(result)
    working = json.dumps(result.intermediate, default=str)[:2500]
    return ToolReply(
        content=f"VALUATION ({result.method.value}): fair value/share = "
                f"{result.fair_value_per_share}\nequity_value={result.equity_value} "
                f"EV={result.enterprise_value}\nworking={working}"
                f"\nnotes: {result.notes}",
        payload={"valuation": result},
    )


def _h_reject_early(ctx, inp) -> ToolReply:
    return ToolReply(content="", terminal="reject",
                     payload={"reason": inp.get("reason", ""),
                              "confidence": inp.get("confidence", 0.0)})


def _h_submit_final(ctx, inp) -> ToolReply:
    return ToolReply(content="", terminal="submit",
                     payload={"markdown_memo": inp.get("markdown_memo", ""),
                              "dossier_raw": inp.get("dossier", {})})


_HANDLERS = {
    "get_financials": _h_financials,
    "get_ratios": _h_ratios,
    "get_peers": _h_peers,
    "get_segments": _h_segments,
    "get_statement": _h_statement,
    "get_insider_activity": _h_insider,
    "get_ownership": _h_ownership,
    "read_filing_section": _h_read_filing,
    "get_news": _h_news,
    "get_transcripts": _h_transcripts,
    "research": _h_research,
    "spawn_analyst": _h_spawn_analyst,
    "ask_analyst": _h_ask_analyst,
    "compute_valuation": _h_compute_valuation,
    "reject_early": _h_reject_early,
    "submit_final": _h_submit_final,
}

"""Turn a NameData bundle into grounded, capped text blocks for the agents.

Keeps token usage sane (cost isn't binding, but huge prompts add latency and
truncation risk). NO market price appears anywhere here — price-blinding.
"""

from __future__ import annotations

from microcap_engine.schemas.name_result import NameData

# Per-section caps (chars). 10-K sections can be ~60k chars each live.
_FILING_SECTION_CAP = 18_000
_FILING_TOTAL_CAP = 90_000


def profile_block(data: NameData) -> str:
    p = data.profile
    return (
        f"COMPANY: {p.name} ({data.ticker})\n"
        f"Sector: {p.sector} | Industry: {p.industry} | Country: {p.country} | "
        f"Exchange: {p.exchange}\n"
        f"Description: {p.description}"
    )


def financials_block(data: NameData) -> str:
    lines = [
        "MULTI-PERIOD FINANCIALS (most recent first; values in reporting currency):",
        "period | revenue | gross_profit | operating_income | net_income | ebitda | "
        "op_cash_flow | capex | free_cash_flow | cash | total_debt | total_equity | "
        "preferred | COMMON_EQUITY | shares",
    ]
    for f in data.financials:
        lines.append(
            " | ".join(
                str(x) if x is not None else "-"
                for x in (
                    f.period,
                    f.revenue,
                    f.gross_profit,
                    f.operating_income,
                    f.net_income,
                    f.ebitda,
                    f.operating_cash_flow,
                    f.capital_expenditure,
                    f.free_cash_flow,
                    f.cash_and_equivalents,
                    f.total_debt,
                    f.total_equity,
                    f.preferred_equity,
                    f.common_equity,
                    f.shares_outstanding,
                )
            )
        )
    # Explicit book-value callout (the #1 input for financials valued on book).
    latest = next((f for f in data.financials if f.common_equity is not None), None)
    if latest is not None:
        bvps = (latest.common_equity / latest.shares_outstanding
                if latest.shares_outstanding else None)
        lines.append(
            f"\nBOOK VALUE NOTE ({latest.period}): COMMON equity = {latest.common_equity:,.0f} "
            f"(= total_equity {latest.total_equity:,.0f} − preferred "
            f"{latest.preferred_equity or 0:,.0f} − minority "
            f"{latest.minority_interest or 0:,.0f}). "
            f"Use COMMON equity for book-value valuation; the preferred is a SENIOR claim ahead of "
            f"common. Common book value/share ≈ "
            f"{f'{bvps:,.2f}' if bvps else 'n/a'} (on {latest.shares_outstanding:,.0f} shares)."
        )
    if data.key_metrics:
        lines.append("\nKEY METRICS (annual): period | ev/ebitda | ev/sales | fcf_yield | roic")
        for m in data.key_metrics:
            lines.append(
                f"{m.period} | {m.ev_to_ebitda} | {m.ev_to_sales} | {m.fcf_yield} | {m.roic}"
            )
    return "\n".join(lines)


def filings_block(data: NameData) -> str:
    if not data.filings:
        return "FILINGS: none retrieved."
    out: list[str] = []
    used = 0
    for f in data.filings:
        header = f"\n=== {f.form} filed {f.filed_date} (accession {f.accession}) ==="
        out.append(header)
        used += len(header)
        # Prefer the canonical sections; fall back to full_text head.
        items = f.sections or {"BODY": f.full_text}
        for name, text in items.items():
            if used >= _FILING_TOTAL_CAP:
                out.append("...[filing text truncated for length]...")
                return "\n".join(out)
            chunk = text[:_FILING_SECTION_CAP]
            out.append(f"\n--- {name} (accession {f.accession}) ---\n{chunk}")
            used += len(chunk)
    return "\n".join(out)


def transcripts_block(data: NameData, per_call_cap: int = 16_000) -> str:
    """Raw transcript text for the distiller agent (its own context window)."""
    if not data.transcripts:
        return "TRANSCRIPTS: none available."
    out = ["EARNINGS CALL TRANSCRIPTS (most recent first):"]
    for t in data.transcripts:
        out.append(f"\n=== {t.label} ({t.call_date}) ===\n{t.content[:per_call_cap]}")
    return "\n".join(out)


def news_text(data: NameData) -> str:
    if not data.news:
        return "NEWS: none retrieved."
    lines = ["RECENT NEWS (most recent first):"]
    for n in data.news:
        lines.append(f"[{n.published}] {n.source}: {n.headline}")
        if n.body:
            lines.append(f"    {n.body[:400]}")
    return "\n".join(lines)

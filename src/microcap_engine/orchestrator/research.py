"""Web-research subagent — the PM's "go learn how this is valued" capability.

Spawns a fresh agent with Anthropic's server-side web_search tool to answer a
focused methodology/domain question (e.g. "How are P&C insurers valued and which
metrics matter?", "Where do InP substrates sit in the AI-optical supply chain and
what drives demand?"). Returns a distilled, sourced text answer. This is what lets
the engine generalize to any sector without hard-coding sector logic.
"""

from __future__ import annotations

from microcap_engine.config import settings
from microcap_engine.llm.client import LLMClient
from microcap_engine.utils.logging import get_logger

log = get_logger(__name__)

_WEB_SEARCH_TOOL = {"type": "web_search_20260209", "name": "web_search"}

_RESEARCH_SYSTEM = (
    "You are a research analyst. Answer the question precisely, concretely, and "
    "COMPREHENSIVELY using web search. Your answer feeds a deep investment report, so give "
    "the FULL picture, not a summary — explain the topic from first principles, in depth, "
    "with the specifics, mechanisms, numbers, and named players. When the question is about "
    "how to VALUE a kind of business, return: the standard valuation framework(s) "
    "practitioners use and WHY, the specific metrics/drivers that matter, typical multiple "
    "ranges, and the key pitfalls. Be thorough, specific, and cite sources.\n"
    "PRICE-BLINDING (critical): the person you report to is forming an INDEPENDENT "
    "valuation and must NOT see the market's price. Do NOT state the subject company's "
    "stock price, market capitalization, enterprise value, or any analyst PRICE TARGET / "
    "consensus target, and do not describe its recent price move (e.g. 'up 55% YTD'). "
    "Report the qualitative, fundamental, scientific, and methodological findings only. "
    "(Peer/industry TYPICAL MULTIPLE RANGES used as valuation conventions are fine; a "
    "specific dollar price/cap/target for THIS company is not.)"
)


def research(
    client: LLMClient,
    question: str,
    *,
    ticker: str,
    model: str | None = None,
    max_turns: int = 3,
    max_tokens: int = 6000,  # comprehensive but bounded
) -> str:
    """Run a bounded web-search research turn-loop; return the distilled answer."""
    messages = [{"role": "user", "content": question}]
    text_out = ""
    for _ in range(max_turns):
        try:
            resp = client.tool_turn(
                model=model or settings.extract_model,
                system=_RESEARCH_SYSTEM,
                messages=messages,
                tools=[_WEB_SEARCH_TOOL],
                ticker=ticker,
                phase="research",
                label=f"research:{question[:40]}",
                max_tokens=max_tokens,
                thinking=False,
            )
        except Exception as e:  # pragma: no cover - network/tool unavailable
            log.warning("research failed (%s): %s", question[:40], e)
            return text_out or f"[research unavailable: {e}]"
        text_out = "".join(
            getattr(b, "text", "") for b in resp.content if getattr(b, "type", None) == "text"
        )
        if getattr(resp, "stop_reason", None) == "pause_turn":
            # Server tool hit its iteration cap; re-send to continue.
            messages = messages + [{"role": "assistant", "content": resp.content}]
            continue
        break
    return text_out.strip() or "[no research answer produced]"

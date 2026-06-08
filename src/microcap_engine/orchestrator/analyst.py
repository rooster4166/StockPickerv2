"""A persistent, tool-using sub-analyst the PM can delegate to AND follow up with.

Unlike a one-shot helper, an Analyst is a standing member of the PM's team: it can
pull the data itself (historical 10-K/10-Q sections, earnings-call transcripts,
peers, ratios) and the web (`research`), CONSOLIDATE it into an answer, and — because
it is persistent and addressable by id — the PM can come back with follow-up
questions, which the analyst answers with its full prior context intact. That is the
back-and-forth a real PM has with the analysts on the desk: delegate the deep dig,
then probe until the conclusion is definitive (sometimes one pass is enough).
"""

from __future__ import annotations

from microcap_engine.llm.client import LLMClient
from microcap_engine.orchestrator import tools as toolkit
from microcap_engine.utils.logging import get_logger

log = get_logger(__name__)

# The data/research tools an analyst may use to investigate and consolidate. No
# compute_valuation / terminal tools — analysts inform the PM; the PM values.
_ANALYST_TOOLS = {
    "get_financials", "get_ratios", "get_peers", "get_segments",
    "read_filing_section", "get_news", "get_transcripts", "research",
}


def _tr(tool_use_id: str, content: str) -> dict:
    return {"type": "tool_result", "tool_use_id": tool_use_id, "content": content or "(empty)"}


class Analyst:
    """One standing sub-analyst with its own role, memory, and tool access."""

    def __init__(self, client: LLMClient, ctx: toolkit.ToolContext, *, analyst_id: str,
                 role: str, model: str, max_turns: int = 10):
        self.client = client
        self.ctx = ctx
        self.id = analyst_id
        self.role = role
        self.model = model
        self.max_turns = max_turns
        self.ticker = ctx.ticker
        self.messages: list[dict] = []  # persistent across follow-ups
        self.trace: list[dict] = []  # every turn's reasoning + the tools it pulled
        self.system = (
            f"You are a {role} on a micro-cap research desk, reporting to the PM. Investigate the "
            "question RIGOROUSLY and concretely, pulling the primary record YOURSELF with the data "
            "tools (historical 10-K/10-Q sections via read_filing_section; earnings-call "
            "transcripts; financials; get_statement for FULL balance-sheet/income/cash-flow line "
            "items; ratios; peers; segments; get_insider_activity; get_ownership) and the web via "
            "research where needed. Pull every NUMBER from the data tools — never web-search for a "
            "balance-sheet/financial figure FMP serves (use get_statement); reserve research for "
            "industry/scientific/qualitative context the tools cannot give. CONSOLIDATE what you "
            "find into a tight, decision-useful answer for the PM: "
            "lead with the conclusion, then the specific evidence. State explicitly what you could "
            "NOT determine and what you'd need. Do not hedge into mush — give the PM something it "
            "can act on. When the PM follows up, you already have all your prior context; go "
            "deeper, don't repeat. Be EFFICIENT: pull what you need decisively (batch tool "
            "calls), avoid redundant or overlapping research calls, and converge on the answer — "
            "you have a limited number of turns, so don't wander.\n"
            "GROUND EVERYTHING IN CITATIONS — non-negotiable. EVERY material claim, figure, "
            "and explanation must carry its source inline, and you must actually PULL that source "
            "with a tool before asserting it — never answer from memory alone. For a number, cite "
            "the filing + section/period or the statement line (e.g. '10-K FY2024, Item 7' or 'Q3-"
            "2024 income statement'). For management commentary, quote/cite the specific earnings "
            "call. For an industry fact, valuation convention, or a TECHNICAL/SCIENTIFIC concept "
            "(e.g. a biological mechanism, a clinical-trial endpoint, a physics/engineering fact), "
            "use `research` to verify it and CITE the source you got it from — explain the concept "
            "AND prove it with that citation; do not present an unsourced explanation as fact. If "
            "you cannot find a source for something, say so explicitly and flag it as unverified "
            "rather than stating it as established. An uncited claim is treated as not proven.\n"
            "If your subject is scientific/technical (a drug, a quantum/deep-tech program, a "
            "mining asset), do NOT merely catalog what the trials/specs say — ASSESS THE SCIENCE: "
            "judge "
            "whether the mechanism is plausible, whether a surrogate signal credibly translates to "
            "the real endpoint, and the SPECIFIC failure modes of this modality (e.g. autoimmunity "
            "for a self-antigen vaccine; antigen escape / immunosuppressive microenvironment for "
            "solid-tumor CAR-T; decoherence for quantum), why the modality historically fails, and "
            "whether THIS design overcomes it — all with citations. When the PM challenges the "
            "science, defend it or concede with evidence.\n"
            "SECTION-AUTHORING: when the PM asks you to WRITE a section of the final investment "
            "report (e.g. the technology/science deep-dive, the industry & competitive-landscape "
            "brief, the financial analysis), do not give a terse summary — AUTHOR a complete, "
            "publication-ready, deeply-detailed section that TEACHES the topic from first "
            "principles (how the technology/process actually works end-to-end; the full "
            "competitive map — who the rivals are, what they are doing, and the specific, "
            "technically-grounded reason THIS company does or does not have a durable edge), every "
            "claim and figure cited. It will be incorporated into the report largely AS YOU WRITE "
            "IT, so make it thorough, rigorous, and self-contained — the depth here is the desk's "
            "entire edge over a generalist analyst, so do not hold back."
        )
        self._tools = toolkit.verification_tool_specs()  # the read/research subset

    def ask(self, question: str, *, context: str = "") -> str:
        """Ask (or follow up with) this analyst; runs a tool loop, returns its analysis."""
        opener = f"PM QUESTION: {question}"
        if context:
            opener += f"\n\nCONTEXT FROM THE PM:\n{context}"
        if not self.messages:
            opener = (f"You are investigating {self.ctx.data.profile.name} ({self.ticker}).\n\n"
                      + opener)
        self.messages.append({"role": "user", "content": opener})
        answer = ""
        for turn in range(self.max_turns):
            try:
                resp = self.client.tool_turn(
                    model=self.model, system=self.system, messages=self.messages,
                    tools=self._tools, ticker=self.ticker, phase="analyst",
                    label=f"analyst:{self.id}:t{turn}", max_tokens=14000, thinking=True)
            except Exception as e:  # pragma: no cover
                log.warning("[%s] analyst %s turn failed: %s", self.ticker, self.id, e)
                break
            self.messages.append({"role": "assistant", "content": resp.content})
            thinking = "".join(getattr(b, "thinking", "") for b in resp.content
                               if getattr(b, "type", None) == "thinking")
            text = "".join(getattr(b, "text", "") for b in resp.content
                           if getattr(b, "type", None) == "text")
            tool_uses = [b for b in resp.content if getattr(b, "type", None) == "tool_use"]
            turn_rec: dict = {"thinking": thinking, "said": text, "pulled": []}
            if not tool_uses:
                self.trace.append(turn_rec)
                answer = text
                break
            results: list[dict] = []
            for tu in tool_uses:
                if tu.name not in _ANALYST_TOOLS:
                    results.append(_tr(tu.id, f"[{tu.name} is not available to an analyst]"))
                    continue
                reply = toolkit.execute(self.ctx, tu.name, dict(tu.input or {}))
                results.append(_tr(tu.id, reply.content))
                turn_rec["pulled"].append({"tool": tu.name, "input": dict(tu.input or {}),
                                           "result": (reply.content or "")[:1500]})
            self.messages.append({"role": "user", "content": results})
            self.trace.append(turn_rec)
        else:
            # Hit the turn cap mid-investigation — ask for its best consolidation.
            answer = answer or "[analyst reached its step budget without a final answer]"
        return answer or "[analyst returned no analysis]"

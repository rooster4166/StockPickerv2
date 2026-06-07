"""The agentic PM orchestrator — a tool-using loop, not a fixed pipeline.

The PM investigates in any order, as many steps as it needs, then calls a terminal
tool. ``reject_early`` drops the name. ``submit_final`` submits the memo + dossier
and triggers a code-enforced RED-TEAM GATE: a decorrelated skeptic attacks the
submission, and if it finds valuation-changing flaws the PM is forced back into the
loop to fix or rebut them — repeating until the memo survives (or a round cap).

Preserves the non-negotiables: the valuation gate (only an AssumptionSet computes a
value), price-blinding (no tool returns the market quote), judgment-in-LLM /
math-in-code, and full per-call audit.
"""

from __future__ import annotations

import json

from microcap_engine.config import AUDIT_DIR, settings
from microcap_engine.llm.client import LLMClient
from microcap_engine.orchestrator import tools as toolkit
from microcap_engine.orchestrator.charter import PM_CHARTER, initial_brief
from microcap_engine.orchestrator.judge import JUDGE_SYSTEM, judge_default, judge_task
from microcap_engine.orchestrator.reviewer import ToolReviewer
from microcap_engine.schemas.dossier import AgenticOutcome, FinalDossier
from microcap_engine.schemas.judge import JudgeReport
from microcap_engine.schemas.name_result import NameData
from microcap_engine.schemas.redteam import RedTeamReport
from microcap_engine.utils.logging import get_logger

log = get_logger(__name__)

_REDTEAM_GATE_SYSTEM = (
    "You are a forensic auditor reviewing a FINAL valuation memo before it is accepted. Find "
    "ERRORS — things that are factually or methodologically WRONG — not mere uncertainty.\n"
    "Set would_change_valuation=TRUE only for a genuine ERROR that, once corrected, moves the "
    "fair value: a mis-stated number (e.g. book value, share count, NEP), the WRONG valuation "
    "method for this business, an ignored claim (preferred/convertible/debt), double-counting, a "
    "math error, or an input contradicted by the filings.\n"
    "ALSO STRESS-TEST THE KEY JUDGMENT INPUTS — these drive the value and no filing 'proves' them, "
    "so YOU must check them against external reality using the research/data tools:\n"
    "  • DISCOUNT RATE / cost of capital — is it built up and reasonable for a $50-300M micro-cap "
    "(risk-free + ERP + beta + a real SIZE/ILLIQUIDITY premium)? An unjustified or too-low rate "
    "(e.g. 7-8% on a tiny illiquid name), or a rate that DOUBLE-COUNTS risk (probability-adjusting "
    "cash flows AND discounting at a venture rate), is a valuation-changing ERROR.\n"
    "  • PROBABILITIES / PoS — for a drug, catalyst, or milestone, independently look up the "
    "published base rate (research) for that phase/indication. A probability that departs from the "
    "defensible base rate WITHOUT a reasoned, evidenced adjustment is a valuation-changing ERROR.\n"
    "  • Peer multiples / growth / margin assumptions that are not supported by the peers or the "
    "company's own history.\n"
    "Do NOT flag would_change_valuation for inherent BUSINESS UNCERTAINTY (will ROE stay high? "
    "will competition intensify?) when the memo ALREADY prices that uncertainty through its "
    "probability weighting and a reasoned, base-rate-anchored input — that is correct analysis. "
    "The line is: a DEFENSIBLE-but-uncertain assumption is fine; one that is INDEFENSIBLE "
    "against external base rates / cost-of-capital norms is an error.\n"
    "IMPORTANT: for the gate to act, a real value-changing error must be marked BOTH "
    "severity='high' AND would_change_valuation=true. Use 'low'/'medium' for everything else.\n"
    "If the memo's numbers tie to the filings AND its discount rate and probabilities are "
    "defensible, say so with no high+would_change concerns. Be exacting; do not manufacture errors "
    "from ordinary, already-priced uncertainty."
)


class AgenticOrchestrator:
    def __init__(
        self,
        data: NameData,
        client: LLMClient,
        run_id: str,
        *,
        model: str | None = None,
        redteam_model: str | None = None,
        max_steps: int = 60,
        max_cost_usd: float = 25.0,
        max_red_rounds: int = 3,   # red-team rejections allowed
        max_judge_rounds: int = 3,  # best-in-existence judge rejections allowed (separate budget)
    ):
        self.data = data
        self.client = client
        self.run_id = run_id
        self.model = model or settings.main_model
        self.redteam_model = redteam_model or settings.redteam_model
        self.max_steps = max_steps
        self.max_cost_usd = max_cost_usd
        self.max_red_rounds = max_red_rounds
        self.max_judge_rounds = max_judge_rounds
        self.ctx = toolkit.ToolContext(
            ticker=data.ticker, data=data, fmp=None, edgar=None,
            client=client, run_id=run_id, model=self.model,
        )
        # Full investigation transcript — every thinking step, tool call + RESULT,
        # valuation, and red-team round — so the run reads like a research team's
        # complete history plus the final paper.
        self.transcript: list[dict] = []
        self._last_red_concerns: list[dict] = []
        self._last_judge: dict = {}
        self._last_red_trace: list[dict] = []
        self._last_judge_trace: list[dict] = []
        # Persistent tool-using reviewers (can verify numbers via the data/web tools);
        # persistence lets the PM and the SAME reviewer debate across rounds.
        self._red_team_reviewer: ToolReviewer | None = None
        self._judge_reviewer: ToolReviewer | None = None

    def bind_providers(self, fmp, edgar) -> AgenticOrchestrator:
        self.ctx.fmp = fmp
        self.ctx.edgar = edgar
        return self

    def _cost(self) -> float:
        return self.client.audit.summary(self.data.ticker)["cost_usd"]

    def analyze(self) -> AgenticOutcome:
        t = self.data.ticker
        tools = toolkit.tool_specs()
        messages: list[dict] = [{"role": "user", "content": initial_brief(self.data)}]
        red_rounds = 0
        judge_rounds = 0
        tool_calls = 0

        for step in range(self.max_steps):
            if self._cost() > self.max_cost_usd:
                messages.append({"role": "user", "content":
                                 "Cost budget reached. Call submit_final NOW with your best, "
                                 "fully-justified valuation (or reject_early if truly no case)."})
            resp = self.client.tool_turn(
                model=self.model, system=PM_CHARTER, messages=messages, tools=tools,
                ticker=t, phase="pm", label=f"pm:step{step}",
                max_tokens=20000, thinking=True,  # room for a long, comprehensive memo
            )
            messages.append({"role": "assistant", "content": resp.content})
            thinking = "".join(getattr(b, "thinking", "") or "" for b in resp.content
                               if getattr(b, "type", None) == "thinking")
            said = "".join(getattr(b, "text", "") or "" for b in resp.content
                           if getattr(b, "type", None) == "text")
            turn = {"step": step, "thinking": thinking, "said": said, "calls": []}
            self.transcript.append(turn)

            tool_uses = [b for b in resp.content if getattr(b, "type", None) == "tool_use"]
            if not tool_uses:
                messages.append({"role": "user", "content":
                                 "Keep going: use tools to investigate, then submit_final or "
                                 "reject_early. Do not answer in plain text."})
                continue

            tool_results: list[dict] = []
            for tu in tool_uses:
                tool_calls += 1
                reply = toolkit.execute(self.ctx, tu.name, dict(tu.input or {}))

                if reply.terminal == "reject":
                    log.info("[%s] PM reject_early: %s", t, reply.payload.get("reason", "")[:120])
                    turn["calls"].append({"tool": "reject_early", "input": tu.input,
                                          "result": reply.payload.get("reason", "")})
                    return self._finish(AgenticOutcome(
                        ticker=t, action="drop",
                        reject_reason=reply.payload.get("reason", ""), tool_calls=tool_calls))

                if reply.terminal == "submit":
                    accepted, result_text, outcome, gate = self._handle_submit(
                        reply.payload, red_rounds, judge_rounds, tool_calls)
                    turn["calls"].append({
                        "tool": "submit_final",
                        "input": {"dossier": reply.payload.get("dossier_raw")},
                        "result": result_text, "red_team": self._last_red_concerns,
                        "judge": dict(self._last_judge),
                        "red_team_trace": self._last_red_trace,
                        "judge_trace": self._last_judge_trace})
                    tool_results.append(_tr(tu.id, result_text))
                    if accepted:
                        return self._finish(outcome)
                    if gate == "red":
                        red_rounds += 1
                    elif gate == "judge":
                        judge_rounds += 1
                else:
                    turn["calls"].append({"tool": tu.name, "input": tu.input,
                                          "result": reply.content})
                    tool_results.append(_tr(tu.id, reply.content))

            messages.append({"role": "user", "content": tool_results})

        # Ran out of steps without an accepted submission — return best effort.
        log.warning("[%s] PM hit max_steps without accepted submission", t)
        return self._finish(self._best_effort(red_rounds, tool_calls))

    # ── submission gates: red-team (errors) then best-in-existence judge ────
    def _handle_submit(self, payload, red_rounds, judge_rounds, tool_calls):
        """Returns (accepted, message, outcome, gate) where gate in {red, judge, None}."""
        t = self.data.ticker
        memo = payload.get("markdown_memo", "")
        try:
            dossier = FinalDossier.model_validate(payload.get("dossier_raw", {}))
        except Exception as e:
            return (False, f"submit_final REJECTED — the dossier is invalid: {e}. Fix it and "
                           f"call submit_final again.", None, None)

        # GATE 1 — red-team: real errors only (the prompt forbids flagging priced uncertainty).
        report = self._red_team(memo, dossier)
        blockers = [c for c in report.concerns
                    if c.severity == "high" and c.would_change_valuation]
        if blockers and red_rounds < self.max_red_rounds:
            concerns_txt = "\n".join(
                f"- [{c.category}] {c.description} (evidence: {c.evidence})" for c in blockers)
            log.info("[%s] red-team REJECTED (round %d): %d blockers", t, red_rounds + 1,
                     len(blockers))
            return (False,
                    "The REVIEWER (same person each round) found ERRORS that change the valuation "
                    "(these are factual/method errors, not ordinary uncertainty):\n" + concerns_txt
                    + "\n\nIn your revised memo, add a '## Response to Reviewer' section that "
                    "addresses EACH concern point-by-point: either the correction you made, OR an "
                    "evidence-based rebuttal for why you are standing by your analysis. The SAME "
                    "reviewer will read your responses and CONCEDE the points you have adequately "
                    "answered. Then call submit_final again.", None, "red")

        # GATE 2 — independent best-in-existence judge (tool-verified fact-check +
        # completeness/rigor + CONVICTION: would a skeptical elite investor act on it).
        if self._judge_reviewer is None:
            self._judge_reviewer = ToolReviewer(
                self.client, self.ctx, system=JUDGE_SYSTEM, output_schema=JudgeReport,
                phase="judge", model=self.model, default_factory=judge_default)
        judge = self._judge_reviewer.review(judge_task(self.data, memo, dossier))
        self._last_judge_trace = list(self._judge_reviewer.last_trace)
        self._last_judge = {
            "best": judge.best_in_existence, "score": judge.overall_score,
            "would_act": judge.would_act_on_it,
            "factual_errors": judge.factual_errors, "gaps": judge.gaps_vs_best_in_class,
            "verdict": judge.verdict,
        }
        if not judge.best_in_existence and judge_rounds < self.max_judge_rounds:
            log.info("[%s] judge NOT best-in-existence (%d/100, round %d): %d errors, %d gaps",
                     t, judge.overall_score, judge_rounds + 1,
                     len(judge.factual_errors), len(judge.gaps_vs_best_in_class))
            parts = [f"The INDEPENDENT JUDGE has NOT yet rated this best-in-existence "
                     f"(score {judge.overall_score}/100). Not accepted until it is the best, most "
                     f"accurate, most complete valuation of this company that could exist."]
            if judge.factual_errors:
                parts.append("FACTUAL ERRORS — verify against the data tools and FIX:\n"
                             + "\n".join(f"- {e}" for e in judge.factual_errors))
            if judge.gaps_vs_best_in_class:
                parts.append("GAPS vs best-in-class — close every one (deepen/explain/add):\n"
                             + "\n".join(f"- {g}" for g in judge.gaps_vs_best_in_class))
            parts.append("Correct the numbers, deepen the memo, then call submit_final again.")
            return (False, "\n\n".join(parts), None, "judge")

        unresolved = [c.description for c in blockers]
        outcome = AgenticOutcome(
            ticker=t, action="evaluated", dossier=dossier, memo_markdown=memo,
            red_team_rounds=red_rounds, unresolved_concerns=unresolved,
            judge_approved=judge.best_in_existence, judge_score=judge.overall_score,
            judge_gaps=judge.gaps_vs_best_in_class, tool_calls=tool_calls)
        log.info("[%s] ACCEPTED — judge %d/100, best_in_existence=%s",
                 t, judge.overall_score, judge.best_in_existence)
        return (True, "ACCEPTED.", outcome, None)

    def _red_team(self, memo: str, dossier: FinalDossier) -> RedTeamReport:
        # The SAME tool-using reviewer across rounds (persistent): it can VERIFY the
        # memo's numbers via the data/web tools, remembers its own objections, and
        # CONCEDES when the PM fixes them or rebuts with evidence.
        vals = "\n".join(f"- {v.method.value}: {v.fair_value_per_share}/sh ({v.notes})"
                         for v in self.ctx.valuations[-5:])
        body = (
            f"STRUCTURED DOSSIER:\n{dossier.model_dump_json(indent=2)}\n\n"
            f"VALUATIONS COMPUTED (code):\n{vals}\n\n"
            f"FULL MEMO (read its 'Response to Reviewer' section if present):\n{memo[:40000]}"
        )
        if self._red_team_reviewer is None:
            self._red_team_reviewer = ToolReviewer(
                self.client, self.ctx, system=_REDTEAM_GATE_SYSTEM, output_schema=RedTeamReport,
                phase="redteam_gate", model=self.redteam_model,
                default_factory=lambda: RedTeamReport(
                    would_break_thesis=False, summary="reviewer did not emit; no blockers"))
            msg = ("Independently VERIFY this memo's key numbers/claims with the data and research "
                   "tools (check common equity/book value, share count, margins, peer multiples "
                   "against the filings), then review for ERRORS (not uncertainty).\n\n" + body)
        else:
            msg = (
                "This is the author's REVISED memo responding to YOUR prior review. Re-verify "
                "anything you flagged. For EACH concern you previously raised: if it is now "
                "corrected, OR the author rebuts it with specific evidence/reasoning that you find "
                "convincing, CONCEDE and drop it. Keep a concern only if it remains a genuine "
                "valuation-changing ERROR despite the fix/rebuttal (plus any NEW one). If nothing "
                "material remains, return NO high-severity would_change_valuation concerns so the "
                "report can finalize. Be fair: do not re-raise a point adequately answered.\n\n"
                + body
            )
        report = self._red_team_reviewer.review(msg)
        self._last_red_trace = list(self._red_team_reviewer.last_trace)
        self._last_red_concerns = [
            {"category": c.category, "severity": c.severity, "description": c.description,
             "evidence": c.evidence, "would_change_valuation": c.would_change_valuation}
            for c in report.concerns
        ]
        return report

    def _best_effort(self, red_rounds: int, tool_calls: int) -> AgenticOutcome:
        """No accepted submission within budget — return whatever valuation exists."""
        last = self.ctx.last_valuation
        if last is None:
            return AgenticOutcome(ticker=self.data.ticker, action="drop",
                                  reject_reason="No valuation reached within budget.",
                                  tool_calls=tool_calls)
        dossier = FinalDossier(
            fair_value_per_share=last.fair_value_per_share,
            fair_value_low=last.fair_value_p10 or last.fair_value_per_share,
            fair_value_high=last.fair_value_p90 or last.fair_value_per_share,
            valuation_method=last.method.value, confidence=0.3,
            thesis_summary="Budget reached before a finalized memo; last computed value used.")
        return AgenticOutcome(ticker=self.data.ticker, action="evaluated", dossier=dossier,
                              memo_markdown="[incomplete — budget reached]",
                              red_team_rounds=red_rounds, tool_calls=tool_calls)


    # ── transcript ─────────────────────────────────────────────────────────
    def _finish(self, outcome: AgenticOutcome) -> AgenticOutcome:
        """Write the full investigation transcript, then return the outcome."""
        try:
            path = AUDIT_DIR / self.run_id / f"{self.data.ticker}.transcript.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(self._render_transcript(outcome), encoding="utf-8", newline="\n")
            outcome.transcript_path = str(path)
        except Exception as e:  # pragma: no cover
            log.warning("[%s] transcript write failed: %s", self.data.ticker, e)
        return outcome

    def _render_transcript(self, outcome: AgenticOutcome) -> str:
        d = self.data
        out: list[str] = [
            f"# {d.profile.name} ({d.ticker}) — Full Investigation Transcript",
            "\n*The complete research history: every step the PM took, what each tool returned, "
            "every valuation computed, and every red-team round — followed by the final memo.*\n",
            f"\n**Outcome:** {outcome.action} | **Red-team rounds:** {outcome.red_team_rounds} | "
            f"**Tool calls:** {outcome.tool_calls}\n",
            "\n---\n",
        ]
        for turn in self.transcript:
            out.append(f"\n## Step {turn['step']}")
            if turn.get("thinking"):
                out.append("\n**🧠 PM reasoning:**\n\n> "
                           + turn["thinking"].strip().replace("\n", "\n> "))
            if turn.get("said"):
                out.append(f"\n**PM note:** {turn['said'].strip()}")
            for c in turn["calls"]:
                inp = json.dumps(c["input"], default=str)[:1500] if c.get("input") else ""
                out.append(f"\n### ⚙️ `{c['tool']}`")
                if inp and c["tool"] not in ("submit_final",):
                    out.append(f"\n_input:_ `{inp}`")
                if c["tool"] == "submit_final":
                    out.append(f"\n_gate verdict:_ {c['result']}")
                    if c.get("red_team_trace"):
                        out.append("\n**🔬 Red-team's own verification (how it checked the "
                                   "numbers):**")
                        out.extend(self._render_reviewer_trace(c["red_team_trace"]))
                    if c.get("red_team"):
                        out.append("\n_red-team concerns this round:_")
                        for rc in c["red_team"]:
                            flag = " [CHANGES VALUATION]" if rc.get("would_change_valuation") else ""  # noqa: E501
                            out.append(f"\n- [{rc['severity']}/{rc['category']}]{flag} "
                                       f"{rc['description']}")
                    if c.get("judge_trace"):
                        out.append("\n**🔬 Judge's own verification (independent fact-check):**")
                        out.extend(self._render_reviewer_trace(c["judge_trace"]))
                    j = c.get("judge") or {}
                    if j:
                        out.append(f"\n_independent judge:_ score {j.get('score')}/100, "
                                   f"best_in_existence={j.get('best')}")
                        for e in j.get("factual_errors") or []:
                            out.append(f"\n  - FACTUAL ERROR: {e}")
                        for g in j.get("gaps") or []:
                            out.append(f"\n  - GAP: {g}")
                else:
                    res = str(c.get("result", ""))[:6000]
                    out.append(f"\n_returned:_\n\n```\n{res}\n```")
        out.append("\n\n---\n\n# FINAL CONSOLIDATED MEMO\n")
        return self._join_transcript(out, outcome)

    @staticmethod
    def _render_reviewer_trace(trace: list[dict]) -> list[str]:
        """Render a reviewer's verification turns: its reasoning + each check it ran."""
        lines: list[str] = []
        for tr in trace:
            if tr.get("thinking"):
                lines.append("\n> _reviewer reasoning:_ "
                             + tr["thinking"].strip()[:1200].replace("\n", "\n> "))
            for ck in tr.get("checks", []):
                inp = json.dumps(ck.get("input", {}), default=str)[:400]
                res = str(ck.get("result", ""))[:1200]
                lines.append(f"\n  - 🔎 checked `{ck['tool']}` {inp}\n    → `{res}`")
            if tr.get("said"):
                lines.append(f"\n  _reviewer note:_ {tr['said'].strip()[:800]}")
        return lines

    def _join_transcript(self, out: list[str], outcome: AgenticOutcome) -> str:
        out.append(outcome.memo_markdown or "*(no memo — see outcome)*")
        if outcome.dossier:
            out.append("\n\n---\n\n## Structured Dossier\n```json\n"
                       + outcome.dossier.model_dump_json(indent=2) + "\n```")
        return "\n".join(out)


def _tr(tool_use_id: str, content: str) -> dict:
    return {"type": "tool_result", "tool_use_id": tool_use_id, "content": content or "(empty)"}

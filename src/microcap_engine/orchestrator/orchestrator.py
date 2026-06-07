"""The orchestrator (PM).

Constructed with a ``NameData`` bundle that has NO market quote — price-blinding
is enforced by the type system, not by discipline. ``analyze()`` runs the seven
phases in strict dependency order, threading ``OrchestratorState``, and returns a
``DeepDiveResult``. The market price is never joined here; that happens later, in
the portfolio layer.
"""

from __future__ import annotations

from microcap_engine.llm.client import LLMClient
from microcap_engine.orchestrator.phases import runners
from microcap_engine.orchestrator.state import OrchestratorConfig, OrchestratorState
from microcap_engine.schemas.name_result import DeepDiveResult, NameData
from microcap_engine.utils.logging import get_logger

log = get_logger(__name__)


class Orchestrator:
    def __init__(
        self,
        data: NameData,
        config: OrchestratorConfig,
        client: LLMClient,
        run_id: str,
    ):
        # `data` is a NameData — it structurally cannot carry a Quote.
        self.data = data
        self.config = config
        self.client = client
        self.run_id = run_id
        self.state = OrchestratorState(run_id=run_id, ticker=data.ticker, config=config)

    def analyze(self) -> DeepDiveResult:
        s = self.state
        t = self.data.ticker
        log.info("[%s/%s] phase 0 transcripts", t, self.config.label)
        s.transcripts = runners.run_phase0_transcripts(self.data, s, self.client)
        log.info("[%s/%s] phase 1 financials", t, self.config.label)
        s.financials = runners.run_phase1_financials(self.data, s, self.client)
        log.info("[%s/%s] phase 2 business", t, self.config.label)
        s.business = runners.run_phase2_business(self.data, s, self.client)
        log.info("[%s/%s] phase 3 industry", t, self.config.label)
        s.industry = runners.run_phase3_industry(self.data, s, self.client)
        log.info("[%s/%s] phase 4 news", t, self.config.label)
        s.news = runners.run_phase4_news(self.data, s, self.client)
        log.info("[%s/%s] phase 5 consolidate (gate)", t, self.config.label)
        s.assumption_set = runners.run_phase5_consolidate(self.data, s, self.client)
        log.info("[%s/%s] phase 6 valuation (price-blinded)", t, self.config.label)
        s.valuation = runners.run_phase6_valuation(s)  # gate enforced inside
        log.info("[%s/%s] phase 7 red-team", t, self.config.label)
        s.redteam = runners.run_phase7_redteam(self.data, s, self.client)

        return DeepDiveResult(
            ticker=t,
            config_label=self.config.label,
            transcripts=s.transcripts,
            financials=s.financials,
            business=s.business,
            industry=s.industry,
            news=s.news,
            assumption_set=s.assumption_set,
            valuation=s.valuation,
            redteam=s.redteam,
        )

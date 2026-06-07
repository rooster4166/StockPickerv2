# Final Reports

Published investment memos and full investigation transcripts from the Micro-Cap
Value Engine, one folder per validation run. Each company folder contains:

- `<TICKER>.memo.md` — the feature-length, HBR-grade investment memo (the headline
  Fair Market Value, the no-growth floor, the probability-weighted outcome
  distribution, and the full reasoning).
- `<TICKER>.transcript.md` — the complete investigation history: every step the PM
  took, what each tool/analyst returned, every valuation computed, and every
  red-team / judge round, followed by the final memo.
- `<TICKER>.dossier.json` — the structured output (fair value, confidence band,
  method, citations, judge verdict).

These are the price-blinded analyses; the market-price comparison is joined only at
the portfolio layer.

## Validation set (five deliberately different value-driver archetypes)

| Ticker | Company | Archetype | Tests |
|--------|---------|-----------|-------|
| ANIX | Anixa Biosciences | Pre-revenue biotech (science: biology) | rNPV / base-rate PoS / science understanding |
| KINS | Kingstone Companies | P&C insurer (financial / spread) | excess_returns (warranted P/B × ROE) |
| FLWS | 1-800-Flowers | Consumer brand (proven compounder) | DCF / multiples on real cash flows |
| ACRE | Ares Commercial RE | Mortgage REIT (asset / book / NAV) | NAV / book-yield |
| ARQQ | Arqit Quantum | Quantum-encryption deep-tech (science: physics) | science path generalizes beyond biology |

"""Sector/industry COMPLEXITY-BARRIER prior — the dominant edge term.

How much specialized domain knowledge does valuing a business in this sector require,
that a generalist micro-cap analyst (and the thin coverage) would lack? Science and
deep-tech sit at the top (the LLM can read the biology/physics no one else will);
simple consumer/retail/utility businesses at the bottom (anyone can value them). This
is a coarse PRIOR — the Sonnet triage refines it per-business (e.g. a 'Software-
Infrastructure' label hiding a quantum-cryptography company). Empirically seeded from
the validation set (biotech/quantum/under-covered-insurer high; REIT/retail low).
"""

from __future__ import annotations

# Base score by sector (0..1). Refined by industry keywords below.
_SECTOR_BASE = {
    "healthcare": 0.80,
    "technology": 0.65,
    "basic materials": 0.55,
    "energy": 0.50,
    "industrials": 0.45,
    "financial services": 0.45,
    "communication services": 0.40,
    "consumer cyclical": 0.30,
    "consumer defensive": 0.28,
    "real estate": 0.30,
    "utilities": 0.20,
}

# Industry keyword -> hard override/boost (matched as substrings, case-insensitive).
# High = the value genuinely turns on hard-to-understand science/tech/structure.
_INDUSTRY_HIGH = {  # -> 0.95
    "biotechnology", "drug manufacturers", "diagnostics", "gene", "therapeut",
    "pharmaceutical", "medical device", "semiconductor", "quantum",
}
_INDUSTRY_MED_HIGH = {  # -> 0.70
    "software - infrastructure", "aerospace", "defense", "specialty chemical",
    "electronic", "scientific", "space", "fuel cell", "battery", "photonic",
    "insurance - specialty", "insurance - property", "insurance - reinsurance",
}
_INDUSTRY_LOW = {  # -> 0.22 (well-trodden, easy to value, usually competently covered)
    "reit", "bank", "retail", "restaurant", "grocery", "apparel", "footwear",
    "hotel", "airline", "utilities", "mortgage", "thrift", "savings",
}


def complexity_prior(sector: str | None, industry: str | None) -> float:
    """A 0..1 complexity-barrier prior from sector + industry text."""
    ind = (industry or "").lower()
    for kw in _INDUSTRY_HIGH:
        if kw in ind:
            return 0.95
    # LOW keywords win over the medium boosts (a "mortgage REIT" is low even though
    # 'real estate' isn't the lowest sector) — these are the efficiently-covered kinds.
    for kw in _INDUSTRY_LOW:
        if kw in ind:
            base = _SECTOR_BASE.get((sector or "").lower(), 0.3)
            return min(base, 0.25)
    for kw in _INDUSTRY_MED_HIGH:
        if kw in ind:
            return 0.70
    return _SECTOR_BASE.get((sector or "").lower(), 0.35)

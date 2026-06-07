"""Price-blinding: nothing the orchestrator touches may import ``Quote``.

The market price must not reach the analysis. We enforce this structurally:
  1. ``NameData`` (what the orchestrator receives) has no price field.
  2. No module under ``orchestrator/``, ``gate/``, or ``ensemble/`` imports Quote.
  3. ``Quote`` is imported only by the portfolio/runner layers.
"""

from __future__ import annotations

import ast
from pathlib import Path

import microcap_engine
from microcap_engine.schemas.name_result import NameData

SRC = Path(microcap_engine.__file__).parent
BLINDED_DIRS = ["orchestrator", "gate", "ensemble"]


def test_name_data_has_no_price_field():
    assert "price" not in NameData.model_fields
    assert "quote" not in NameData.model_fields


def _references_quote(py: Path) -> bool:
    """True if the module imports or *uses* the Quote symbol (AST-based, so
    docstrings/comments mentioning the word 'quote' don't count)."""
    tree = ast.parse(py.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if any(alias.name == "Quote" for alias in node.names):
                return True
        if isinstance(node, ast.Name) and node.id == "Quote":
            return True
        if isinstance(node, ast.Attribute) and node.attr == "Quote":
            return True
    return False


def test_blinded_dirs_never_import_quote():
    offenders = [
        str(py.relative_to(SRC))
        for d in BLINDED_DIRS
        for py in (SRC / d).rglob("*.py")
        if _references_quote(py)
    ]
    assert not offenders, f"price-blinding violated; Quote referenced in: {offenders}"


def test_portfolio_layer_is_allowed_to_use_quote():
    # Sanity: the portfolio/runner layer is where the price legitimately enters.
    book = (SRC / "portfolio" / "book.py").read_text(encoding="utf-8")
    assert "price" in book.lower()

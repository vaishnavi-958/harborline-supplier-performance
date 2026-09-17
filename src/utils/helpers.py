"""Shared helpers for configuration, dates, and safe division."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_yaml(path: Path | str) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def load_config() -> dict[str, Any]:
    return load_yaml(ROOT / "config" / "config.yaml")


def load_supplier_profiles() -> dict[str, Any]:
    return load_yaml(ROOT / "config" / "supplier_profiles.yaml")


def load_scoring_config() -> dict[str, Any]:
    return load_yaml(ROOT / "config" / "scoring_config.yaml")


def project_path(*parts: str) -> Path:
    return ROOT.joinpath(*parts)


def safe_div(numerator: float, denominator: float, default: float = 0.0) -> float:
    if denominator == 0 or denominator is None:
        return default
    return numerator / denominator


def clip(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))

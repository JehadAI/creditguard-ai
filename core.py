"""Cached resources + session-state helpers shared by all pages."""
import time
from importlib import metadata

import streamlit as st

from detector import FraudDetector


@st.cache_resource(show_spinner="Loading model…")
def get_detector() -> FraudDetector:
    return FraudDetector()


def init_state() -> None:
    st.session_state.setdefault("history", [])          # one entry per analysis run


def log_analysis(source: str, total: int, fraud: int) -> None:
    st.session_state.setdefault("history", []).append(
        dict(time=time.strftime("%H:%M:%S"), source=source, transactions=total,
             fraud=fraud, normal=total - fraud)
    )


def session_totals() -> tuple[int, int, int]:
    h = st.session_state.get("history", [])
    total = sum(x["transactions"] for x in h)
    fraud = sum(x["fraud"] for x in h)
    return total, fraud, total - fraud


def version_mismatches(report: dict) -> list[str]:
    """Pickles are only guaranteed to load with the library versions used for training."""
    out = []
    for pkg in ("scikit-learn", "xgboost"):
        trained = report.get("versions", {}).get(pkg)
        try:
            installed = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            installed = None
        if trained and installed and trained != installed:
            out.append(f"{pkg}: trained with {trained}, installed {installed}")
    return out

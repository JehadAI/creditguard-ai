"""Pure-Python inference layer (no Streamlit imports so it can be unit-tested).

It applies EXACTLY the same preprocessing as the training notebook:
    raw row -> reorder columns to FEATURE_ORDER -> RobustScaler on [Amount, Time]
            -> model.predict_proba -> compare with the saved threshold.
"""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

ARTIFACT_DIR = Path(__file__).parent / "artifacts"


def risk_level(p: float, threshold: float) -> str:
    """Risk band derived from the saved decision threshold.

    High   : p >= threshold          (the model flags it as fraud)
    Medium : p >= threshold / 2      (below the threshold but clearly elevated)
    Low    : otherwise
    """
    if p >= threshold:
        return "High"
    if p >= threshold / 2:
        return "Medium"
    return "Low"


class FraudDetector:
    def __init__(self, folder: Path | str = ARTIFACT_DIR):
        folder = Path(folder)
        self.model = joblib.load(folder / "fraud_model.joblib")
        self.scaler = joblib.load(folder / "scaler.joblib")
        self.cfg = joblib.load(folder / "preprocessing_config.joblib")
        self.threshold: float = float(self.cfg["threshold"])
        self.feature_order: list[str] = list(self.cfg["feature_order"])
        self.scale_cols: list[str] = list(self.cfg["scale_cols"])
        with open(folder / "model_report.json") as f:
            self.report: dict = json.load(f)

    # ---------------------------------------------------------------- validation
    def missing_columns(self, df: pd.DataFrame) -> list[str]:
        return [c for c in self.feature_order if c not in df.columns]

    # ---------------------------------------------------------------- inference
    def _prepare(self, raw: pd.DataFrame) -> pd.DataFrame:
        X = raw[self.feature_order].astype(float).copy()          # same order as training
        X[self.scale_cols] = self.scaler.transform(X[self.scale_cols])  # same scaler (fit on train only)
        return X

    def predict_proba(self, raw: pd.DataFrame) -> np.ndarray:
        return self.model.predict_proba(self._prepare(raw))[:, 1]

    def predict(self, raw: pd.DataFrame) -> pd.DataFrame:
        p = self.predict_proba(raw)
        out = pd.DataFrame(index=raw.index)
        out["fraud_probability"] = p
        out["normal_probability"] = 1.0 - p
        out["prediction"] = np.where(p >= self.threshold, "Fraud", "Normal")
        out["risk_level"] = [risk_level(v, self.threshold) for v in p]
        return out

"""
termora/utils/model_loader.py
==============================
Loads the saved bank_marketing_model.pkl and model_meta.json once
and caches them for the Streamlit session.
"""

import json
import joblib
import streamlit as st
import pandas as pd
from termora.config import MODEL_PATH, META_PATH, FEATURE_ORDER


@st.cache_resource(show_spinner=False)
def load_model():
    """Load and cache the production pipeline (preprocessor + classifier)."""
    try:
        pipeline = joblib.load(MODEL_PATH)
        return pipeline
    except FileNotFoundError:
        st.error(f"Model file not found: {MODEL_PATH}")
        return None


@st.cache_resource(show_spinner=False)
def load_meta():
    """Load and cache model metadata."""
    try:
        with open(META_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def predict(input_dict: dict) -> tuple[int, float]:
    """
    Run prediction on a single customer dictionary.

    Parameters
    ----------
    input_dict : dict
        Keys are human-readable feature names (matching FEATURE_ORDER).

    Returns
    -------
    (class_label, probability_of_yes)
    """
    pipeline = load_model()
    if pipeline is None:
        raise RuntimeError("Model could not be loaded.")

    # Handle alias if present
    d = dict(input_dict)
    if "Contact Day of Week" in d and "Contact Day" not in d:
        d["Contact Day"] = d["Contact Day of Week"]

    # Build DataFrame in the exact column order expected by the pipeline
    df = pd.DataFrame([d])[FEATURE_ORDER]

    pred  = int(pipeline.predict(df)[0])
    proba = float(pipeline.predict_proba(df)[0][1])
    return pred, proba

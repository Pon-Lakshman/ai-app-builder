import os
import requests
import streamlit as st


def get_api_base_url():
    # First check environment variables
    value = os.getenv("API_BASE_URL")

    if value:
        return value.rstrip("/")

    # Then check Streamlit Cloud secrets
    try:
        value = st.secrets.get("API_BASE_URL")

        if value:
            return value.rstrip("/")
    except Exception:
        pass

    # Local development fallback
    return "http://127.0.0.1:8000"


def call_api(
    endpoint: str,
    prompt: str,
    timeout: int = 180,
):
    api_base_url = get_api_base_url()

    url = f"{api_base_url}{endpoint}"

    response = requests.post(
        url,
        json={"prompt": prompt},
        timeout=timeout,
    )

    response.raise_for_status()

    data = response.json()

    return data["result"]
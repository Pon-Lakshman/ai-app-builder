import os

import requests


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)


def call_api(
    endpoint: str,
    prompt: str,
    timeout: int = 180,
):

    url = f"{API_BASE_URL}{endpoint}"

    response = requests.post(
        url,
        json={
            "prompt": prompt,
        },
        timeout=timeout,
    )

    response.raise_for_status()

    data = response.json()

    return data["result"]

import os

from huggingface_hub import InferenceClient


MODEL_NAME = "Qwen/Qwen3-4B-Instruct-2507"


def get_hf_client():

    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:

        raise RuntimeError(
            "HF_TOKEN environment variable is not configured."
        )

    return InferenceClient(
        api_key=hf_token
    )


def generate_response(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 800,
):

    client = get_hf_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )

    return response.choices[0].message.content
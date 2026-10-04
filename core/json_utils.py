import json


def parse_ai_json(response: str):
    """
    Extract and parse JSON from an AI response.

    Handles:
    - Normal JSON
    - ```json ... ``` responses
    - JSON surrounded by extra text
    """

    response = response.strip()

    # -----------------------------------------
    # Direct JSON
    # -----------------------------------------

    try:
        return json.loads(response)

    except json.JSONDecodeError:
        pass

    # -----------------------------------------
    # Remove Markdown code fences
    # -----------------------------------------

    if response.startswith("```"):

        lines = response.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        response = "\n".join(lines).strip()

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            pass

    # -----------------------------------------
    # Extract JSON object from surrounding text
    # -----------------------------------------

    start = response.find("{")
    end = response.rfind("}")

    if start != -1 and end != -1 and end > start:

        json_text = response[start:end + 1]

        try:
            return json.loads(json_text)

        except json.JSONDecodeError:
            pass

    # -----------------------------------------
    # Fallback
    # -----------------------------------------

    return {
        "raw_response": response
    }
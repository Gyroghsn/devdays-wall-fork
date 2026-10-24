"""Shared rules for participant cards, used by the Welcome Bot and the site builder."""
import json
import re

# Allowed fields and their maximum length.
FIELDS = {"name": 40, "city": 40, "emoji": 8, "fun_fact": 140}

QUIZ_FILE = "quiz/answers.md"
USERNAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,38})$")

EXAMPLE = """```json
{
  "name": "Sarah",
  "city": "Sfax",
  "emoji": "🚀",
  "fun_fact": "I once fixed a bug by deleting a semicolon"
}
```"""


def card_path(username):
    return f"participants/{username.lower()}.json"


def parse_card(text):
    """Return (card, errors). `card` is None when there are errors."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return None, [
            f"The file is not valid JSON (line {e.lineno}, column {e.colno}: {e.msg}). "
            "Check your commas and double quotes."
        ]
    if not isinstance(data, dict):
        return None, ["The file must contain one JSON object, starting with `{` and ending with `}`."]

    errors = []
    for key, max_len in FIELDS.items():
        value = data.get(key)
        if value is None:
            errors.append(f"Missing field `{key}`.")
        elif not isinstance(value, str) or not value.strip():
            errors.append(f"`{key}` must be some text between double quotes.")
        elif len(value) > max_len:
            errors.append(f"`{key}` is too long ({len(value)} characters, max {max_len}).")

    for key in data:
        if key in FIELDS:
            continue
        hint = next((f for f in FIELDS if f == key.strip().lower().replace(" ", "_")), None)
        if hint:
            errors.append(f"Unknown field `{key}`. Did you mean `{hint}`?")
        else:
            errors.append(f"Unknown field `{key}`. Allowed fields: {', '.join(f'`{f}`' for f in FIELDS)}.")

    if errors:
        return None, errors
    return {key: data[key].strip() for key in FIELDS}, []

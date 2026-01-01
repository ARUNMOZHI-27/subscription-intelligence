import subprocess
from config import OLLAMA_MODEL, OLLAMA_TIMEOUT


def explain_alert(sub: dict, message: str) -> str:
    name = sub.get("name", "this subscription")
    cost = sub.get("monthly_cost", 0)
    yearly = cost * 12 if cost else None

    prompt = f"""
You are a friendly, calm personal finance assistant.

Context:
- Subscription: {name}
- Monthly cost: ₹{cost}
- Alert: {message}

Guidelines:
- Be concise (5–7 lines max)
- Sound human, not formal
- Do NOT repeat the alert message verbatim
- If cost exists, mention yearly cost briefly
- End with ONE gentle question or suggestion
- No bullet-point essays

Tone example:
"Looks like…, This means…, You might want to…, Want help with…?"

Now explain this alert to the user.
"""




    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=OLLAMA_TIMEOUT,
            encoding="utf-8",
            errors="ignore"
        )

        if result.returncode != 0 or not result.stdout.strip():
            return f"(LLM unavailable) {message}"

        return result.stdout.strip()

    except Exception:
        return f"(LLM unavailable) {message}"

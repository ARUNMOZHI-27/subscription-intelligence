# llm_chat.py
from llm_explainer import explain_alert

def chat_explain(context: str) -> str:
    prompt = (
        "You are a friendly, calm personal subscription assistant.\n"
        "Explain briefly, clearly, and like talking to a human.\n"
        "No long paragraphs. No formal tone.\n\n"
        f"{context}"
    )

    return explain_alert(
        {"name": "Chat Assistant"},
        prompt
    )
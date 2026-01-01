from rich.table import Table
from rich.console import Console

from conversation_memory import ConversationMemory
from subscription_mcp import (
    list_subscriptions,
    analyze_spend,
    recommend_savings,
    get_monthly_summary,
    export_calendar_file,
    status
    
)
from llm_explainer import explain_alert

console = Console()
memory = ConversationMemory()

def _render_subscriptions(subs):
    table = Table(title="📦 Active Subscriptions")
    table.add_column("Name", style="cyan")
    table.add_column("₹ / Month", justify="right")
    table.add_column("Category", style="green")
    table.add_column("Trial End", style="yellow")
    table.add_column("Renewal", style="red")

    for s in subs:
        table.add_row(
            s["name"],
            str(s.get("monthly_cost", 0)),
            s.get("category", "-"),
            s.get("trial_end_date") or "-",
            s.get("renewal_date") or "-"
        )

    console.print(table)

def route_user_message(message: str) -> str:
    msg = message.lower().strip()

    #-----------------------
    STATUS
    # -----------------------
    if "status" in msg:
        status = status()
        return (
            f"🧠 Agent running: {'✅' if status['running'] else '❌'}\n"
            f"🕒 Last check: {status['last_run']}"
        )

    # -----------------------
    # LIST SUBSCRIPTIONS
    # -----------------------
    if "subscription" in msg:
        subs = list_subscriptions()
        if not subs:
            return "You don’t have any subscriptions yet."

        _render_subscriptions(subs)
        return "Here’s the list above."

    # -----------------------
    # SPEND
    # -----------------------
    if any(x in msg for x in ["spend", "cost", "money", "salary"]):
        data = analyze_spend()
        explanation = explain_alert(
            {"name": "Spending", "monthly_cost": data["total_monthly_spend"]},
            f"Total spend: ₹{data['total_monthly_spend']}"
        )
        return (
            f"💰 Total monthly spend: ₹{data['total_monthly_spend']}\n\n"
            f"{explanation}"
        )

    # -----------------------
    # MONTHLY SUMMARY
    # -----------------------
    if "summary" in msg:
        return get_monthly_summary()

    # -----------------------
    # SAVINGS
    # -----------------------
    if any(x in msg for x in ["save", "reduce", "cancel"]):
        result = recommend_savings()
        return result.get("recommendations", "No suggestions right now.")

    # -----------------------
    # FALLBACK
    # -----------------------
    return (
        "I can help you manage subscriptions.\n\n"
        "Try:\n"
        "• Show subscriptions\n"
        "• How much am I spending?\n"
        "• Status\n"
        "• Monthly summary\n"
        "• Suggest savings"
    )

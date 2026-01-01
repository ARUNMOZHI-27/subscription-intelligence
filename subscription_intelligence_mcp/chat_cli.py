from rich.console import Console
from rich.table import Table

from conversation_memory import ConversationMemory
from subscription_mcp import (
    list_subscriptions,
    analyze_spend,
    recommend_savings,
    get_monthly_summary,
    export_calendar_file,
    status
)
from llm_chat import chat_explain

console = Console()
memory = ConversationMemory()


def show_subscriptions():
    subs = list_subscriptions()
    if not subs:
        console.print("[yellow]No subscriptions found.[/yellow]")
        return

    table = Table(title="📦 Your Subscriptions")
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


def route_user_message(message: str):
    msg = message.lower().strip()

    # ---------------- STATUS ----------------
    if "status" in msg:
        st = status()
        reply = (
            f"🟢 Agent running: {'Yes' if st['running'] else 'No'}\n"
            f"🕒 Last check: {st['last_check']}\n"
            f"⏭ Next check: {st['next_check']}\n"
            f"⚠ Upcoming alerts: {st['upcoming_alerts']}"
        )
        return reply

    # ---------------- SHOW SUBSCRIPTIONS ----------------
    if any(x in msg for x in ["show", "list", "subscriptions"]):
        show_subscriptions()
        return "👆 These are your current subscriptions."

    # ---------------- SPENDING ----------------
    if any(x in msg for x in ["spend", "cost", "money", "expense"]):
        data = analyze_spend()
        reply = chat_explain(
            f"User monthly spend is ₹{data['total_monthly_spend']}.\n"
            f"Category breakdown: {data['category_breakdown']}"
        )
        return f"💰 Monthly spend: ₹{data['total_monthly_spend']}\n\n{reply}"

    # ---------------- SAVINGS ----------------
    if any(x in msg for x in ["save", "reduce", "cancel"]):
        facts = recommend_savings()
        reply = chat_explain(
            f"User wants to save money.\nFacts:\n{facts}"
        )
        return reply

    # ---------------- MONTHLY SUMMARY ----------------
    if "summary" in msg:
        return get_monthly_summary()

    # ---------------- CALENDAR ----------------
    if "calendar" in msg:
        path = export_calendar_file()
        return f"📅 Calendar file created:\n{path}\nImport it into Google Calendar."

    # ---------------- FALLBACK ----------------
    return (
        "I can help you manage subscriptions.\n\n"
        "Try asking:\n"
        "• Show subscriptions\n"
        "• How much am I spending?\n"
        "• Suggest savings\n"
        "• Monthly summary\n"
        "• Status\n"
        "• Export calendar"
    )


# ---------------- CLI LOOP ----------------

console.print("\n💬 [bold cyan]Subscription Intelligence Chat[/bold cyan]")
console.print("Type [bold]exit[/bold] to quit\n")

while True:
    user = input("You: ").strip()
    if user.lower() in ("exit", "quit"):
        console.print("👋 Bye!")
        break

    response = route_user_message(user)
    console.print("\n[bold green]Assistant:[/bold green]")
    console.print(response)
    print()

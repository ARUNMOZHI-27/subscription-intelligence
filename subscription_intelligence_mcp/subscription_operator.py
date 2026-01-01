import threading
import time
from datetime import datetime, timedelta
import sys
from dotenv import load_dotenv
load_dotenv()
from storage import load_subscriptions, save_subscriptions
from intelligence import analyze_subscription, analyze_duplicates, generate_monthly_summary
from notifier import send_notification, send_monthly_summary
from llm_explainer import explain_alert
from config import CHECK_INTERVAL_HOURS, MONTHLY_SUBSCRIPTION_BUDGET
from agent_state import update_state, get_state

VERBOSE = True


def run_agent_once():
    now = datetime.now()
    subs = load_subscriptions()
    alerts_sent = 0

    if VERBOSE:
        print("\n🤖 Agent running |", now)

    # ---------------- PER SUBSCRIPTION ----------------
    for sub in subs:
        alerts = analyze_subscription(sub)

        for tag, severity, message in alerts:
            if tag not in sub.get("notified", []):
                explanation = explain_alert(sub, message)
                send_notification(sub["name"], severity, message, explanation)
                sub.setdefault("notified", []).append(tag)
                alerts_sent += 1

                if VERBOSE:
                    print(f"📧 Alert → {sub['name']} ({tag})")

    # ---------------- DUPLICATES (ONCE) ----------------
    dup_alerts = analyze_duplicates(subs)
    for tag, severity, message in dup_alerts:
        if tag not in get_state().get("last_duplicates", []):
            explanation = explain_alert(
                {"name": "Subscription Intelligence"}, message
            )
            send_notification("Subscription Intelligence", severity, message, explanation)
            alerts_sent += 1

    # ---------------- BUDGET ----------------
    total = sum(s.get("monthly_cost", 0) for s in subs)
    if total > MONTHLY_SUBSCRIPTION_BUDGET:
        if "budget_alert" not in get_state().get("budget_sent", []):
            msg = f"Monthly budget exceeded: ₹{total} / ₹{MONTHLY_SUBSCRIPTION_BUDGET}"
            explanation = explain_alert({"name": "Budget"}, msg)
            send_notification("Budget Alert", "critical", msg, explanation)
            alerts_sent += 1

    # ---------------- SUMMARY ----------------
    send_monthly_summary(generate_monthly_summary(subs))

    save_subscriptions(subs)

    update_state(
        running=True,
        last_check=now.isoformat(),
        next_check=(now + timedelta(hours=CHECK_INTERVAL_HOURS)).isoformat(),
        upcoming_alerts=alerts_sent
    )

    if VERBOSE:
        print("✅ Agent cycle complete")


def agent_loop():
    while True:
        run_agent_once()
        time.sleep(CHECK_INTERVAL_HOURS * 3600)

if __name__ == "__main__":
    print("🚀 Subscription Intelligence Agent started")

    # Status command still works
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        s = get_state()
        print("\n📡 Status")
        print(f"Running: {'✅' if s['running'] else '❌'}")
        print(f"Last check: {s['last_check']}")
        print(f"Next check: {s['next_check']}")
        print(f"Upcoming alerts: {s['upcoming_alerts']}")
        sys.exit(0)

    # 🔥 Docker-safe foreground loop
    while True:
        run_agent_once()
        time.sleep(CHECK_INTERVAL_HOURS * 3600)

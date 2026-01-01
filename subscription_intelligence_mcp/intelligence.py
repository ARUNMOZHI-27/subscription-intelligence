from datetime import datetime, date
from collections import defaultdict
from typing import List, Tuple, Dict
from dateutil.relativedelta import relativedelta

# -----------------------
# DATE PARSER
# -----------------------

def parse_date(d):
    if not d:
        return None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(d, fmt).date()
        except:
            pass
    return None


# -----------------------
# ALERT ENGINE (PHASE 1)
# -----------------------

def analyze_subscription(sub) -> List[Tuple[str, str, str]]:
    alerts = []
    today = date.today()

    trial = parse_date(sub.get("trial_end_date"))
    billing = parse_date(sub.get("billing_start_date"))
    renewal = parse_date(sub.get("renewal_date"))

    cost = sub.get("monthly_cost", 0)
    notified = set(sub.get("notified", []))

    # 🔔 Trial ending
    if trial:
        days = (trial - today).days
        if days in (7, 3, 1) and f"trial_{days}" not in notified:
            alerts.append((
                f"trial_{days}",
                "warning",
                f"Free trial ends in {days} day(s) on {trial}"
            ))

    # 💳 Billing started
    if billing and billing <= today and "billing_started" not in notified:
        alerts.append((
            "billing_started",
            "critical",
            f"Billing started – ₹{cost}/month"
        ))

    # 🔁 Renewal (EXPLICIT OR INFERRED)
    effective_renewal = None

    if renewal:
        effective_renewal = renewal
    elif billing:
        months = (today.year - billing.year) * 12 + (today.month - billing.month)
        effective_renewal = billing + relativedelta(months=months + 1)

    if effective_renewal:
        days = (effective_renewal - today).days
        if days in (7, 3, 1) and f"renew_{days}" not in notified:
            alerts.append((
                f"renew_{days}",
                "warning",
                f"Subscription renews in {days} day(s) on {effective_renewal}"
            ))

    return alerts


# -----------------------
# DUPLICATE / OVERLAP
# -----------------------

def analyze_duplicates(subs: list) -> List[Tuple[str, str, str]]:
    alerts = []
    cat = defaultdict(list)

    for s in subs:
        category = s.get("category")
        name = s.get("name", "Unknown")
        if not category:
            continue
        cat[category].append(name)

    for category, names in cat.items():
        if len(names) > 1:
            alerts.append((
                f"duplicate_{category}",
                "info",
                f"Overlapping subscriptions in '{category}': {', '.join(names)}"
            ))

    return alerts


# -----------------------
# CATEGORY SPEND
# -----------------------

def analyze_category_spend(subs) -> Dict[str, int]:
    spend = defaultdict(int)
    for s in subs:
        spend[s.get("category", "Other")] += s.get("monthly_cost", 0)
    return dict(spend)


# -----------------------
# SAVINGS INTELLIGENCE (PHASE 2)
# -----------------------

def detect_savings(subs) -> List[Dict]:
    overlaps = []
    cat = defaultdict(list)

    for s in subs:
        cat[s.get("category", "Other")].append(s)

    for category, items in cat.items():
        if len(items) > 1:
            monthly = sum(i.get("monthly_cost", 0) for i in items)
            overlaps.append({
                "category": category,
                "services": [i.get("name") for i in items],
                "monthly": monthly,
                "yearly": monthly * 12
            })

    return overlaps


def calculate_annual_savings(monthly_cost: int) -> int:
    return monthly_cost * 12


# -----------------------
# SUMMARY
# -----------------------

def generate_monthly_summary(subs):
    total = sum(s.get("monthly_cost", 0) for s in subs)
    lines = ["📊 Monthly Subscription Summary\n"]

    for s in subs:
        lines.append(f"- {s.get('name')}: ₹{s.get('monthly_cost', 0)}/month")

    lines.append(f"\n💰 Total: ₹{total}")
    return "\n".join(lines)
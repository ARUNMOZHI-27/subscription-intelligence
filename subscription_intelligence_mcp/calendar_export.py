from ics import Calendar, Event
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from intelligence import parse_date


def export_calendar(subs, output_file="subscriptions.ics"):
    cal = Calendar()
    today = date.today()

    for sub in subs:
        name = sub.get("name", "Subscription")
        cost = sub.get("monthly_cost", 0)

        trial = parse_date(sub.get("trial_end_date"))
        billing = parse_date(sub.get("billing_start_date"))
        renewal = parse_date(sub.get("renewal_date"))

        # 🔔 Trial end event
        if trial and trial >= today:
            e = Event()
            e.name = f"Trial ends: {name}"
            e.begin = datetime.combine(trial, datetime.min.time())
            e.description = f"Free trial ends for {name}. Cost: ₹{cost}/month"
            cal.events.add(e)

        # 🔁 Renewal event (explicit OR inferred)
        effective_renewal = None

        if renewal:
            effective_renewal = renewal
        elif billing:
            months = (today.year - billing.year) * 12 + (today.month - billing.month)
            effective_renewal = billing + relativedelta(months=months + 1)

        if effective_renewal and effective_renewal >= today:
            e = Event()
            e.name = f"Subscription renews: {name}"
            e.begin = datetime.combine(effective_renewal, datetime.min.time())
            e.description = f"{name} renews. Monthly cost: ₹{cost}"
            cal.events.add(e)

    with open(output_file, "w",encoding="utf-8") as f:
        f.writelines(cal)

    return output_file

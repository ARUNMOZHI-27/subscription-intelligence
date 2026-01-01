import streamlit as st
import pandas as pd
from datetime import datetime, date

from storage import load_subscriptions
from intelligence import analyze_category_spend

# -----------------------
# CONFIG
# -----------------------

st.set_page_config(
    page_title="Subscription Intelligence",
    layout="wide",
)

st.title("📊 Subscription Intelligence Dashboard")

subs = load_subscriptions()

if not subs:
    st.warning("No subscriptions found.")
    st.stop()


# -----------------------
# DATAFRAME
# -----------------------

df = pd.DataFrame(subs)

df["monthly_cost"] = df["monthly_cost"].fillna(0)

# Normalize date columns
for col in ["trial_end_date", "renewal_date", "billing_start_date"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")


# -----------------------
# METRICS
# -----------------------

total_monthly = df["monthly_cost"].sum()
annual_projection = total_monthly * 12

col1, col2, col3 = st.columns(3)

col1.metric("💸 Monthly Spend", f"₹{total_monthly}")
col2.metric("📅 Annual Projection", f"₹{annual_projection}")
col3.metric("📦 Subscriptions", len(df))


# -----------------------
# TABLE
# -----------------------

st.subheader("📦 Active Subscriptions")

display_df = df[[
    "name",
    "monthly_cost",
    "category",
    "trial_end_date",
    "renewal_date",
]]

st.dataframe(display_df, width="stretch")


# -----------------------
# CATEGORY SPEND
# -----------------------

st.subheader("📂 Spend by Category")

category_spend = analyze_category_spend(subs)

cat_df = pd.DataFrame(
    category_spend.items(),
    columns=["Category", "Monthly Spend"]
)

st.pyplot(
    cat_df.set_index("Category").plot.pie(
        y="Monthly Spend",
        figsize=(5, 5),
        autopct="%1.0f%%",
        legend=False
    ).figure
)


# -----------------------
# UPCOMING EVENTS
# -----------------------

st.subheader("⏰ Upcoming Trials & Renewals")

today = date.today()

events = []

for s in subs:
    trial = s.get("trial_end_date")
    renew = s.get("renewal_date")

    if trial:
        t = pd.to_datetime(trial).date()
        if t >= today:
            events.append(("Trial End", s["name"], t))

    if renew:
        r = pd.to_datetime(renew).date()
        if r >= today:
            events.append(("Renewal", s["name"], r))

events_df = pd.DataFrame(events, columns=["Type", "Service", "Date"])

if not events_df.empty:
    st.dataframe(events_df.sort_values("Date"), use_container_width=True)
else:
    st.info("No upcoming events.")


# -----------------------
# FOOTER
# -----------------------

st.caption("Subscription Intelligence • Local • Private • Autonomous")

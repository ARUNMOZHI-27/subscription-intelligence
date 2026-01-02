

---

# 🧠 Subscription Intelligence MCP

An autonomous subscription monitoring system built using **MCP (Model Context Protocol)**.  
It tracks subscriptions, detects billing risks, finds duplicates, monitors budgets, and explains everything using LLMs — **without letting the LLM control logic**.

> **Core philosophy:** Rules decide. LLM explains.

---

## ✨ Features

- 🔔 Trial expiry alerts (7 / 3 / 1 day)
- 🔁 Renewal reminders
- 💸 Billing start notifications  
- 🔍 Duplicate subscription detection
- 📊 Monthly spending analysis
- 🎯 Budget limit alerts
- 🤖 LLM-powered human explanations
- 📧 Email notifications
- 📲 Push notifications via **ntfy.sh**
- 💬 Interactive Chat CLI
- 📅 Calendar export (`.ics`)
- 📊 Streamlit dashboard
- 🐳 Docker & Docker Compose support

---

## 🧩 High-Level Architecture

subscriptions.json ↓ storage.py ↓ intelligence.py        ← Rules decide ↓ llm_explainer.py       ← LLM explains ↓ notifier.py            ← Email / Push ↓ subscription_operator.py (Agent) ↓ MCP tools / CLI / Dashboard

**LLM NEVER triggers actions.  
It only explains facts produced by rules.**

---

## 🚀 Quick Start (Docker – Recommended)

```bash
docker compose up -d

Check logs:

docker logs -f subintel

Stop:

docker compose down


---

## 🧪 Run Locally (Without Docker)

pip install -r subscription_intelligence_mcp/requirements.txt
python subscription_operator.py


---

## ⚙️ Configuration

Create a .env file in the project root.

.env Example

# =====================
# Email Notifications
# =====================
EMAIL_ENABLED=true
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_gmail_app_password
EMAIL_TO=your_email@gmail.com

# =====================
# Push Notifications (ntfy)
# =====================
NTFY_ENABLED=true
NTFY_TOPIC=subintel-demo

# =====================
# Agent Settings
# =====================
CHECK_INTERVAL_HOURS=6
MONTHLY_SUBSCRIPTION_BUDGET=2500

# =====================
# LLM Settings
# =====================

OLLAMA_MODEL=llama3.2
OLLAMA_TIMEOUT=120


# =====================
# Storage & Logs
# =====================
DATA_DIR=/data
LOG_DIR=/data/logs
LOG_LEVEL=INFO

## ⚠️ Important Notes

Gmail requires App Password, not your real password

ntfy.sh topics are public → choose a unique topic

Docker users must mount /data as a volume



---

## 🧰 MCP Tools Available

Tool	Description

list_subscriptions()	List all subscriptions
add_subscription()	Add a new subscription
analyze_spend()	Monthly + category spending
recommend_savings()	Detect duplicates & savings
get_monthly_summary()	Monthly overview
status()	Agent runtime status
export_calendar_file()	Generate .ics calendar



---

## 📖 Usage Examples

🐍 Python (MCP Client)

from subscription_mcp import mcp

# Add a subscription
mcp.call_tool("add_subscription", {
    "name": "Netflix",
    "monthly_cost": 499,
    "category": "Streaming",
    "billing_start_date": "2025-01-01",
    "auto_pay": True
})

# List subscriptions
subs = mcp.call_tool("list_subscriptions")
print(subs)

# Spending analysis
spend = mcp.call_tool("analyze_spend")
print(spend)

# Savings advice
print(mcp.call_tool("recommend_savings"))


---

## 💬 Chat CLI

python chat_cli.py

Example commands:

show subscriptions
how much am i spending
suggest savings
export calendar
status


---

## 📊 Dashboard (Streamlit)

streamlit run dashboard.py

Dashboard includes:

Subscription table

Category pie chart

Renewal timeline

Annual cost projection



---

## 📁 Project Structure

subscription-intelligence/
├── subscription_intelligence_mcp/
│   ├── __init__.py
│   ├── subscription_mcp.py
│   ├── subscription_operator.py
│   ├── intelligence.py
│   ├── llm_explainer.py
│   ├── notifier.py
│   ├── storage.py
│   ├── agent_state.py
│   ├── chat_cli.py
│   ├── dashboard.py
│   ├── calendar_export.py
│   ├── validators.py
│   ├── config.py
│   └── requirements.txt
├── data/
│   └── subscriptions.json
├── tests/
├── docs/
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── LICENSE
└── README.md


---

## 🧠 How the Intelligence Works

1️⃣ Rules-Based Alerts

Parses billing, trial, and renewal dates

Triggers alerts at 7 / 3 / 1 day

Detects duplicate categories

Enforces budget limits


2️⃣ Spending Analysis

Aggregates monthly spend

Groups by category

Calculates annual savings


3️⃣ LLM Explanation Layer

Input: factual alert data

Output: calm, human explanation

No decision-making power


4️⃣ Notifications

📧 Email (SMTP)

📲 ntfy.sh push notifications

Smart deduplication prevents spam



---

## 🐳 Docker Details

Build Image

docker build -t subintel .

Run Container

docker run -d \
  --name subintel \
  --env-file .env \
  -v $(pwd)/data:/data \
  subintel


---

## 🧪 Testing

pytest tests/ -v
pytest --cov=subscription_intelligence_mcp


---

## 🐛 Troubleshooting

Subscriptions not saving

Ensure /data/subscriptions.json exists

Check volume mount

Verify write permissions


Emails not sending

Use Gmail App Password

Confirm EMAIL_ENABLED=true

Check logs: docker logs -f subintel


Docker exits immediately

Missing dependency → rebuild with --no-cache

Check logs for Python errors



---

## 📜 License

MIT License © 2026 Arunmozhi (ARUNMOZHI-27)

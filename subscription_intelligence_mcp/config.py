import os
from dotenv import load_dotenv

load_dotenv()

# Agent
CHECK_INTERVAL_HOURS = 24


MONTHLY_SUBSCRIPTION_BUDGET = 4000

# Push notifications
NTFY_ENABLED = True
NTFY_TOPIC = "subscription-intelligence"

# Alerts
TRIAL_ALERT_DAYS = [7, 3, 1]
RENEWAL_ALERT_DAYS = [7, 3, 1]

SHOW_DETAILS_IN_TERMINAL=True


EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

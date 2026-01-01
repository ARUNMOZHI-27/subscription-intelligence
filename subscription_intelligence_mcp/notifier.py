import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "true").lower() == "true"
NTFY_ENABLED = os.getenv("NTFY_ENABLED", "false").lower() == "true"

SMTP_SERVER = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_FROM = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO", EMAIL_FROM)

NTFY_TOPIC = os.getenv("NTFY_TOPIC")  # ex: subintel-mozhi


def _email_config_valid():
    return all([SMTP_SERVER, SMTP_PORT, EMAIL_FROM, EMAIL_PASSWORD])


# ---------------- PUSH ----------------

def send_push_notification(title: str, message: str):
    if not (NTFY_ENABLED and NTFY_TOPIC):
        return

    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode("utf-8"),
            headers={"Title": title},
            timeout=5
        )
        print("📲 Push sent")
    except Exception as e:
        print("⚠️ Push failed:", e)


# ---------------- MAIN ----------------

def send_notification(service, severity, message, explanation=""):
    subject = f"[{severity.upper()}] Subscription Alert – {service}"

    body = f"""Service: {service}
Severity: {severity}

{message}

Why this matters:
{explanation}
"""

    # 📧 EMAIL
    if EMAIL_ENABLED and _email_config_valid():
        try:
            msg = MIMEMultipart()
            msg["From"] = EMAIL_FROM
            msg["To"] = EMAIL_TO
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain", "utf-8"))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_FROM, EMAIL_PASSWORD)
                server.send_message(msg)

            print("📧 Email sent")

        except Exception as e:
            print("⚠️ Email failed:", e)

    # 📲 PUSH (independent of email)
    send_push_notification(
        title=f"{severity.upper()} – {service}",
        message=f"{message}\n\n{explanation}"
    )


def send_monthly_summary(summary_text: str):
    if not (EMAIL_ENABLED and _email_config_valid()):
        return

    try:
        msg = MIMEText(summary_text, "plain", "utf-8")
        msg["From"] = EMAIL_FROM
        msg["To"] = EMAIL_TO
        msg["Subject"] = "📊 Monthly Subscription Summary"

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)

        print("📊 Monthly summary sent")

    except Exception as e:
        print("⚠️ Monthly summary failed:", e)

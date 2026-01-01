import json
import os
from pathlib import Path

# -----------------------
# DATA DIRECTORY RESOLUTION
# -----------------------

DEFAULT_DATA_DIR = "data"

DATA_DIR = os.getenv("DATA_DIR", DEFAULT_DATA_DIR)

DATA_DIR = Path(DATA_DIR)
FILE = DATA_DIR / "subscriptions.json"


def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------
# LOAD
# -----------------------

def load_subscriptions():
    ensure_data_dir()

    if not FILE.exists():
        return []

    with FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------
# SAVE
# -----------------------

def save_subscriptions(subs):
    ensure_data_dir()

    with FILE.open("w", encoding="utf-8") as f:
        json.dump(subs, f, indent=2, ensure_ascii=False)


# -----------------------
# MARK NOTIFIED
# -----------------------

def mark_notified(name: str, tag: str):
    subs = load_subscriptions()

    for s in subs:
        if s.get("name", "").lower() == name.lower():
            s.setdefault("notified", [])
            if tag not in s["notified"]:
                s["notified"].append(tag)

    save_subscriptions(subs)
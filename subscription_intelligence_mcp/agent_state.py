from typing import Dict
from threading import Lock

_STATE = {
    "running": False,
    "last_check": None,
    "next_check": None,
    "upcoming_alerts": 0
}

_LOCK = Lock()


def update_state(**kwargs):
    with _LOCK:
        for k, v in kwargs.items():
            _STATE[k] = v


def get_state() -> Dict:
    with _LOCK:
        return dict(_STATE)

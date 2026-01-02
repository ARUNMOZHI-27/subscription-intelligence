from datetime import datetime
from typing import Optional


class ValidationError(Exception):
    """Raised when validation fails"""
    pass


def validate_name(name: str) -> str:
    if not isinstance(name, str):
        raise ValidationError("Subscription name must be a string")

    name = name.strip()
    if not name:
        raise ValidationError("Subscription name cannot be empty")

    if len(name) > 100:
        raise ValidationError("Subscription name is too long")

    return name


def validate_monthly_cost(cost) -> int:
    if not isinstance(cost, (int, float)):
        raise ValidationError("Monthly cost must be a number")

    cost = int(cost)
    if cost < 0:
        raise ValidationError("Monthly cost cannot be negative")

    return cost


def validate_category(category: str) -> str:
    if not isinstance(category, str):
        raise ValidationError("Category must be a string")

    category = category.strip()
    if not category:
        raise ValidationError("Category cannot be empty")

    return category


def validate_date(date_str: Optional[str]) -> Optional[str]:
    if date_str is None:
        return None

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValidationError("Date must be in YYYY-MM-DD format")

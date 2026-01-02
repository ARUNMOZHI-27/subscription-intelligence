import pytest
from subscription_intelligence_mcp.validators import (
    validate_name,
    validate_monthly_cost,
    validate_category,
    validate_date,
    ValidationError
)


def test_name_ok():
    assert validate_name("Netflix") == "Netflix"


def test_name_fail():
    with pytest.raises(ValidationError):
        validate_name("")


def test_cost_ok():
    assert validate_monthly_cost(299) == 299


def test_cost_fail():
    with pytest.raises(ValidationError):
        validate_monthly_cost(-10)


def test_category_ok():
    assert validate_category("Streaming") == "Streaming"


def test_date_ok():
    assert validate_date("2026-01-01") == "2026-01-01"


def test_date_fail():
    with pytest.raises(ValidationError):
        validate_date("01-01-2026")

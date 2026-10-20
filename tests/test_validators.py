"""Tests for the input validators."""

import pytest

from taskflow.validators import validate_due_date, validate_priority, validate_title


def test_title_is_stripped():
    assert validate_title("  Buy milk  ") == "Buy milk"


def test_empty_title_is_rejected():
    with pytest.raises(ValueError):
        validate_title("   ")


def test_too_long_title_is_rejected():
    with pytest.raises(ValueError):
        validate_title("a" * 101)


def test_priority_is_normalised():
    assert validate_priority(" HIGH ") == "high"


def test_invalid_priority_is_rejected():
    with pytest.raises(ValueError):
        validate_priority("urgent")


def test_valid_due_date_is_accepted():
    assert validate_due_date("2026-11-15") == "2026-11-15"


def test_missing_due_date_is_allowed():
    assert validate_due_date(None) is None


def test_wrong_format_due_date_is_rejected():
    with pytest.raises(ValueError):
        validate_due_date("15-11-2026")


def test_impossible_due_date_is_rejected():
    with pytest.raises(ValueError):
        validate_due_date("2026-02-30")
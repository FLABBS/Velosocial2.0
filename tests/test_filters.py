import pytest
from bot.utils.filters import build_user_filters, validate_filter_params


def test_build_user_filters_none():
    cond, params = build_user_filters()
    assert cond == "1=1"
    assert params == []


def test_build_user_filters_values():
    cond, params = build_user_filters(bike_type="road", skill_level="beginner")
    assert cond == "bike_type = ? AND skill_level = ?"
    assert params == ["road", "beginner"]


def test_validate_filter_params():
    assert validate_filter_params("road", "pro") is True
    assert validate_filter_params(None, None) is True
    assert not validate_filter_params("plane", "pro")
    assert not validate_filter_params("road", "expert")

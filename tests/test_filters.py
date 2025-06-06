import pytest
from bot.utils.filters import build_user_filters, validate_filter_params


def test_build_user_filters_empty():
    condition, params = build_user_filters()
    assert condition == "1=1"
    assert params == []


def test_build_user_filters_full():
    condition, params = build_user_filters('road', 'beginner')
    assert condition == "bike_type = ? AND skill_level = ?"
    assert params == ['road', 'beginner']


def test_validate_filter_params():
    assert validate_filter_params('road', 'beginner') is True
    assert validate_filter_params('plane', 'beginner') is False

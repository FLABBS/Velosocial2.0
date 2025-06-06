import pytest
from bot.models import User


def test_user_validate_ok():
    user = User(telegram_id=1, bike_type='road', skill_level='beginner')
    user.validate()


def test_user_validate_invalid():
    user = User(telegram_id=1, bike_type='invalid', skill_level='beginner')
    with pytest.raises(ValueError):
        user.validate()

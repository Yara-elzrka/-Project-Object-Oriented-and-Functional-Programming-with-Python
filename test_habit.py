import pytest
from datetime import datetime, timedelta
from habit.habit import Habit


def test_create_habit_valid():
    habit = Habit("Exercise", "daily")
    assert habit.name == "Exercise"
    assert habit.periodicity == "daily"
    assert isinstance(habit.created_at, datetime)
    assert habit.events == []


def test_create_habit_invalid_periodicity():
    with pytest.raises(ValueError):
        Habit("Meditate", "monthly")  # invalid periodicity


def test_check_off_event_added():
    habit = Habit("Read", "daily")
    assert len(habit.events) == 0
    habit.check_off()
    assert len(habit.events) == 1
    assert isinstance(habit.events[0], datetime)


def test_check_off_with_custom_timestamp():
    habit = Habit("Journal", "daily")
    custom_time = datetime(2023, 1, 1, 10, 0)
    habit.check_off(custom_time)
    assert habit.events[0] == custom_time

from datetime import datetime, timedelta
from habit.habit import Habit
from habit.manager import HabitManager
from habit.analytics import (
    get_all_habits,
    get_habits_by_periodicity,
    get_longest_streak,
    get_longest_streak_all
)


def test_get_all_habits():
    manager = HabitManager()
    manager.create_habit("Meditate", "daily")
    manager.create_habit("Walk", "weekly")
    result = get_all_habits(manager)
    assert "Meditate" in result
    assert "Walk" in result


def test_get_habits_by_periodicity():
    manager = HabitManager()
    manager.create_habit("Yoga", "daily")
    manager.create_habit("Cleaning", "weekly")
    daily_habits = get_habits_by_periodicity(manager, "daily")
    assert "Yoga" in daily_habits
    assert "Cleaning" not in daily_habits


def test_get_longest_streak_daily():
    habit = Habit("Stretch", "daily")
    base = datetime(2023, 1, 1)
    for i in range(5):
        habit.check_off(base + timedelta(days=i))
    assert get_longest_streak(habit) == 5


def test_get_longest_streak_with_gap():
    habit = Habit("Workout", "daily")
    base = datetime(2023, 1, 1)
    habit.check_off(base)
    habit.check_off(base + timedelta(days=1))
    habit.check_off(base + timedelta(days=3))  # gap breaks streak
    habit.check_off(base + timedelta(days=4))
    assert get_longest_streak(habit) == 2


def test_get_longest_streak_all():
    manager = HabitManager()
    h1 = manager.create_habit("Read", "daily")
    h2 = manager.create_habit("Run", "weekly")

    base = datetime(2023, 1, 1)
    for i in range(3):
        h1.check_off(base + timedelta(days=i))
    for i in range(2):
        h2.check_off(base + timedelta(weeks=i))

    assert get_longest_streak_all(manager) == 3

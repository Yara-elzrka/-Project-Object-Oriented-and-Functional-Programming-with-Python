from datetime import timedelta


def get_all_habits(manager):
    return [habit.name for habit in manager.habits]

def get_habits_by_periodicity(manager, periodicity):
    return [habit.name for habit in manager.habits if habit.periodicity == periodicity]

def get_longest_streak_all(manager):
    return max(get_longest_streak(habit) for habit in manager.habits)

def get_longest_streak(habit):
    if not habit.events:
        return 0

    sorted_events = sorted(habit.events)
    streak = 1
    max_streak = 1

    delta = timedelta(days=1) if habit.periodicity == "daily" else timedelta(weeks=1)

    for i in range(1, len(sorted_events)):
        if sorted_events[i] - sorted_events[i - 1] <= delta:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 1

    return max_streak

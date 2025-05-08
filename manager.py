from .habit import Habit
from typing import List, Optional


class HabitManager:
    def __init__(self) -> None:
        self.habits: List[Habit] = []

    def create_habit(self, name: str, periodicity: str) -> Habit:
        habit = Habit(name, periodicity)
        self.habits.append(habit)
        return habit

    def get_habit_by_name(self, name: str) -> Optional[Habit]:
        return next((habit for habit in self.habits if habit.name == name), None)

    def delete_habit(self, name: str) -> bool:
        habit = self.get_habit_by_name(name)
        if habit:
            self.habits.remove(habit)
            return True
        return False

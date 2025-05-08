from datetime import datetime

class Habit:
    def __init__(self, name, periodicity, created_at=None):
        if periodicity not in ("daily", "weekly"):
            raise ValueError("Periodicity must be either 'daily' or 'weekly'")
        self.name = name
        self.periodicity = periodicity
        self.created_at = created_at or datetime.now()
        self.events = []

    def check_off(self, timestamp=None):
        time = timestamp or datetime.now()
        self.events.append(time)
        return time

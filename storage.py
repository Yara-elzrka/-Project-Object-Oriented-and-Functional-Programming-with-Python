import sqlite3
from datetime import datetime
from .habit import Habit

DB_PATH = "data/habits.db"


# Initialize the database
def init_db():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    periodicity TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS habit_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_name TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (habit_name) REFERENCES habits(name)
                );
            """)
            conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")


# Save a habit to the database
def save_habit(habit: Habit):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO habits (name, periodicity, created_at)
                VALUES (?, ?, ?)
            """, (habit.name, habit.periodicity, habit.created_at.isoformat()))
            conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while saving the habit: {e}")


# Load all habits from the database
def load_all_habits():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT name, periodicity, created_at FROM habits")
            rows = cur.fetchall()

        habits = [
            Habit(name, periodicity, datetime.fromisoformat(created_at))
            for name, periodicity, created_at in rows
        ]
        for habit in habits:
            load_checkoffs_for(habit)
        return habits
    except sqlite3.Error as e:
        print(f"An error occurred while loading habits: {e}")
        return []  # Return an empty list in case of error


# Save a habit's check-in event to the database
def save_checkoff(habit_name, timestamp):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO habit_events (habit_name, timestamp)
                VALUES (?, ?)
            """, (habit_name, timestamp.isoformat()))
            conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while saving the check-off: {e}")


# Load all check-in events for a specific habit
def load_checkoffs_for(habit):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT timestamp FROM habit_events
                WHERE habit_name = ?
            """, (habit.name,))
            rows = cur.fetchall()

        habit.events = [datetime.fromisoformat(row[0]) for row in rows]
    except sqlite3.Error as e:
        print(f"An error occurred while loading check-offs for habit '{habit.name}': {e}")

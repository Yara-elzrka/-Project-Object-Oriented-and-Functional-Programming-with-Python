from habit.manager import HabitManager
from habit.analytics import get_all_habits, get_longest_streak
from habit.storage import init_db, save_habit, save_checkoff, load_all_habits

def main():
    init_db()
    manager = HabitManager()

    # Load existing habits from DB
    stored_habits = load_all_habits()
    for h in stored_habits:
        manager.habits.append(h)

    while True:
        print("\n--- Dream Track Habit Tracker ---")
        print("1. Create habit")
        print("2. List habits")
        print("3. Check-in habit")
        print("4. View streaks")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Habit name: ").strip()
            period = input("Periodicity (daily/weekly): ").strip().lower()
            if period not in ["daily", "weekly"]:
                print("Invalid periodicity. Please enter 'daily' or 'weekly'.")
                continue
            habit = manager.create_habit(name, period)
            save_habit(habit)
            print(f"Habit '{habit.name}' created and saved.")

        elif choice == "2":
            habits = get_all_habits(manager)
            if habits:
                print("Tracked habits:")
                for habit in habits:
                    print(f"- {habit}")
            else:
                print("No habits found.")

        elif choice == "3":
            name = input("Which habit to check-in? ").strip()
            habit = manager.get_habit_by_name(name)
            if habit:
                ts = habit.check_off()
                save_checkoff(habit.name, ts)
                print(f"Habit '{habit.name}' checked in at {ts}")
            else:
                print("Habit not found.")

        elif choice == "4":
            name = input("Enter habit name to view streak: ").strip()
            habit = manager.get_habit_by_name(name)
            if habit:
                streak = get_longest_streak(habit)
                print(f"Longest streak for '{habit.name}': {streak} check-ins")
            else:
                print("Habit not found.")

        elif choice == "5":
            print("Exiting. Stay consistent!")
            break

        else:
            print("Invalid option. Please choose a number from 1 to 5.")

if __name__ == "__main__":
    main()

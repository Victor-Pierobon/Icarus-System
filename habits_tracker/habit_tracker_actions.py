import datetime
import sqlite3
import flet as ft

# Connect to SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect('habits.db')
cursor = conn.cursor()


def add_habit(conn, cursor, habit):
    """Adds a new habit to the tracker."""
    try:
        cursor.execute("INSERT INTO habits (name) VALUES (?)", (habit,))
        conn.commit()
        print(f"Habit '{habit}' added!")
    except sqlite3.IntegrityError:
        print(f"Habit '{habit}' already exists.")

def mark_habit_done(conn, cursor, habit):
    """Records that a habit was completed today."""
    today = datetime.date.today()
    try:
        cursor.execute("SELECT id FROM habits WHERE name = ?", (habit,))
        habit_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO completions (habit_id, date) VALUES (?, ?)", (habit_id, today))
        conn.commit()
        print(f"Congratulations!\nHabit '{habit}' was completed today.")
    except TypeError:
        print(f"Habit '{habit}' not found.")

def view_habits():
    """Displays all habits and their completion history."""
    cursor.execute("SELECT h.name, c.date FROM habits h LEFT JOIN completions c ON h.id = c.habit_id")
    habits_data = cursor.fetchall()
    
    if habits_data:
        for habit_name, completion_date in habits_data:
            print(f"Habit: {habit_name}")
            if completion_date:
                print(f"  Completed on: {completion_date}")
    else:
        print("No habits added yet.")

def view_habit_progress(conn, cursor, habit):
    """Shows the progress of a specific habit."""
    cursor.execute(
        "SELECT c.date FROM habits h JOIN completions c ON h.id = c.habit_id WHERE h.name = ?", (habit,)
    )
    dates = [str(row[0]) for row in cursor.fetchall()]
    if dates:
        print(f"Habit: {habit}")
        print(f"  Completed on: {', '.join(dates)}")
    else:
        print(f"Habit '{habit}' not found or has no completion records.")

def delete_habit(conn, cursor, habit):
    """Deletes a habit from the tracker."""
    try:
        cursor.execute("SELECT id FROM habits WHERE name = ?", (habit,))
        habit_id = cursor.fetchone()[0]
        cursor.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
        cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        conn.commit()
        print(f"Habit '{habit}' deleted!")
    except TypeError:
        print(f"Habit '{habit}' not found.")

# No need to call save_habits() anymore, as changes are saved immediately to the database.

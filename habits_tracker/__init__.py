import flet as ft
import habit_tracker_actions as actions
import datetime
import sqlite3

# --- Database Setup ---
def get_db_connection():
    """Returns a new database connection."""
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    return conn, cursor

# Create tables if they don't exist
conn, cursor = get_db_connection()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS completions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        date DATE,
        FOREIGN KEY (habit_id) REFERENCES habits(id)
    )
''')
conn.commit()
conn.close()
# --- End Database Setup ---

def main(page: ft.Page):
    page.title = "Habit Tracker"
    page.padding = ft.padding.all(20)

    habits = []

    def refresh_habits():
        habit_list.controls.clear()
        conn, cursor = get_db_connection()  # Get connection inside the function
        cursor.execute("SELECT name FROM habits")
        for row in cursor.fetchall():
            habits.append(row[0])
        conn.close()  # Close the connection

        for habit in habits:
            habit_list.controls.append(ft.Text(habit))
        page.update()

    def add_habit_button_clicked(e):
        new_habit = habit_input.value
        if new_habit:
            conn, cursor = get_db_connection()
            actions.add_habit(conn, cursor, new_habit)
            conn.close()
            habits.append(new_habit)
            habit_input.value = ""
            refresh_habits()

    def delete_habit_button_clicked(e):
        habit_to_delete = habit_input.value
        if habit_to_delete in habits:
            conn, cursor = get_db_connection()
            actions.delete_habit(conn, cursor, habit_to_delete)
            conn.close()
            habits.remove(habit_to_delete)
            habit_input.value = ""
            refresh_habits()

    habit_input = ft.TextField(label="Habit Name")
    add_habit_button = ft.ElevatedButton(
        text="Add Habit", on_click=add_habit_button_clicked
    )
    delete_habit_button = ft.ElevatedButton(
        text="Delete Habit", on_click=delete_habit_button_clicked
    )
    habit_list = ft.Column(controls=[])

    refresh_habits()

    page.add(
        ft.Column(
            controls=[
                ft.Row(controls=[habit_input, add_habit_button, delete_habit_button]),
                habit_list,
            ]
        )
    )

ft.app(target=main)

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

    habits = {}  # Use a dictionary to store habit names and completion status

    def refresh_habits():
        habits.clear()
        habit_list.controls.clear()
        conn, cursor = get_db_connection()
        cursor.execute("SELECT id, name FROM habits")
        for row in cursor.fetchall():
            habit_id, habit_name = row
            habits[habit_id] = {"name": habit_name, "done": False}
        conn.close()

        # Check if habits are done for today
        today = datetime.date.today()
        conn, cursor = get_db_connection()
        for habit_id in habits:
            cursor.execute(
                "SELECT 1 FROM completions WHERE habit_id = ? AND date = ?",
                (habit_id, today),
            )
            if cursor.fetchone():
                habits[habit_id]["done"] = True
        conn.close()

        # Update the UI
        for habit_id, habit_data in habits.items():
            habit_list.controls.append(
                ft.Row(
                    [
                        ft.Text(habit_data["name"]),
                        ft.Checkbox(
                            value=habit_data["done"],
                            on_change=lambda e, id=habit_id: mark_habit_done(id),
                        ),
                    ]
                )
            )
        page.update()

    def add_habit_button_clicked(e):
        def close_dialog(e):
            dlg.open = False
            page.update()

        def save_habit(e):
            new_habit = new_habit_input.value
            if new_habit:
                conn, cursor = get_db_connection()
                actions.add_habit(conn, cursor, new_habit)
                conn.close()
                dlg.open = False
                refresh_habits()
                page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add Habit"),
            content=ft.Column(
                [
                    ft.TextField(label="Habit Name", id="new_habit_input"),
                    ft.Row(
                        [
                            ft.ElevatedButton(text="Save", on_click=save_habit),
                            ft.OutlinedButton(
                                text="Cancel", on_click=close_dialog
                            ),
                        ]
                    ),
                ]
            ),
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def mark_habit_done(habit_id):
        conn, cursor = get_db_connection()
        habit_name = habits[habit_id]["name"]
        if habits[habit_id]["done"]:
            # If already marked done, unmark it
            cursor.execute(
                "DELETE FROM completions WHERE habit_id = ? AND date = ?",
                (habit_id, datetime.date.today()),
            )
        else:
            actions.mark_habit_done(conn, cursor, habit_name)
        conn.close()
        refresh_habits()

    add_habit_button = ft.FloatingActionButton(
        icon=ft.icons.ADD, on_click=add_habit_button_clicked
    )
    habit_list = ft.Column(controls=[])

    refresh_habits()

    page.add(
        ft.Column(
            controls=[
                habit_list,
                add_habit_button,
            ]
        )
    )

ft.app(target=main)

import flet as ft
import habit_tracker_actions as actions

def main(page: ft.Page):
    page.title = "Habit Tracker"
    page.padding = ft.padding.all(20)  # Add padding to the page

    # Create the ListView outside the main function to keep it in memory
    habits_list = ft.ListView(
        expand=True,
        spacing=10,
        padding=ft.padding.all(10),
        horizontal=True,
            
    )
    

    # Add habit input and button
    habit_input = ft.TextField(
        label="New Habit",
        expand=True,
        border_radius=ft.border_radius.all(5),
        border_color=ft.colors.BLUE_GREY_100,
        border_width=1,
        filled=True,
        fill_color=ft.colors.BLUE_GREY_50,
    )
    

    add_habit_button = ft.ElevatedButton(
        text="Add habit",  # Use 'size' here
        on_click=lambda e: add_habit_and_update_list(habit_input.value, habits_list, page),
        style=ft.ButtonStyle(
            color=ft.colors.BLUE,
            padding=ft.padding.all(15),
        ),
    )

    # Wrap the button in a Container to apply border_radius
    button_container = ft.Container(
        content=add_habit_button,
        border_radius=ft.border_radius.all(5),
    )

    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[habit_input, button_container],  # Use button_container here
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15,
                ),
                ft.Container(height=20),  # Replace SizedBox with Container
                habits_list,
            ]
        ),
    )
    

    # Initial update to display existing habits
    update_habits_list(habits_list, page)

    page.update()

def add_habit_and_update_list(habit, habits_list, page):
    """Adds a habit and updates the ListView."""
    actions.add_habit(habit)
    update_habits_list(habits_list, page)

def update_habits_list(habits_list, page):
    """Updates the ListView with the current habits."""
    habits_list.controls = [
        ft.ListTile(
            title=ft.Text(h, style=ft.TextStyle(size=18)),  # Use 'size' here
            trailing=ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.DONE,
                        on_click=lambda e: mark_habit_done_and_update(h, habits_list, page),
                        icon_color=ft.colors.GREEN,
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e: delete_habit_and_update(h, habits_list, page),
                        icon_color=ft.colors.RED,
                    ),
                ]
            ),
        )
        for h in actions.habits
    ]
    page.update()

def mark_habit_done_and_update(habit, habits_list, page):
    """Marks a habit as done and updates the ListView."""
    actions.mark_habit_done(habit)
    update_habits_list(habits_list, page)

def delete_habit_and_update(habit, habits_list, page):
    """Deletes a habit and updates the ListView."""
    actions.delete_habit(habit)
    update_habits_list(habits_list, page)

ft.app(target=main)

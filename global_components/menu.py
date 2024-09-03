import flet as ft
from flet import UserControl, Text, Icon, Tooltip, ElevatedButton, MainAxisAlignment, PopupMenuItem, Row, Column, alignment


class MyMenu(UserControl):
    def __init__(self, page: ft.Page):  # Removed menu_items parameter
        super().__init__()
        self.page = page
        self.is_menu_open = False
        self.menu_items = [  # Define menu items here
            {"text": "Daily Quest", "route": "/daily_quest"},
            {"text": "Status", "route": "/status"},
            {"text": "Habit Tracker", "route": "/habit_tracker"},
        ]

    def build(self):
        menu_items = []
        for item in self.menu_items:
            menu_items.append(
                PopupMenuItem(text=item['text'], on_click=lambda e: self.page.go(item['route']))
            )

        return Column(
            [
                Row(
                    [
                        ElevatedButton(
                            "Menu",
                            width=100,
                            bgcolor="#4c7df7",
                            color="white",
                            on_click=self.toggle_menu,
                            tooltip=Tooltip(
                                content=ft.Container(
                                    content=ft.Text("Menu"),
                                    padding=10,
                                    border_radius=ft.border_radius.all(5),
                                    bgcolor="#222222",
                                ),
                            ),
                        ),
                    ],
                    alignment=MainAxisAlignment.END,
                ),
                ft.Container(
                    content=ft.Menu(
                        items=menu_items,
                        open=self.is_menu_open,
                        on_close=lambda e: setattr(self, "is_menu_open", False),
                    ),
                    alignment=alignment.top_right,
                ),
            ],
        )

    def toggle_menu(self, e):
        self.is_menu_open = not self.is_menu_open
        self.update()

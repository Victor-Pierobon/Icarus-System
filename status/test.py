import flet as ft
import player

def main(page: ft.Page):
    page.title = "Player Test"
    page.padding = ft.padding.all(20)

    # Input fields
    player_name_input = ft.TextField(label="Player Name")
    experience_input = ft.TextField(label="Experience Gain")
    stat_input = ft.TextField(label="Stat to Allocate")
    points_input = ft.TextField(label="Points to Allocate")

    # Buttons
    create_player_button = ft.ElevatedButton(
        text="Create Player",
        on_click=lambda e: create_player(player_name_input.value, page)
    )
    gain_experience_button = ft.ElevatedButton(
        text="Gain Experience",
        on_click=lambda e: gain_experience(player_name_input.value, experience_input.value, page)
    )
    allocate_points_button = ft.ElevatedButton(
        text="Allocate Points",
        on_click=lambda e: allocate_points(player_name_input.value, stat_input.value, points_input.value, page)
    )

    # Output area
    output_text = ft.Text(value="", size=16)

    # Layout
    page.add(
        ft.Column(
            controls=[
                ft.Row(controls=[player_name_input, create_player_button]),
                ft.Row(controls=[experience_input, gain_experience_button]),
                ft.Row(controls=[stat_input, points_input, allocate_points_button]),
                ft.Container(height=20),
                output_text
            ]
        )
    )

def create_player(name, page):
    player.create_new_player(name)
    page.snack_bar = ft.SnackBar(ft.Text(f"Player '{name}' created!"))
    page.show_snack_bar()

def gain_experience(name, experience, page):
    try:
        experience = int(experience)
        player.gain_experience(name, experience)
        page.snack_bar = ft.SnackBar(ft.Text(f"Experience gained!"))
        page.snack_bar.open = True
        page.update()
    except ValueError:
        page.snack_bar = ft.SnackBar(ft.Text("Invalid experience value."))
        page.snack_bar.open = True
        page.update()

def allocate_points(name, stat, points, page):
    try:
        points = int(points)
        player.allocate_stat_points(name, stat, points)
        page.snack_bar = ft.SnackBar(ft.Text(f"Points allocated!"))
        page.snack_bar.open = True
        page.update()
    except ValueError:
        page.snack_bar = ft.SnackBar(ft.Text("Invalid points value."))
        page.snack_bar.open = True
        page.update()

ft.app(target=main)

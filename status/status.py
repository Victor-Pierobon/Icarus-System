import flet as ft
import player_controls as player
import sys
sys.path.append('../')
#discover how to make this f* shit work
from global_components.menu import MyMenu




def main(page: ft.Page):
    page.title = "Player Status"
    page.padding = ft.padding.all(20)

    player_name = ft.TextField(label="Enter Player Name")

    def display_player_info(e):
        player_name_value = player_name.value
        if player_name_value:
            conn, cursor = player.create_connection()
            player_data = player.get_player_data(conn, cursor, player_name_value)
            conn.close()

            if player_data:
                page.add(
                    ft.Column(
                        [
                            ft.Text(f"Name: {player_data['name']}", size=20),
                            ft.Text(f"Level: {player_data['level']}"),
                            ft.Text(f"HP: {player_data['hp']}"),
                            ft.Text(f"MP: {player_data['mp']}"),
                            ft.Text(f"Job: {player_data['job']}"),
                            ft.Text(f"Experience: {player_data['experience']}"),
                            ft.Text(f"Experience to Next Level: {player_data['experience_to_next_level']}"),
                            ft.Text(f"Strength: {player_data['strenght']}"),
                            ft.Text(f"Vitality: {player_data['vitality']}"),
                            ft.Text(f"Agility: {player_data['agility']}"),
                            ft.Text(f"Intelligence: {player_data['inteligence']}"),
                            ft.Text(f"Status Points: {player_data['status_points']}"),
                        ]
                    )
                )
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Player not found!"))
                page.snack_bar.open = True
                page.update()

    page.add(
        MyMenu(),
        player_name,
        ft.ElevatedButton("Show Player Info", on_click=display_player_info)
    )

ft.app(target=main)

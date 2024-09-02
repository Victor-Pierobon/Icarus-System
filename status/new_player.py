import flet as ft
import player

def main(page: ft.Page):
    page.title = "Create New Player"
    page.padding = ft.padding.all(20)



    player_name_input = ft.TextField(label="Player Name")

    def create_player(e):
        new_player_name = player_name_input.value
        if new_player_name:
            conn, cursor = player.create_connection()
            player.create_new_player(conn, cursor, new_player_name)
            conn.close()
            page.snack_bar = ft.SnackBar(ft.Text(f"Player '{new_player_name}' created!"))
            page.snack_bar.open = True
            page.update()
            # You might want to redirect to the player status page here
            # using page.go(f"/{new_player_name}")

    page.add(
        ft.Column(
            [
                ft.Text(f"Welcome new player! \n Whats your name?", size = 20,color="#4c7df7", ),
                player_name_input,
                ft.ElevatedButton("Create Player", on_click=create_player),
            ]
        )
    )

ft.app(target=main)

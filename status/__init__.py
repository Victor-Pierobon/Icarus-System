import flet as ft
import player
import asyncio

def main(page: ft.Page):
    page.title = "Status"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 50
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    player_name = "Demon King 97"
    player_data = player.player_data.get(player_name, {})

    # Create controls for displaying player data
    name_text = ft.Text(f"NAME: {player_name}", style=ft.TextStyle(weight=ft.FontWeight.BOLD))
    level_text = ft.Text(f"LEVEL: {player_data.get('level', 1)}", style=ft.TextStyle(weight=ft.FontWeight.BOLD), text_align=ft.TextAlign.RIGHT)
    job_text = ft.Text("JOB: NONE", style=ft.TextStyle(weight=ft.FontWeight.BOLD))
    hp_text = ft.Text(f"HP: {player_data.get('hp', 100)}", style=ft.TextStyle(weight=ft.FontWeight.BOLD))
    mp_text = ft.Text(f"MP: {player_data.get('mp', 100)}", style=ft.TextStyle(weight=ft.FontWeight.BOLD))
    strength_text = ft.Text(f"STRENGTH: {player_data.get('strenght', 1)}", style=ft.TextStyle(weight=ft.FontWeight.BOLD))
    vitality_text = ft.Text(f"VITALITY: {player_data.get('vitality', 1)}", style=ft.TextStyle(weight=ft.FontWeight.BOLD), text_align=ft.TextAlign.RIGHT)
    agility_text = ft.Text(f"AGILITY: {player_data.get('agility', 1)}", style=ft.TextStyle(weight=ft.FontWeight.BOLD))
    inteligence_text = ft.Text(f"INTELLIGENCE: {player_data.get('inteligence', 1)}", style=ft.TextStyle(weight=ft.FontWeight.BOLD), text_align=ft.TextAlign.RIGHT)
    remaining_points_text = ft.Text(f"REMAINING POINTS: {player_data.get('remaining_points', 0)}", style=ft.TextStyle(weight=ft.FontWeight.BOLD))

    # Create progress bars
    hp_progress_bar = ft.ProgressBar(value=player_data.get('hp', 100) / 100, color=ft.colors.RED, width=200)
    mp_progress_bar = ft.ProgressBar(value=player_data.get('mp', 100) / 100, color=ft.colors.BLUE, width=200)

    # Create the status card
    status_card = ft.Card(
        content=ft.Column(
            [
                ft.Text("STATUS", style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=24)),
                ft.Divider(),
                ft.Row([name_text, level_text]),
                ft.Row([job_text]),
                ft.Row([hp_text, hp_progress_bar]),
                ft.Row([mp_text, mp_progress_bar]),
                ft.Divider(),
                ft.Row([strength_text, vitality_text]),
                ft.Row([agility_text, inteligence_text]),
                ft.Divider(),
                remaining_points_text,
            ]
        )
    )

    page.add(status_card)

    # Function to update the player data and UI
    async def update_player_data():
        nonlocal player_data, name_text, level_text, hp_text, mp_text, strength_text, vitality_text, agility_text, inteligence_text, remaining_points_text, hp_progress_bar, mp_progress_bar
        player_data = player.player_data.get(player_name, {})
        name_text.value = f"NAME: {player_name}"
        level_text.value = f"LEVEL: {player_data.get('level', 1)}"
        hp_text.value = f"HP: {player_data.get('hp', 100)}"
        mp_text.value = f"MP: {player_data.get('mp', 100)}"
        strength_text.value = f"STRENGTH: {player_data.get('strenght', 1)}"
        vitality_text.value = f"VITALITY: {player_data.get('vitality', 1)}"
        agility_text.value = f"AGILITY: {player_data.get('agility', 1)}"
        inteligence_text.value = f"INTELLIGENCE: {player_data.get('inteligence', 1)}"
        remaining_points_text.value = f"REMAINING POINTS: {player_data.get('remaining_points', 0)}"
        hp_progress_bar.value = player_data.get('hp', 100) / 100
        mp_progress_bar.value = player_data.get('mp', 100) / 100
        page.update()

    # Run the update function every second
    async def periodic_update():
        while True:
            await update_player_data()
            await asyncio.sleep(1)

    # Start the periodic update task
    asyncio.create_task(periodic_update())

ft.app(target=main)

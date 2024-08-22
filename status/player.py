import json
import math

try:
    with open("player_data.json", "r") as f:
        player_data = json.load(f)
except FileNotFoundError:
    player_data = {}
    

def save_player_data():
    """Save the data of the player to a json file"""
    with open ("player_data.json", "w") as f:
        json.dump(player_data, f)


def create_new_player(player_name):
    """Creates a new player at level 1"""
    if player_name not in player_data:
        player_data[player_name] = {
            "level": 1,
            "hp": 100,
            "mp": 100,
            "job": "none",
            "experience": 0,
            "experience_to_next_level": 100,
            "strenght": 1,
            "vitality": 1,
            "agility": 1,
            "inteligence": 1,
            "remaining_points": 0,

        }
        save_player_data()
        print(f"Welcome '{player_name}'")
    else:
        print(f"It can only be one player")

def gain_experience(player_name, experience):
    """Adds experience to the player and levels them up if needed."""
    if player_name in player_data:
        player = player_data[player_name]
        player[experience] += experience
        while player["experience"] >= player["experience_to_next_level"]:
            player["level"] +=1
            player["experience"] -= player["experience_to_next_level"]
            player["experience_to_next_level"] = math.ceil(player["experience_to_next_level"] *1.05) # Increase exp needed for next level
            player["remaining_points"] += 2
            print(f"LEVEL UP! \nLevel{player['level']}" )
        save_player_data()
    else:
        print(f"The System don't recognise this player")
    
def allocate_stat_points(player_name, stat, points):
    """Allocates stat points to a stat of the player"""
    if player_name in player_data:
        player = player_data[player_name]
        if player ["remaining_points"] >= points:
            player[stat] += points
            player ["remaining_points"] -= points
            save_player_data()
            print(f"points allocatedd successfully!")
        else:
            print(f"The player dosen't have enough points.")
    else:
        print(f"The System don't recognise this player")

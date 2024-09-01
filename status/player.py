import sqlite3
import math

def create_connection():
    """Creates a new datavase connection"""
    conn = sqlite3.connect("player_data.db")
    cursor = conn.cursor()
    return conn, cursor

conn = sqlite3.connect("player_data.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        level INTEGER,
        hp INTEGER,
        mp INTEGER,
        job TEXT,
        experience INTEGER,
        experience_to_next_level INTEGER,
        strenght INTEGER,
        vitality INTEGER,
        agility INTEGER,
        inteligence INTEGER,
        status_points INTEGER
    )
""")
conn.commit()
conn.close()





def create_new_player(conn, cursor, player_name):
    """Creates a new player at level 1"""
    conn, cursor = create_connection()
    try:
        cursor.execute(
            """
            INSERT INTO players (name, level, hp, mp, job, experience, experience_to_next_level, strenght, vitality, agility, inteligence, status_points)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (player_name, 1, 100, 100, "none", 0, 100, 1, 1, 1, 1, 0),
        )
        conn.commit()
        print(f"Welcome '{player_name}'!")
    except sqlite3.IntegrityError:
        print(f"Player '{player_name}' already exists.")

def get_player_data(conn, cursor, player_name):
    """Retrives player data from the database."""
    conn, cursor = create_connection()
    try:
        cursor.execute("SELECT * FROM players WHERE name = ?", (player_name))
        player_name = cursor.fetchone()
        if player_data:
            return {
                "id": player_data[0],
                "name": player_data[1],
                "level": player_data[2],
                "hp": player_data[3],
                "mp": player_data[4],
                "job": player_data[5],
                "experience": player_data[6],
                "experience_to_next_level": player_data[7],
                "strenght": player_data[8],
                "vitality": player_data[9],
                "agility":player_data[10],
                "inteligence": player_data[11],
                "status_points": player_data[12],
            }
        else:
            return None
    finally:
        conn.close()

def save_player_data(conn, cursor, player_data):
    """Updates player data in database."""
    cursor.execute(
        """
        UPDATE players SET
            level = ?,
            hp = ?,
            mp - ?,
            job = ?.
            experience = ?,
            experience_to_next_level = ?,
            strenght = ?,
            vitality = ?,
            agility = ?,
            inteligence = ?,
            status_points = ?,
        WHERE id = ?
        """,
        (
            player_data["level"],
            player_data["hp"],
            player_data["mp"],
            player_data["job"],
            player_data["experience"],
            player_data["experience_to_next_level"],
            player_data["strenght"],
            player_data["vitality"],
            player_data["agility"],
            player_data["inteligence"],
            player_data["status_points"],
            player_data["id"],
        ),
    )
    conn.commit()


def gain_experience(conn, cursor, player_name, experience):
    """Adds experience to the player and levels them up if needed."""
    player_data = get_player_data(conn, cursor, player_name)
    if player_data:
        player_data["experience"] += experience
        while player_data["experience"] >= player_data["experience_to_next_level"]:
            player_data["level"] += 1
            player_data["experience"] -= player_data["experience_to_next_level"]
            player_data["experience_to_next_level"] = math.ceil(player_data["experience_to_next_level"] * 1.05)
            player_data["remaining_points"] += 2
            print(f"LEVEL UP! \nlevel {player_data['level']}")
        save_player_data(conn, curosr, player_data)
    else:
        print(f"The System don't recognise this player")

    
def allocate_stat_points(player_name, stat, points):
    """Allocates stat points to a stat of the player"""
    player_data = get_player_data(conn, cursor, player_name)
    if player_data:
        if player_data["status_points"] >= points:
            player_data[stat] += points
            player_data["status_points"] -= points
            save_player_data(conn, cursor, player_data)
        else:
            print(f"The player dpsen't ahve enough points.")
    else:
        print(f"the System don't recognise this player")

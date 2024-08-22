import datetime
import json
import flet as ft

# Load existing habits from a json if it dosen't exist load a a empty dictionary
try:
    with open("habits.json","r") as f:
        habits = json.load(f)
except FileNotFoundError:
    habits = {}

def add_habit(habit):
    """adds a new habit to the tracker."""
    if habit not in habits:
        habits[habit] = []
        save_habits()
        print(f"Habit '{habit}' added!")
    else:
        print(f"Habit '{habit}' already exists.")

def mark_habit_done(habit):
    """ records that a habit was complet today."""
    if habit in habits:
        today = datetime.date.today().strftime("%Y-%m-%d")  
        habits[habit].append(today)
        save_habits()
        print(f" congratulations \nHabit '{habit}' was completed today.")
    else:
        print(f"Habit '{habit}' not found.")

def view_habits():
    """ Displays all habits and their completion history."""
    if habits:
        for habit, dates in habits.items():
            print(f"Habit: {habit}")
            print(f"  Completed on: {dates}")
    else:
        print("No habits added yet.")

def view_habit_progress(habit):
    """Shows the progress of a specific habit."""
    if habit in habits:
        dates = habits[habit]
        print(f"Habit: {habit}")
        print(f"  Completed on: {dates}")
    else:
        print(f"Habit '{habit}' not found.")

def save_habits():
    """Save the habits dictionary to json file"""
    with open("habits.json", "w") as f:
        json.dump(habits, f)

def delete_habit(habit):
    """Deletes a habit from the tracker"""
    if habit in habits:
        del habits[habit]
        save_habits()
        print(f"Habit '{habit}' deleted!")
    else:
        print(f"Habit '{habit}' not found.")

import json
import os

SAVE_FILE = "save.json"

def save_game(state):
    with open(SAVE_FILE, "w") as f:
        json.dump(state, f)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE) as f:
            return json.load(f)
    return None

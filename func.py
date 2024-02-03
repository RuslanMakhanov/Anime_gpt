import json
from datetime import datetime


def get_time_text(date=False):
    current_time = datetime.now()
    if date:
        return current_time.strftime("%Y-%m-%d %H:%M")
    else:
        return current_time.strftime("%H:%M")


def save_in_json(var, file_dir):
    with open(file_dir, 'w') as file:
        json.dump(var, file)

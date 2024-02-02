import json


def save_in_json(var, file_dir):
    with open(file_dir, 'w') as file:
        json.dump(var, file)

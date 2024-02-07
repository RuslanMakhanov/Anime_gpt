import json
from datetime import datetime
import config as cfg

try:
    with open(cfg.trigger_words_file, 'r') as file_trigger_words:
        trigger_words_data = {'trigger_words': [line.strip() for line in file_trigger_words.readlines()]}
        print('Trigger_words_data is loading SEXessful')
except FileNotFoundError:
    print("Trigger_words_file not found, we make a new :)")
    trigger_words_data = {'trigger_words': []}


def load_json_file(dir_file):
    try:
        with open(dir_file, 'r') as file:
            print(f"{dir_file} is loading secesfull")
            return json.load(file)
    except FileNotFoundError:
        print(f"{dir_file} not found")
        return {}


def get_time_text(date=False):
    current_time = datetime.now()
    if date:
        return current_time.strftime("%Y-%m-%d %H:%M")
    else:
        return current_time.strftime("%H:%M")


def save_in_json(var, file_dir):
    with open(file_dir, 'w') as file:
        json.dump(var, file)


user_states = load_json_file(cfg.user_states_file)


def set_user_state(msg, state):
    user_id = str(msg.from_user.id)
    user_states[user_id] = state
    save_in_json(user_states, cfg.user_states_file)


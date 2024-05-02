import json
from datetime import datetime
import config as cfg
import re

try:
    with open(cfg.trigger_words_file, 'r') as file_trigger_words:
        trigger_words_data = {'trigger_words': [line.strip() for line in file_trigger_words.readlines()]}
        print(f'{cfg.trigger_words_file} is loading SEXessful')
except FileNotFoundError:
    print(f"{cfg.trigger_words_file} not found, we make a new :)")
    trigger_words_data = {'trigger_words': []}


def check_date_format(text):
    pattern = r'\d{4}-\d{2}-\d{2}'
    if re.match(pattern, text):
        return True
    else:
        return False


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
smoke_free_users = load_json_file(cfg.smoke_free_json)


def set_user_state(msg, state):
    user_id = str(msg.from_user.id)
    user_states[user_id] = state
    save_in_json(user_states, cfg.user_states_file)


def set_user_smoke_free(msg, date):
    user_id = str(msg.from_user.id)
    smoke_free_users[user_id] = date
    save_in_json(smoke_free_users, cfg.smoke_free_json)


def days_since_last(last_date) -> int:
    """На вход принимает дату ГГГГ-ММ-ДД:str и возвращает количество дней прошедших с этой даты"""
    try:
        # Преобразование строковых дат в объекты datetime
        last_watering_date = datetime.strptime(last_date, '%Y-%m-%d')
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date, '%Y-%m-%d')
        # Вычисление разницы между датами
        days_difference = (current_date - last_watering_date).days
        return days_difference
    except TypeError:
        return 0

import json
from datetime import datetime
import config as cfg

# Загружаем существующие триггерные слова из файла
try:
    with open(cfg.trigger_words_file, 'r') as file_trigger_words:
        trigger_words_data = {'trigger_words': [line.strip() for line in file_trigger_words.readlines()]}
        print('Trigger_words_data is loading SEXessful')
except FileNotFoundError:
    print("Trigger_words_file not found, we make a new :)")
    trigger_words_data = {'trigger_words': []}

# Загрузка данных из файла
try:
    with open(cfg.user_states_file, 'r') as file_user_states:
        user_states = json.load(file_user_states)
        print("User_states is loading SEXessful")
except FileNotFoundError:
    # Если файл не найден, начинаем с пустого словаря
    user_states = {}
    print("User_states_file not found, we make a new :)")


def get_time_text(date=False):
    current_time = datetime.now()
    if date:
        return current_time.strftime("%Y-%m-%d %H:%M")
    else:
        return current_time.strftime("%H:%M")


def save_in_json(var, file_dir):
    with open(file_dir, 'w') as file:
        json.dump(var, file)


def set_user_state(msg, state):
    user_id = str(msg.from_user.id)
    user_states[user_id] = state
    save_in_json(user_states, cfg.user_states_file)


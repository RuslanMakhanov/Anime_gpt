import json

from aiogram.filters import Command
from aiogram.types import Message

import config as cfg
import func
from RPG import get_rpg_game
from anime import anime_girl
from misc import dp

version = "0.0.9 Async update (aiogram)"

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


@dp.message(Command("start"))
async def start_handler(msg: Message):
    user_name = msg.from_user.username
    user_id = str(msg.from_user.id)

    # Отправляем приветственное сообщение
    if user_id not in user_states:
        await msg.answer(f"Привет, {user_name}! Теперь бот готов с вами общаться, напиши ей. "
                         "\nНапример: Аска, привет. Я новый пользователь. Расскажи о себе.")
        print(f'A new user: {user_name}, with user_id: {user_id}')
    else:
        await msg.answer(f"И снова привет, {user_name}! Бот готов с вами общаться, напиши ей. "
                         "\nНапример: Аска, привет. Я новый пользователь. Расскажи о себе.")
    user_states[user_id] = 'idle'
    func.save_in_json(user_states, cfg.user_states_file)


@dp.message(Command("id"))
async def chat_id(msg: Message):
    chat_id = str(msg.chat.id)
    await msg.answer("ИД данного чата: " + chat_id)


@dp.message(Command("add_trigger"))
async def handle_waiting_for_new_trigger_word(msg: Message):
    # Получаем текст сообщения
    original_text = msg.text
    user_name = msg.from_user.username
    # Удаляем слово из текста
    new_trigger_word = original_text.replace("/add_trigger", "").strip().lower()

    # Проверяем, что новое триггерное слово не повторяется
    if new_trigger_word not in trigger_words_data['trigger_words'] and len(new_trigger_word) != 0:
        # Добавляем триггерное слово в список
        trigger_words_data['trigger_words'].append(new_trigger_word)

        # Сохраняем обновленные триггерные слова в файл
        with open(cfg.trigger_words_file, 'a') as file:
            file.write(new_trigger_word + '\n')

        # Отвечаем на сообщение
        await msg.answer(f'Триггерное слово "{new_trigger_word}" добавлено успешно!')
        print(f'{user_name}: Триггерное слово "{new_trigger_word}" добавлено успешно!')
    elif len(new_trigger_word) <= 0:
        await msg.answer(f'Вы не ввели слово')
    else:
        await msg.answer(f'Триггерное слово "{new_trigger_word}" уже существует!')


@dp.message(Command("version"))
async def handle_version(msg: Message):
    await msg.answer(version)


@dp.message(Command("rpg"))
async def handle_rpg(msg: Message):
    user_id = str(msg.from_user.id)
    if user_states.get(user_id) == 'idle':
        await msg.answer('Вы находитесь в текстовом РПГ, для выхода напишите '
                         '/exit, или для начала напишите Старт.')
        user_states[user_id] = 'in_rpg_game'
        func.save_in_json(user_states, cfg.user_states_file)


@dp.message(Command("exit"))
async def handle_exit(msg: Message):
    user_id = str(msg.from_user.id)
    if user_states.get(user_id) != 'idle':
        await msg.answer('Ваш статус "idle", вы можете продолжать общаться с Аской')
        user_states[user_id] = 'idle'
        func.save_in_json(user_states, cfg.user_states_file)


@dp.message(Command("status"))
async def handle_status(msg: Message):
    user_id = str(msg.from_user.id)
    await msg.answer(user_states.get(user_id))


@dp.message(Command("idle"))
async def handle_idle(msg: Message):
    user_id = str(msg.from_user.id)
    await msg.answer('Вы установили статус "idle"')
    user_states[user_id] = 'idle'
    func.save_in_json(user_states, cfg.user_states_file)


@dp.message()
async def message_handler(msg: Message):
    user_name = msg.from_user.username
    user_id = str(msg.from_user.id)
    if msg.text is not None:
        if (any(word in msg.text.lower() for word in trigger_words_data['trigger_words'])
                and user_states.get(user_id) == 'idle'):
            print(f'Update is handled from {user_name}:{user_id}')
            await msg.answer(anime_girl(msg.text, user_name, user_id))

        elif user_states.get(user_id) == 'in_rpg_game':
            await msg.answer(get_rpg_game(msg.text, user_name, user_id))
            pass

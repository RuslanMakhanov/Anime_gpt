from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from func import *
from RPG import get_rpg_game
from anime import anime_girl
from misc import dp

from menu import *

version = "0.0.10 RaspberyPi"


def create_menu_handler(menu_list, menu_actions):
    @dp.message(lambda message: message.text in menu_list)
    async def create_menu(msg: Message):
        await handle_menu(msg, menu_actions)


async def handle_menu(msg, menu_actions):
    """
    Обработка действий меню
    :param msg: Message
    :param menu_actions: Словарь действий
    """
    selected_option = menu_actions.get(msg.text)
    if selected_option:
        user_state, response_text, reply_markup = selected_option
        set_user_state(msg, user_state)
        await msg.delete()
        await msg.answer(response_text, reply_markup=reply_markup)
    else:
        await msg.answer("Неизвестная опция в меню.")


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

    set_user_state(msg, 'idle')


@dp.message(Command("menu"))
async def get_menu(msg: Message):
    await msg.answer("🏡 Вы в главном меню 🏡", reply_markup=main_menu_1)
    set_user_state(msg, "idle")


@dp.message(Command("id"))
async def get_chat_id(msg: Message):
    chat_id = str(msg.chat.id)
    await msg.answer("ИД данного чата: " + chat_id)


@dp.message(Command("self_image"))
async def sent_self_image(msg: Message):
    await msg.answer_photo(photo=FSInputFile('image.jpeg'))


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
        set_user_state(msg, "in_rpg_game")


@dp.message(Command("exit"))
async def handle_exit(msg: Message):
    user_id = str(msg.from_user.id)
    if user_states.get(user_id) != 'idle':
        await msg.answer('Ваш статус "idle", вы можете продолжать общаться с Аской')
        set_user_state(msg, "idle")


@dp.message(Command("status"))
async def handle_status(msg: Message):
    await msg.answer(f"{get_time_text()} - Включен")


@dp.message(Command("idle"))
async def handle_idle(msg: Message):
    user_id = str(msg.from_user.id)
    await msg.answer('Вы установили статус "idle"')
    set_user_state(msg, "idle")


create_menu_handler(main_menu_list,main_menu_actions)


@dp.message(lambda message: message.text == "Назад")
async def back(msg: Message):
    user_id = str(msg.from_user.id)
    if user_states.get(user_id) in ["settings", "debug", "games"]:
        set_user_state(msg, "idle")
        await msg.delete()
        await msg.answer("🏡 Вы в главном меню 🏡", reply_markup=main_menu_1)


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


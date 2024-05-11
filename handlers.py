from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from func import *
from anime import anime_girl
from misc import dp
from aiogram import F

version = "0.1.0 Raspberry Pi"


@dp.message(Command("start"))
async def start_handler(msg: Message):
    user_name = msg.from_user.username
    user_id = str(msg.from_user.id)

    # Отправляем приветственное сообщение
    if user_id not in user_states:
        await msg.answer(f"Привет, {user_name}! Теперь бот готов с вами общаться, напиши ей. "
                         "\nНапример: Аска, привет. Я новый пользователь. Расскажи о себе.", reply_markup=None)
        print(f'{get_time_text(date=True)}: A new user: {user_name}, with user_id: {user_id}')
    else:
        await msg.answer(f"И снова привет, {user_name}! Бот готов с вами общаться, напиши ей. "
                         "\nНапример: Аска, привет. Что нового у тебя.", reply_markup=None)

    set_user_state(msg, 'idle')


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


@dp.message(Command("status"))
async def handle_status(msg: Message):
    await msg.answer(f"{get_time_text()} - Включен")


@dp.message(Command("idle"))
async def handle_idle(msg: Message):
    await msg.answer('Вы установили статус "idle"')
    set_user_state(msg, "idle")


@dp.message(F.text)
async def message_handler(msg: Message):
    await text_handler_from_user(msg, msg.text)


async def text_handler_from_user(msg, text):
    user_name = msg.from_user.username
    user_id = str(msg.from_user.id)
    if text is not None:
        if (any(word in text.lower() for word in trigger_words_data['trigger_words'])
                and user_states.get(user_id) == 'idle'):
            print(f'{get_time_text(date=True)}: Update is handled from {user_name}:{user_id}')
            await msg.answer(anime_girl(text, user_name, user_id))


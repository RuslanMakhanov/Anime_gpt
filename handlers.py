from aiogram.filters import Command
from aiogram.types import Message

from func import *
from RPG import get_rpg_game
from anime import anime_girl
from misc import dp
from aiogram import F
from modules.stt import save_voice_as_mp3, audio_to_text
from modules.anime_one import send_anime_girl
from modules.waifu_module import get_image

version = "0.1.0 Raspberry Pi"


def delete_word(original_text, text_to_delete):
    # Удаляем слово из текста
    replace_text = original_text.replace(text_to_delete, "").strip().lower()
    return replace_text

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


@dp.message(Command("waifu"))
async def sent_waifu_image(msg: Message):
    image_url = await get_image()
    if image_url:
        if ".gif" in image_url:
            await msg.answer_animation(animation=image_url)
        else:
            await msg.answer_photo(photo=image_url)

    else:
        await msg.answer("URL Пустой")



@dp.message(Command("add_trigger"))
async def handle_waiting_for_new_trigger_word(msg: Message):
    # Получаем текст сообщения
    original_text = msg.text
    user_name = msg.from_user.username
    # Удаляем слово из текста
    new_trigger_word = delete_word(original_text=original_text, text_to_delete="/add_trigger")

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
    await msg.answer('Вы установили статус "idle"')
    set_user_state(msg, "idle")


@dp.message(Command("smoke_free"))
async def smoke_free_handler(msg: Message):
    # Получаем текст сообщения
    original_text = msg.text
    user_name = msg.from_user.username
    # Удаляем слово из текста
    replace_text = original_text.replace("/smoke_free", "").strip().lower()
    if replace_text:
        if check_date_format(replace_text):
            set_user_smoke_free(msg=msg, date=replace_text)
            await msg.answer(send_anime_girl(task=f"уведомление что успешно установлена дата когда {user_name} бросил курить:{replace_text}", user_name=msg.from_user.username))
        else:
            await msg.answer("Дата введена не верно попробуйте еще раз\nПример: /smoke_free 2024-04-28")
    else:
        await msg.answer("Введите дату, когда вы бросили курить!\nПример: /smoke_free 2024-04-28")

    pass

# Это то самое где бот говорил страшным голосом? 
@dp.message(F.voice)
async def audio(msg: Message):
    mp3_voice_path = await save_voice_as_mp3(voice=msg.voice)
    stt_text = await audio_to_text(mp3_voice_path)
    if stt_text:
        await text_handler_from_user(msg, stt_text)


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

        elif user_states.get(user_id) == 'in_rpg_game':
            await msg.answer(get_rpg_game(text, user_name, user_id))
            pass

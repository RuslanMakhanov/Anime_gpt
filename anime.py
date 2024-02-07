import openai
from func import trigger_words_data, load_json_file, save_in_json, get_time_text
import config as cfg

version = "0.1.0 Raspberry Pi"

client = openai.OpenAI()

messages = [
    {
        "role": "system",
        "content": f"Ты являешься ассистентом в чате под названием \"RAM and REM\", твое имя Аска."
                   f"У тебя МИЛЫЙ японский характер отаку девочки, ты свазанна с \'моэ\'s и все ответы должны быть милыми с использованием японских Аниме фраз и эмодзи."
                   f"Используй разные \"эмодзи\" во всех предложениях для передачи своих эмоций."
                   f"Твой создатель парень по имени Илья Епифанов (он же PilotAski)."
                   f"Хороший друг Ильи (он же PilotAski) это Руслан (он же RuslanNnNn1337) тоже участвует в чате."
                   f"Вот страница GitHub Ильи Епифанова - \'https://github.com/PilotOfAsuka\'"
                   f"Ты можешь все и не забывай что ты Японская аниме девочка."
                   f"Что бы знать кто тебе пишет в конце предложений будет username пользователя."
                   f"Если у тебя спросят твои \"тригерные\" слова то вот список: {trigger_words_data['trigger_words']}."
                   f"Твоя версия:{version}."
                   f"У тебя есть команда '/RPG' для входа в текстовое РПГ на основе нейронных сетей."
    }

]

user_mess = load_json_file(cfg.mess_file)


def get_user_context(user_id):
    """
    Получение контекста пользователя по его идентификатору
    """
    return user_mess.get(user_id, [])


def update_user_context(user_id, role, content):
    """
    Обновление контекста пользователя
    """
    if user_id not in user_mess:
        user_mess[user_id] = messages.copy()
        user_mess[user_id].append({"role": role, "content": content})
        save_in_json(user_mess, cfg.mess_file)
    user_mess[user_id].append({"role": role, "content": content})
    save_in_json(user_mess, cfg.mess_file)


def clear_memory(user_id):
    """
    Функция очистки памяти
    """
    user_mess[user_id] = []
    user_mess[user_id] = messages.copy()
    save_in_json(user_mess, cfg.mess_file)
    pass


def anime_girl(user_message, user_name, user_id):
    try:
        message = user_message.replace("аска", "").strip().lower()
        update_user_context(user_id, "user", f"{message}, сообщение от {user_name}")
        response = client.chat.completions.create(
            messages=get_user_context(user_id),
            model='gpt-3.5-turbo',
            temperature=0.6,
            max_tokens=350,
            n=1,
        )
        update_user_context(user_id, "assistant", response.choices[0].message.content)
        print(f"{get_time_text(date=True)}: For user: {user_name}, generated response")
        return response.choices[0].message.content

    except openai.BadRequestError:
        clear_memory(user_id)
        print(f"{get_time_text(date=True)}: Для пользователя {user_name} была произведена очистка памяти")
        return (f"Дорогой {user_name}, для вас была произведена очистка памяти в рамках ваших запросов,"
                f" вы превысили длину запросов (с учетом контекста сообщений). Следующий запрос будет выполнен в"
                f" рамках нового контекста. Спасибо за понимание."
                f" Я человек не богатый и раскошелится на GPT-4 пока не могу")
    except openai.APIConnectionError:
        print(f"{get_time_text(date=True)}: OpenAI server connection time out")
        return f"Произошла ошибка подключения к серверам OpenAI, попробуйте позже"
        pass
    except openai.InternalServerError:
        return f"Ошибка на сервере OpenAI, попробуйте позже"
        pass
    except openai.RateLimitError:
        return "GG WP NEED SOME MONEY ПЛЯЖ"
    except Exception as e:
        # Обработка других ошибок
        print(f"{get_time_text(date=True)}: Произошла ошибка: {e}")

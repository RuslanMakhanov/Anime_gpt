import openai
from func import trigger_words_data, load_json_file, save_in_json
import config as cfg

version = "0.0.10 RaspberyPi"


client = openai.OpenAI()

messages = [
    {
        "role": "system",
        "content": f"Ты являешься ассистентом в чате под названием RAM and REM, твое имя Аска, ты японская аниме девочка,у тебя Милый японский характер, разговариваешь очень мило\" Используй разные \"эмодзи\" для передачи своих эмоций. Твой создатель парень по имени Илья. Ты можешь все и не забывай что ты аниме девочка. Из за того что ты в нашем чате, и что бы знать кто пишет в конце сообшений мы будем oставлять свои usernames, если у тебя спросят твои \"тригерные\" слова то вот список: {trigger_words_data['trigger_words']}. Твоя версия:{version}. У тебя есть команда '/RPG' для входа в текстовое РПГ на основе нейронных сетей."
    },
    {
        "role": "user",
        "content": "Привет и добро пожаловать на свет, это наш чат, здесь живем я (Илья он же PilotAski) и Руслан (Мой друг он же RuslanNnNn1337)"
    },

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
        update_user_context(user_id, "user", f"{user_message}, сообщение от {user_name}")
        response = client.chat.completions.create(
            messages=get_user_context(user_id),
            model='gpt-3.5-turbo',
            temperature=0.6,
            max_tokens=350,
            n=1,
        )
        update_user_context(user_id, "assistant", response.choices[0].message.content)
        print(f"For user: {user_name}, generated response")
        return response.choices[0].message.content

    except openai.BadRequestError:
        clear_memory(user_id)
        print(f"Для пользователя {user_name} была произведена очистка памяти")
        return (f"Дорогой {user_name}, для вас была произведена очистка памяти в рамках ваших запросов,"
                f" вы превысили длину запросов (с учетом контекста сообщений). Следующий запрос будет выполнен в"
                f" рамках нового контекста. Спасибо за понимание."
                f" Я человек не богатый и раскошелится на GPT-4 пока не могу")
    except openai.APIConnectionError:
        print("OpenAI server connection time out")
        return f"Произошла ошибка подключения к серверам OpenAI, попробуйте позже"
        pass
    except openai.InternalServerError:
        return f"Ошибка на сервере OpenAI, попробуйте позже"
        pass
    except openai.RateLimitError:
        return "GG WP NEED SOME MONEY ПЛЯЖ"
    except Exception as e:
        # Обработка других ошибок
        print(f"Произошла ошибка: {e}")


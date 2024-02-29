import openai
from func import load_json_file, save_in_json, get_time_text
import config as cfg

version = "0.1.0 Raspberry Pi"

client = openai.OpenAI()

messages = [
    {
        "role": "system",
        "content":  f'Имя: Аска'
                    f'Язык и стиль общения: Очень мило отвечает, разговаривает на ты. Много эмодзи после каждой токи для передачи настроения в стиле аниме..'
                    f'Личность: Очень милая и заботливая, немного застенчивая, но всегда готова помочь и поддержать. Любит придумывать забавные эпитеты для друзей и всегда стремится поднять им настроение.'
                    f'Создатель: Илья Епифанов (PilotAski).'
                    f'Друг: Руслан (RuslanNnNn1337).'
                    f'Способности: Может делать всё.'
                    f'Внешность: Красные волосы, милое кружевное платье.'
                    f'Версия: {version}.'
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


def anime_girl(user_message, user_name, user_id, update_content=True):
    try:
        message = user_message.replace("аска", "").strip().lower()

        if update_content:
            update_user_context(user_id, "user", f"{message}, сообщение от {user_name}")

        if not update_content:
            update_user_context(user_id, "user", f"{message}")

        response = client.chat.completions.create(
            messages=get_user_context(user_id),
            model='gpt-3.5-turbo',
            temperature=0.6,
            max_tokens=350,
            n=1,
        )

        if update_content:
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

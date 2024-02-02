import openai



version = "0.0.8 RPG update"

client = openai.OpenAI()


messages = [
    {
        "role": "system",
        "content": f"Ты ведущий текстовой РПГ, ты придумываешь сеттинг в рандомном стиле, первым сообщением ты рассказываешь мини историю персонажа. Тебе нужно писать действия что бы игрок их выбирал и на основе их делать действия. Старайся делать все коротко и информативно."
    }
]

user_mess = {}


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

    user_mess[user_id].append({"role": role, "content": content})


def clear_memory(user_id):
    """
    Функция очистки памяти
    """
    user_mess[user_id] = []
    user_mess[user_id] = messages.copy()
    pass


def get_rpg_game(user_message, user_name, user_id):
    try:
        update_user_context(user_id, "user", f"{user_message}")
        response = client.chat.completions.create(
            messages=get_user_context(user_id),
            model='gpt-3.5-turbo',
            temperature=0.6,
            max_tokens=350,
            n=1,
        )
        update_user_context(user_id, "assistant", response.choices[0].message.content)
        return response.choices[0].message.content

    except openai.BadRequestError:
        clear_memory(user_id)
        print(f"Для пользователя {user_name} была произведена очистка памяти")
        return (f"Дорогой {user_name}, для вас была произведена очистка памяти в рамках ваших запросов,"
                f" вы превысили длину запросов (с учетом контекста сообщений). Следующий запрос будет выполнен в"
                f" рамках нового контекста. Спасибо за понимание."
                f" Я человек не богатый и раскошелится на GPT-4 пока не могу")

    except openai.APIConnectionError:
        return f"Произошла ошибка подключения к серверам OpenAI, попробуйте позже"
        pass
    except openai.InternalServerError:
        return f"Ошибка на сервере OpenAI, попробуйте позже"
        pass

    except Exception as e:
        # Обработка других ошибок
        print(f"Произошла ошибка: {e}")


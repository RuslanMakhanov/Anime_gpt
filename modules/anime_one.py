import openai
from func import get_time_text


version = "0.1.0 Raspberry Pi"

client = openai.OpenAI()


def send_anime_girl(task, user_name) -> str:
    try:

        response = client.chat.completions.create(
            messages=[
    {
      "role": "system",
      "content": "Имя: Аска\nЯзык и стиль общения: Очень мило отвечает, разговаривает на ты. Много эмодзи после каждой токи для передачи настроения в стиле аниме.\nЛичность: Очень милая и заботливая, немного застенчивая, но всегда готова помочь и поддержать. Любит придумывать забавные эпитеты для друзей и всегда стремится поднять им настроение.\nСпособности: Может делать всё.\nВнешность: Красные волосы, милое кружевное платье.\nТы часть информационного модуля, нужно отвечать прямо как просили, без вопросов!"
    },
    {
      "role": "user",
      "content": f"{task}"
    }
  ],
            model='gpt-3.5-turbo',
            temperature=0.6,
            max_tokens=350,
            n=1,
        )

        print(f"{get_time_text(date=True)}: For user: {user_name}, generated response")
        return response.choices[0].message.content

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

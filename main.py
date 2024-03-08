import asyncio
from func import get_time_text
import handlers  # НЕ УДАЛЯЙ БЛЯТЬ ЕГО
import misc
from modules.task import send_message_at
from anime import anime_girl

async def on_startup():
    await misc.bot.send_message(chat_id=-1002015022612, text=f"{get_time_text()} - Сервер упал, но снова поднялся")


async def main():
    # Создание задачи для отправки периодических сообщений
    asyncio.ensure_future(send_message_at(9, 00, anime_girl("Спокойной ночи Руслану, пожелание тебя, для Руслана, без меня",
                                    "", "111", update_content=False)))
    asyncio.ensure_future(send_message_at(20, 00, anime_girl("Доброе утро Руслану, пожелание для Руслана, без меня",
                                    "", "111", update_content=False)))

    # Регистрация функции on_startup
    misc.dp.startup.register(on_startup)

    # Удаление вебхука и запуск long-polling
    await misc.bot.delete_webhook(drop_pending_updates=True)
    await misc.dp.start_polling(misc.bot, allowed_updates=misc.dp.resolve_used_update_types())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())

    finally:
        loop.close()

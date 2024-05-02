import asyncio
from func import get_time_text, days_since_last, smoke_free_users
import handlers  # НЕ УДАЛЯЙ БЛЯТЬ ЕГО
import misc
from modules.task import send_message_at
from modules.anime_one import send_anime_girl

ram_rem_chat = '-1002015022612'
ls = '5848061277'

async def on_startup():
    await misc.bot.send_message(chat_id=ls, text=f"{get_time_text()} - Сервер упал, но снова поднялся")


async def main():
    # Создание задачи для отправки периодических сообщений
    asyncio.ensure_future(send_message_at(hour=9, minutes=00, text=send_anime_girl("Спокойной ночи Руслану, пожелание тебя, для Руслана", "admin",), chat_id=ram_rem_chat))
    asyncio.ensure_future(send_message_at(hour=20, minutes=00, text=send_anime_girl("Доброе утро Руслану, пожелание для Руслана","admin",), chat_id=ram_rem_chat))
    asyncio.ensure_future(send_message_at(hour=13, minutes=00, text=send_anime_girl(task=f"Илья(PilotAski) не курит уже {days_since_last(smoke_free_users.get('5848061277'))}, пожелание ему!", user_name="admin"), chat_id=ram_rem_chat))

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

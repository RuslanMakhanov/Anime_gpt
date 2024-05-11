import asyncio
from func import get_time_text
import handlers  # НЕ УДАЛЯЙ БЛЯТЬ ЕГО
import misc

ram_rem_chat = '-1002015022612'
ls = '5848061277'

async def on_startup():
    await misc.bot.send_message(chat_id=-1002015022612, text=f"{get_time_text()} - Сервер упал, но снова поднялся")


async def startup_task():
    # Регистрация функции on_startup
    misc.dp.startup.register(on_startup)

    # Удаление вебхука и запуск long-polling
    await misc.bot.delete_webhook(drop_pending_updates=True)
    await misc.dp.start_polling(misc.bot, allowed_updates=misc.dp.resolve_used_update_types())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(asyncio.gather(startup_task()))

    finally:
        loop.close()

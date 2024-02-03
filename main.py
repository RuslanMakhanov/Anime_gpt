import asyncio

import func
import handlers  # НЕ УДАЛЯЙ БЛЯТЬ ЕГО
import misc


async def on_startup():
    await misc.bot.send_message(chat_id=-1001715912916, text=f"{func.get_time_text()} - Сервер упал, но снова поднялся")


async def main():
    misc.dp.startup.register(on_startup)
    await misc.bot.delete_webhook(drop_pending_updates=True)
    await misc.dp.start_polling(misc.bot, allowed_updates=misc.dp.resolve_used_update_types())


if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    finally:
        loop.close()

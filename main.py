import asyncio
from datetime import datetime, timedelta

from func import get_time_text
import handlers  # НЕ УДАЛЯЙ БЛЯТЬ ЕГО
import misc

async def on_startup():
    await misc.bot.send_message(chat_id=-1002015022612, text=f"{get_time_text()} - Сервер упал, но снова поднялся")

# Функция, которая отправляет сообщение каждые N секунд
# Функция, которая отправляет сообщение в 22:00 каждый день
async def send_message_at_22():
    while True:
        # Получаем текущее время
        now = datetime.now()

        # Вычисляем время до 22:00 сегодня
        target_time = datetime(now.year, now.month, now.day, 22, 0)
        if now > target_time:
            # Если уже прошло 22:00 сегодня, переходим к 22:00 следующего дня
            target_time += timedelta(days=1)

        # Ожидаем до момента отправки сообщения в 22:00
        await asyncio.sleep((target_time - now).total_seconds())

        # Отправляем сообщение
        await misc.bot.send_message(chat_id='-1002015022612', text='Привет, оповещение в 22:00')

async def main():
    # Создание задачи для отправки периодических сообщений
    asyncio.ensure_future(send_message_at_22())

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

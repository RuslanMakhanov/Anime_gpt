from datetime import datetime, timedelta
import misc
import asyncio


# Функция, которая отправляет сообщение в N часов каждый день
async def send_message_at(hour, minutes, text):
    # 'ВРЕМЯ' - hours, minutes
    while True:
        # Получаем текущее время
        now = datetime.now()

        # Вычисляем время до 'ВРЕМЯ' сегодня
        target_time = datetime(now.year, now.month, now.day, hour, minutes)
        if now > target_time:
            # Если уже прошло 'ВРЕМЯ' сегодня, переходим к 'ВРЕМЯ' следующего дня
            target_time += timedelta(days=1)

        # Ожидаем до момента отправки сообщения
        await asyncio.sleep((target_time - now).total_seconds())

        # Отправляем сообщение
        await misc.bot.send_message(chat_id='-1002015022612',
                                    text=text)

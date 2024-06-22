import random
import asyncpraw

# ЭТО ЖЕ НАДО УБРАТЬ ТЫ ЧЕ ИЛЬЯ ИЛЬЯ ЗАЧЕМ ТЫ ЧЕ
async def get_image_url(subreddit_name):
    # Укажите ваши данные для аутентификации
    client_id = 'gQbpQ1gPPg6AtyiHTq82Sw'
    client_secret = 'Wh4ch68bTL3B2SRiUWy2K8X1W79Drg'
    user_agent = 'GetWaifuImages/0.0.1 by PilotOfAsuka'

    # Создание экземпляра Reddit
    reddit = asyncpraw.Reddit(client_id=client_id,
                              client_secret=client_secret,
                              user_agent=user_agent)

    # Получение сабреддита
    subreddit = await reddit.subreddit(subreddit_name)

    urls = []
    # Получение топовых постов из сабреддита
    async for submission in subreddit.top(limit=150):
        # Проверка, содержит ли пост изображение
        if submission.url.endswith(('jpg', 'jpeg', 'png', 'gif')):
            urls.append(submission.url)

    random.shuffle(urls)

    if urls:
        return random.choice(urls)  # Выбор случайного URL
    else:
        return None

subreddit_names = [
    'AnimeGirls',
    'AnimeART',
]


async def get_image():
    image_url = await get_image_url(random.choice(subreddit_names))
    return image_url


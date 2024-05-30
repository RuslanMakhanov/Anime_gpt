import requests
import random

# Категории из api.waifu.pics
waifu_sfw = [
    "waifu",
    "neko",
    "awoo",
    "lick",
]

waifu_nsfw = [
    "waifu",
    "neKo"
]


def get_random_category(list_of_category) -> str:
    """Возвращает рандомную категорию из списка"""
    category = random.choice(list_of_category)
    return category


def set_api_url(nsfw=False) -> str:
    api_url = f'https://api.waifu.pics/{"sfw" if nsfw is False else "nsfw"}/{get_random_category(waifu_sfw if nsfw is False else waifu_nsfw)}'
    return api_url


def set_api_url_tr(nsfw=False) -> str:
    api_url = f'https://api.waifu.pics/{"sfw" if nsfw is False else "nsfw"}/trap'
    return api_url


def get_data_from_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['url']
    else:
        print('Request failed with status code:', response.status_code)
        return None


print(get_data_from_response(set_api_url_tr(nsfw=True)))

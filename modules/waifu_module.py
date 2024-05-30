import requests
import random

# Категории из api.waifu.pics
waifu_sfw = [
    "waifu",
    "neko",
    "shinobu",
    "megumin",
    "cuddle",
    "cry",
    "hug",
    "awoo",
    "kiss",
    "lick",
    "pat",
    "smug",
    "blush",
    "smile",
    "wave",
    "highfive",
    "handhold",
    "nom",
    "bite",
    "glomp",
    "happy",
    "wink",
    "dance",
]


def get_random_category(list_of_category) -> str:
    """Возвращает рандомную категорию из списка"""
    category = random.choice(list_of_category)
    return category


def set_api_url(nsfw=False) -> str:
    api_url = f'https://api.waifu.pics/{"sfw" if nsfw is False else "nsfw"}/{get_random_category(waifu_sfw)}'
    return api_url


def get_data_from_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['url']
    else:
        print('Request failed with status code:', response.status_code)
        return None


print(get_data_from_response(set_api_url()))

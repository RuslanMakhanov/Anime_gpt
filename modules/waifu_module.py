import requests

api_url = 'https://api.waifu.im/search'


def get_waifu():

    params = {
        'included_tags': ['maid'],

    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data["images"][0]['url']
        # Process the response data as needed
    else:
        print('Request failed with status code:', response.status_code)
        return None

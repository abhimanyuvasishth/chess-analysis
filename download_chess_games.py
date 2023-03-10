import json
import os
import urllib
import urllib.request

from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('CHESS_USERNAME')
BASE_URL = f'https://api.chess.com/pub/player/{USERNAME}/games'
ARCHIVES_URL = f'{BASE_URL}/archives'


def read_json_from_url(url):
    response = urllib.request.urlopen(url)
    return json.loads(response.read().decode('utf-8'))


monthly_archives = read_json_from_url(ARCHIVES_URL)

for month_url in monthly_archives['archives']:
    data = read_json_from_url(month_url)
    print(month_url, len(data['games']))
    for game in data['games']:
        game_id = game['url'].split('/')[-1]
        file_name = f'data/{game_id}.json'
        with open(file_name, 'w') as f:
            json.dump(game, f)

import requests
from api_keys import api_football
headers = api_football


# Gets top scorers data from api-football
def top_scorers(league):
    url = f"https://api-football-v1.p.rapidapi.com/v3/players/topscorers?season=2023&league={league}"
    response = requests.get(url, headers=headers)
    player_list = []
    if response.status_code == 200:
        data = response.json()['response']
        for player in data:
            player_data = {
                'player_id': player['player']['id'],
                'name': player['player']['name'],
                'photo': player['player']['photo'],
                'club': player['statistics'][0]['team']['name'],
                'logo': player['statistics'][0]['team']['logo'],
                'goals': player['statistics'][0]['goals']['total'],
                'league_id': league
            }
            player_list.append(player_data)
        return player_list
    else:
        print("Error fetching data:", response.status_code)


# Gets top assists data from api-football
def top_assists(league):
    url = f"https://api-football-v1.p.rapidapi.com/v3/players/topassists?season=2023&league={league}"
    response = requests.get(url, headers=headers)
    player_list = []
    if response.status_code == 200:
        data = response.json()['response']
        # print(data)
        for player in data:
            player_data = {
                'player_id': player['player']['id'],
                'name': player['player']['name'],
                'photo': player['player']['photo'],
                'club': player['statistics'][0]['team']['name'],
                'logo': player['statistics'][0]['team']['logo'],
                'assists': player['statistics'][0]['goals']['assists'],
                'league_id': league
            }
            player_list.append(player_data)
        return player_list
    else:
        print("Error fetching data:", response.status_code)

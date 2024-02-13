from sys import api_version
import requests
import json
from datetime import datetime
from api_keys import football_api
today_date = datetime.now().strftime("%Y-%m-%d")
end_date = "2024-07-01"


# Get todays matches from football-data api
def get_all_matches():
    url = 'https://api.football-data.org/v4/matches'
    headers = football_api
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        matches_data = response.json()['matches']
        filtered_matches = []
        for match in matches_data:
            data = {
                "homeTeam": match["homeTeam"]["name"],
                "homeCrest": match["homeTeam"]["crest"],
                "awayTeam": match["awayTeam"]["name"],
                "awayCrest": match["awayTeam"]["crest"],
                "utcDate": match["utcDate"]
            }
            filtered_matches.append(data)
        return filtered_matches
    else:
        print("Error fetching data:", response.status_code)
        print(response.text)
        return None


# Get matches from football-data api for given league
def get_matches(league):
    url = f'https://api.football-data.org/v4/competitions/{league}/matches?status=SCHEDULED'
    headers = football_api
    params = {
        'dateFrom': today_date,
        'dateTo': end_date
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        matches_data = response.json()['matches']
        filtered_matches = []
        for match in matches_data:
            if match.get("homeTeam") and match["homeTeam"].get("name") and match.get("awayTeam") and match["awayTeam"].get("name"):
                data = {
                    "homeTeam": match["homeTeam"]["name"],
                    "homeCrest": match["homeTeam"]["crest"],
                    "awayTeam": match["awayTeam"]["name"],
                    "awayCrest": match["awayTeam"]["crest"],
                    "utcDate": match["utcDate"]
                }
                filtered_matches.append(data)
        return filtered_matches
    else:
        print("Error fetching data:", response.status_code)
        print(response.text)
        return None


# Get standings from football-data api for given league
def get_standings(league):
    url = f'https://api.football-data.org/v4/competitions/{league}/standings'
    headers = football_api
    response = requests.get(url, headers=headers)
    standings = []
    if response.status_code == 200:
        data = response.json()['standings'][0]
        standingstable = data['table']
        for team in standingstable:
            standingsdata = {
                "team": team["team"]["shortName"],
                "position": team["position"],
                "playedGames": team["playedGames"],
                "crest": team["team"]["crest"],
                # "form":team["form"],
                "won": team["won"],
                "draw": team["draw"],
                "lost": team["lost"],
                "goalsFor": team["goalsFor"],
                "goalsAgainst": team["goalsAgainst"],
                "goalDifference": team["goalDifference"],
                "points": team["points"],
            }
            standings.append(standingsdata)
        return standings
    else:
        print("Error fetching data:", response.status_code)
        print(response.text)
        return None

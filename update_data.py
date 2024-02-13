from re import T
import mysql.connector
from db_config import DB_CONFIG, DB_LOCAL_CONFIG
from get_football import top_scorers, top_assists
from get_matches import get_standings, get_matches, get_all_matches

league_indexes = {
    "CL": "Champions League",
    "PL": "Premier League",
    "BL1": "Bundesliga",
    "SA": "Serie A",
    "PD": "La Liga",
    "FL1": "Ligue 1"
}

league_ids = {
    "Champions League": 2,
    "Premier League": 39,
    "Bundesliga": 78,
    "Serie A": 135,
    "La Liga": 140,
    "Ligue 1": 61
}

indexes = [39, 78, 135, 140, 61]
codes = ["PL", "BL1", "SA", "PD", "FL1"]


# Inserts the top scorers data into MySQL database for given league
def update_top_scorers(league):
    table_name = "top_scorers"
    data = top_scorers(league)
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    # Iterate through the data and insert into the database
    for player in data:
        insert_query = f"INSERT INTO {table_name} (player_id, name, club, logo, goals,league_id) VALUES (%s, %s, %s, %s, %s, %s)"
        player_data = (player['player_id'], player['name'], player['club'],
                       player['logo'], player['goals'], player['league_id'])

        try:
            cursor.execute(insert_query, player_data)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    connection.commit()
    cursor.close()
    connection.close()


# Inserts the top assists data into MySQL database for given league
def update_top_assists(league):
    table_name = "top_assists"
    data = top_assists(league)
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    # Iterate through the data and insert into the database
    for player in data:
        insert_query = f"INSERT INTO {table_name} (player_id, name, club, logo, assists,league_id) VALUES (%s, %s, %s, %s, %s, %s)"
        player_data = (player['player_id'], player['name'],
                       player['club'], player['logo'], player['assists'], player['league_id'])

        try:
            cursor.execute(insert_query, player_data)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    connection.commit()
    cursor.close()
    connection.close()


# Inserts the top standings data into MySQL database for given league
def update_standings(league):
    table_name = "standings"
    data = get_standings(league)
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    # Iterate through the data and insert into the database
    for team in data:
        insert_query = f"INSERT INTO {table_name}(team, position, playedGames, logo, won, draw, lost, points, goalsFor, goalsAgainst, goalDifference, league_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        team_data = (team['team'], team['position'], team['playedGames'], team['crest'], team['won'],
                     team['draw'], team['lost'], team['points'], team['goalsFor'], team['goalsAgainst'], team['goalDifference'], league_ids[league_indexes[league]])
        try:
            cursor.execute(insert_query, team_data)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    connection.commit()
    cursor.close()
    connection.close()


# Inserts the upcoming matches data into MySQL database for given league
def update_matches(league):
    table_name = "matches"
    data = get_matches(league)
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    # Iterate through the data and insert into the database
    for match in data:
        insert_query = f"INSERT INTO {table_name}(homeTeam, homeCrest, awayTeam, awayCrest, utcDate, league_id) VALUES (%s, %s, %s, %s, %s, %s)"
        team_data = (match['homeTeam'], match['homeCrest'], match['awayTeam'],
                     match['awayCrest'], match['utcDate'], league_ids[league_indexes[league]])
        try:
            cursor.execute(insert_query, team_data)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    connection.commit()
    cursor.close()
    connection.close()


# Inserts the today's matches data into MySQL database
def update_all_matches():
    table_name = "today_matches"
    data = get_all_matches()
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    # Iterate through the data and insert into the database
    for match in data:
        insert_query = f"INSERT INTO {table_name}(homeTeam, homeCrest, awayTeam, awayCrest, utcDate) VALUES (%s, %s, %s, %s, %s)"
        team_data = (match['homeTeam'], match['homeCrest'], match['awayTeam'],
                     match['awayCrest'], match['utcDate'])
        try:
            cursor.execute(insert_query, team_data)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    connection.commit()
    cursor.close()
    connection.close()


# Deletes old data and calls the update functions to insert new
def update_all():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    # Delete existing data
    cursor.execute("DELETE FROM top_scorers")
    cursor.execute("DELETE FROM top_assists")
    cursor.execute("DELETE FROM standings")
    cursor.execute("DELETE FROM matches")
    cursor.execute("DELETE FROM today_matches")
    connection.commit()
    cursor.close()
    connection.close()
    for i in indexes:
        update_top_scorers(i)
        update_top_assists(i)
        pass
    for i in codes:
        update_standings(i)
        update_matches(i)
    update_all_matches()


update_all()

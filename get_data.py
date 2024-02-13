import mysql.connector
from db_config import DB_CONFIG, DB_LOCAL_CONFIG


# Returns standings data for given league id
def get_league_standings(league_id):
    connection = mysql.connector.connect(**DB_LOCAL_CONFIG)
    cursor = connection.cursor(dictionary=True)
    query = f"SELECT * FROM standings WHERE league_id = {league_id} ORDER BY position ASC"
    cursor.execute(query)
    teams = cursor.fetchall()
    cursor.close()
    connection.close()
    teams = [match for match in teams]
    return teams


# Returns matches data for given league id
def get_league_matches(league_id):
    connection = mysql.connector.connect(**DB_LOCAL_CONFIG)
    cursor = connection.cursor(dictionary=True)  # Fetch data as dictionaries
    query = f"SELECT * FROM matches WHERE league_id = {league_id}"
    cursor.execute(query)
    matches = cursor.fetchall()
    cursor.close()
    connection.close()
    return matches


# Returns today's matches data
def get_today_matches():
    connection = mysql.connector.connect(**DB_LOCAL_CONFIG)
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM today_matches"
    cursor.execute(query)
    matches = cursor.fetchall()
    cursor.close()
    connection.close()
    matches = [match for match in matches]
    return matches


# Returns top scorers data for given league id
def get_top_scorers(league_id):
    connection = mysql.connector.connect(**DB_LOCAL_CONFIG)
    cursor = connection.cursor()
    if league_id == 'general':
        query = "SELECT * FROM top_scorers ORDER BY goals DESC LIMIT 20"
    else:
        query = f"SELECT * FROM top_scorers WHERE league_id = {league_id} ORDER BY goals DESC"
    cursor.execute(query)

    top_scorers = cursor.fetchall()

    cursor.close()
    connection.close()
    return top_scorers


# Returns top assists data for given league id
def get_top_assists(league_id):
    connection = mysql.connector.connect(**DB_LOCAL_CONFIG)
    cursor = connection.cursor()
    if league_id == 'general':
        query = f"SELECT * FROM top_assists ORDER BY assists DESC LIMIT 20"
    else:
        query = f"SELECT * FROM top_assists WHERE league_id = {league_id} ORDER BY assists DESC"
    cursor.execute(query)

    top_assists = cursor.fetchall()

    cursor.close()
    connection.close()
    return top_assists


# Returns top goal contributions data for given league id
def get_top_goal_contributions(league_id):
    connection = mysql.connector.connect(**DB_LOCAL_CONFIG)
    cursor = connection.cursor()

    if league_id == 'general':
        # Query to get top goal contributions for general league
        query = """
            SELECT name, club, logo, SUM(goals) + SUM(assists) AS goal_contributions
            FROM (
                SELECT name, club, logo, goals, 0 AS assists FROM top_scorers
                UNION ALL
                SELECT name, club, logo, 0 AS goals, assists FROM top_assists
            ) AS combined_stats
            GROUP BY name, club, logo
            ORDER BY goal_contributions DESC
            LIMIT 20
        """
    else:
        # Query to get top goal contributions for specific league
        query = f"""
            SELECT name, club, logo, SUM(goals) + SUM(assists) AS goal_contributions
            FROM (
                SELECT name, club, logo, goals, 0 AS assists FROM top_scorers WHERE league_id = {league_id}
                UNION ALL
                SELECT name, club, logo, 0 AS goals, assists FROM top_assists WHERE league_id = {league_id}
            ) AS combined_stats
            GROUP BY name, club, logo
            ORDER BY goal_contributions DESC
            LIMIT 20
        """

    cursor.execute(query)
    top_contributions = cursor.fetchall()

    cursor.close()
    connection.close()
    top_contributions = [(name, club, logo, int(goal_contributions))
                         for name, club, logo, goal_contributions in top_contributions]
    return top_contributions

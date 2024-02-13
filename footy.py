from this import d
from flask import Flask, render_template
from datetime import datetime
from get_data import get_top_scorers, get_top_assists, get_top_goal_contributions, get_league_matches, get_league_standings, get_today_matches
import pytz

app = Flask(__name__)

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


# Returns date and time in EST
def format_utc_date(utc_date):
    date_object = datetime.strptime(utc_date, "%Y-%m-%dT%H:%M:%SZ")

    utc_timezone = pytz.timezone('UTC')
    date_object = utc_timezone.localize(date_object)

    est_timezone = pytz.timezone('US/Eastern')
    est_date_time = date_object.astimezone(est_timezone)

    formatted_date_time = est_date_time.strftime("%Y-%m-%d %H:%M")

    return formatted_date_time


@app.route("/")
def home():
    goals = get_top_scorers('general')
    assists = get_top_assists('general')
    conts = get_top_goal_contributions('general')
    return render_template("index.html", goals=goals, assists=assists, conts=conts)


@app.route("/stats/<string:league>")
def stats(league):
    if league == 'general':
        scorers_data = get_top_scorers(league)
        assists_data = get_top_assists(league)
        goal_contributions_data = get_top_goal_contributions(league)
        league_name = "Top 5 European Leagues"
    else:
        league_name = league_indexes[league]
        league_id = league_ids[league_name]
        scorers_data = get_top_scorers(league_id)
        assists_data = get_top_assists(league_id)
        goal_contributions_data = get_top_goal_contributions(league_id)
    return render_template("stats.html", leagueCode=league, leagueName=league_name, goals=scorers_data, assists=assists_data, contributions=goal_contributions_data)


@app.route("/matches/general")
def todays_matches():
    matches_data = get_today_matches()
    if matches_data is not None:
        simplified_matches_data = [
            {
                "homeTeam": match["homeTeam"],
                "homeCrest": match["homeCrest"],
                "awayTeam": match["awayTeam"],
                "awayCrest": match["awayCrest"],
                "formattedDate": format_utc_date(match["utcDate"]).split()[0],
                "formattedTime": format_utc_date(match["utcDate"]).split()[1]
            }
            for match in matches_data
        ]
    if simplified_matches_data == []:
        return render_template("index.html", message="No Matches Today!")
    return render_template("todayMatches.html", leagueName="Today's Matches", matches_data=simplified_matches_data)


@ app.route("/matches/<string:league>")
def matches(league):
    matches_data = get_league_matches(league_ids[league_indexes[league]])
    league_table = get_league_standings(league_ids[league_indexes[league]])

    # Check if matches_data is not None before processing
    if matches_data is not None:
        simplified_matches_data = [
            {
                "homeTeam": match["homeTeam"],
                "homeCrest": match["homeCrest"],
                "awayTeam": match["awayTeam"],
                "awayCrest": match["awayCrest"],
                "formattedDate": format_utc_date(match["utcDate"]).split()[0],
                "formattedTime": format_utc_date(match["utcDate"]).split()[1]
            }
            for match in matches_data
        ]
    if simplified_matches_data == []:
        # Handle the case where fetching data failed
        simplified_matches_data = []
        return render_template("index.html", message="No Upcoming Matches Scheduled!")

    return render_template("matches.html", leagueCode=league, leagueName=league_indexes[league], matches_data=simplified_matches_data, table_data=league_table)


if __name__ == "__main__":
    app.run(debug=True)

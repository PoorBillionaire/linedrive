import sys
import requests
from linedrive import constants


def check_schedule(league, team=None):
    """
    Query ESPN's scoreboard for the given league. Return a list of JSON objects,
    each containing information related to an upcoming game/matchup.

    If a team name is provided, and that team is scheduled to play, the list
    returned will contain only one JSON object.
    """

    scheduled_games = []

    r = requests.get(
        constants.SCOREBOARD["url"] + constants.SCOREBOARD[league],
        headers=constants.HTTP_HEADERS
    )

    for game in r.json()["events"]:
        if team:
            opponents = game["name"].lower().split(" at ")
            for team_name in opponents:
                if " " + team.lower() in team_name:
                    scheduled_games.append(game)
                    return scheduled_games
        else:
            scheduled_games.append(game)
    return scheduled_games


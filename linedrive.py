import json
import zlib
import base64
import requests
import websocket
from argparse import ArgumentParser


"""
He would tinker around the lab and rearrange the tools,
often alone and somewhat bored,
almost excavating the empty air for ideas in pursuit of something exciting.

Black Hole Blues
"""


logo = (
    f"    __    _____   ____________  ____  _____    ________\n"
    f"   / /   /  _/ | / / ____/ __ \/ __ \/  _/ |  / / ____/\n"
    f"  / /    / //  |/ / __/ / / / / /_/ // / | | / / __/   \n"
    f" / /____/ // /|  / /___/ /_/ / _, _// /  | |/ / /___   \n"
    f"/_____/___/_/ |_/_____/_____/_/ |_/___/  |___/_____/   \n")


def build_websocket_url():
    """Construct the Gamecast websocket URL, return it as a string."""

    ws_host="https://fastcast.semfs.engsvc.go.com/public/websockethost"
    ws_uri="FastcastService/pubsub/profiles/12000?TrafficManager-Token="
    r = requests.get(ws_host, headers={"User-Agent": "Mozilla/5.0"})
    ws_info = r.json()
    ws_info["securePort"] = str(ws_info["securePort"])
    ws_uri = ws_uri + ws_info["token"]
    ws_url = f"wss://{ws_info['ip']}:{ws_info['securePort']}/{ws_uri}"
    return ws_url


def websocket_handshake(ws, message=None):
    """Subscribe to the relevant gamecast websocket channel."""

    if not message:
        ws.send(json.dumps({"op": "C"}))
    else:
        if message.get("op") == "C" and message.get("sid"):
            msg = {"op": "S", "sid": message["sid"], "tc": event_channel}
            ws.send(json.dumps(msg))


def websocket_on_message(ws, message):
    """
    Read, filter, and decode each message received from the websocket.
    Gameplay-related events are printed to stdout via calls to the 
    write_message() function.
    """

    message = json.loads(message)

    # If needed, complete the websocket handshake
    if message["op"] == "C":
        websocket_handshake(ws, message=message)
    
    # The next two lines ensure only gameplay related event for the spcecified
    # game are provided. Otherwise, ESPN's websockets include noisy league-wide
    # information.
    elif "pl" in message:
        if message["pl"] != "0" and message["tc"] == event_channel:
            decoded = decode_message(message)
            write_message(ws, decoded)


def decode_message(message):
    """
    Base64 decode and zlib decompress each gameplay message, return its value.
    """

    message["pl"] = json.loads(message["pl"])
    if message["pl"]["~c"] != "0":
        decoded = base64.b64decode(message["pl"]["pl"])
        decoded = zlib.decompress(decoded)
        message["pl"]["pl"] = json.loads(decoded)
        return message


def write_message(ws, message):
    """
    Filter for relevant gameplay events and print them to stdout.
    If the end of a game is detected, close the websocket connection.
    """

    for event in message["pl"]["pl"]:
        if event["op"] == "add" and "value" in event:
            if type(event["value"]) != int and "text" in event["value"]:
                print("{}: {:<3} | {}: {:<3} | Period {} {:<5} | {}".format(
                    homeTeam,
                    event["value"]["homeScore"],
                    awayTeam,
                    event["value"]["awayScore"],
                    event["value"]["period"]["number"],
                    event["value"]["clock"]["displayValue"],
                    event["value"]["text"]))
                if event["value"]["text"].lower() == "end of game":
                    ws.close()


def check_schedule(league, team=None):
    """
    Query ESPN's scoreboard for the given league. Return a list of JSON objects,
    each containing information related to an upcoming game/matchup.

    If a team name is provided, and that team is scheduled to play, the list
    returned will contain only one JSON object.
    """

    scheduled_games = []
    scoreboard = {
        "url": "https://site.api.espn.com/apis/site/v2/sports",
        "ncaaw": "/basketball/womens-college-basketball/scoreboard",
        "ncaam": "/basketball/mens-college-basketball/scoreboard",
        "wnba": "/basketball/wnba/scoreboard",
        "nba": "/basketball/nba/scoreboard",
        "nfl": "/football/nfl/scoreboard",
        "nhl": "/hockey/nhl/scoreboard"
    }

    r = requests.get(
        scoreboard["url"] + scoreboard[league],
        headers={"User-Agent": "Mozilla/5.0"}
    )

    for game in r.json()["events"]:
        if team:
            opponents = game["name"].lower().split(" at ")
            for team_name in opponents:
                if team.lower() in team_name:
                    scheduled_games.append(game)
                    return scheduled_games
        else:
            scheduled_games.append(game)
    return scheduled_games


def main():
    p = ArgumentParser()
    p.add_argument("mode", choices=["events", "schedule"])
    p.add_argument("-l", "--league", choices=["wnba", "nba", "ncaaw", "ncaam", "nfl", "nhl"], help="Team", required=True)
    p.add_argument("-t", "--team", help="Team name")
    args = p.parse_args()


    # Scheduling needs to be checked no matter what, and we do that first.
    schedule = check_schedule(args.league, args.team)

    if args.mode == "events":
        
        print(logo)

        global homeTeam
        global awayTeam
        global event_channel

        awayTeam = schedule[0]["name"].split(" at ")[0].split(" ")[-1]
        homeTeam = schedule[0]["name"].split(" at ")[1].split(" ")[-1]

        channels = {
            "ncaaw": "gp-basketball-womens-college-basketball-",
            "ncaam": "gp-basketball-mens-college-basketball-",
            "wnba" : "gp-basketball-wnba-",
            "nba"  : "gp-basketball-nba-",
            "nfl"  : "gp-football-nfl-",
            "nhl"  : "gp-hockey-nhl-"
        }
        event_channel = channels[args.league] + schedule[0]["id"]

        websocket_url = build_websocket_url()

        ws = websocket.WebSocketApp(
            websocket_url,
            on_open=websocket_handshake,
            on_message=websocket_on_message
        )
        ws.run_forever()


    elif args.mode == "schedule":
        for game in schedule:
            print("{} | {:<18} | {}".format(
                game["date"],
                game["status"]["type"]["name"],
                game["name"]
            ))


if __name__ == "__main__":
    main()

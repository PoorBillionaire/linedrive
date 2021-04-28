from argparse import ArgumentParser
from .core import *


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

from argparse import ArgumentParser
import linedrive


"""
He would tinker around the lab and rearrange the tools,
often alone and somewhat bored,
almost excavating the empty air for ideas in pursuit of something exciting.

Black Hole Blues
"""


def main():
    p = ArgumentParser()
    p.add_argument("mode", choices=["events", "schedule"])
    p.add_argument("-l", "--league", choices=["wnba", "nba", "ncaaw", "ncaam", "nfl", "nhl"], help="Team", required=True)
    p.add_argument("-t", "--team", help="Team name")
    args = p.parse_args()

    if args.mode == "events":

        print(linedrive.constants.logo)

        ws = linedrive.websocket.GamecastWebsocket(args.league, args.team)
        ws.run_forever()

    elif args.mode == "schedule":
        schedule = linedrive.utils.check_schedule(args.league, team=args.team)
        for game in schedule:
            print("{} | {:<18} | {}".format(
                game["date"],
                game["status"]["type"]["name"],
                game["name"]
            ))


if __name__ == "__main__":
    main()

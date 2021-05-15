logo = (
    f"    __    _____   ____________  ____  _____    ________\n"
    f"   / /   /  _/ | / / ____/ __ \/ __ \/  _/ |  / / ____/\n"
    f"  / /    / //  |/ / __/ / / / / /_/ // / | | / / __/   \n"
    f" / /____/ // /|  / /___/ /_/ / _, _// /  | |/ / /___   \n"
    f"/_____/___/_/ |_/_____/_____/_/ |_/___/  |___/_____/   \n")

WS_HOST="https://fastcast.semfs.engsvc.go.com/public/websockethost"

WS_URI="FastcastService/pubsub/profiles/12000?TrafficManager-Token="

HTTP_HEADERS={"User-Agent": "Mozilla/5.0"}

SCOREBOARD = {
    "url": "https://site.api.espn.com/apis/site/v2/sports",
    "ncaaw": "/basketball/womens-college-basketball/scoreboard",
    "ncaam": "/basketball/mens-college-basketball/scoreboard",
    "wnba": "/basketball/wnba/scoreboard",
    "nba": "/basketball/nba/scoreboard",
    "nfl": "/football/nfl/scoreboard",
    "nhl": "/hockey/nhl/scoreboard"
}

CHANNELS = {
    "ncaaw": "gp-basketball-womens-college-basketball-",
    "ncaam": "gp-basketball-mens-college-basketball-",
    "wnba" : "gp-basketball-wnba-",
    "nba"  : "gp-basketball-nba-",
    "nfl"  : "gp-football-nfl-",
    "nhl"  : "gp-hockey-nhl-"
}

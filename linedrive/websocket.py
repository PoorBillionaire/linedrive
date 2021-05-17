import re
import json
import zlib
import base64
import requests

import websocket

from linedrive import constants, utils


"""
I used to think time was a thief.
But you give before you take.
Time is a gift. Every minute. Every second.

Alice Through the Looking Glass
"""


class GamecastWebsocket(websocket.WebSocketApp):
    def __init__(self, league, team):
        self.orient(league, team)
        self.websocket_url = self.build_websocket_url()
        super().__init__(
            self.websocket_url,
            on_open=self.on_open,
            on_message=self.on_message
        )

    def build_websocket_url(self):
        """Construct the Gamecast websocket URL, return it as a string."""

        r = requests.get(constants.WS_HOST, headers=constants.HTTP_HEADERS)
        ws_info = r.json()
        ws_info["securePort"] = str(ws_info["securePort"])
        ws_uri = constants.WS_URI + ws_info["token"]
        ws_url = f"wss://{ws_info['ip']}:{ws_info['securePort']}/{ws_uri}"
        return ws_url

    def on_open(self, wsobj, message=None):
        """Subscribe to the relevant gamecast websocket channel."""
        if not message:
            wsobj.send(json.dumps({"op": "C"}))
        else:
            if message.get("op") == "C" and message.get("sid"):
                msg = {"op": "S", "sid": message["sid"], "tc": self.channel}
                wsobj.send(json.dumps(msg))

    def on_message(self, wsobj, message):
        """
        Read, filter, and decode each message received from the websocket.
        Gameplay-related events are printed to stdout via calls to the
        write_message() function.
        """

        message = json.loads(message)

        # If needed, complete the websocket handshake
        if message["op"] == "C":
            self.on_open(wsobj, message=message)

        # The next few lines ensure only gameplay related event for the
        # specified game are provided. Otherwise, ESPN's websockets include
        # noisy league-wide information.
        elif "pl" in message:
            if message["pl"] != "0" and message["tc"] == self.channel:
                decoded = self.decode_message(message)
                self.write_message(wsobj, decoded)


    def decode_message(self, message):
        """
        Base64 decode and zlib decompress each gameplay message, return its value.
        """

        message["pl"] = json.loads(message["pl"])
        if message["pl"]["~c"] != "0":
            decoded = base64.b64decode(message["pl"]["pl"])
            decoded = zlib.decompress(decoded)
            message["pl"]["pl"] = json.loads(decoded)
            return message


    def write_message(self, wsobj, message):
        """
        Filter for relevant gameplay events and print them to stdout.
        If the end of a game is detected, close the websocket connection.
        """
        for event in message["pl"]["pl"]:
            if event["op"] == "add" and "value" in event:
                if type(event["value"]) != int and "text" in event["value"]:
                    print("{}: {:<3} | {}: {:<3} | Period {} {:<5} | {}".format(
                        self.homeTeam,
                        event["value"]["homeScore"],
                        self.awayTeam,
                        event["value"]["awayScore"],
                        event["value"]["period"]["number"],
                        event["value"]["clock"]["displayValue"],
                        event["value"]["text"]))
                    if event["value"]["text"].lower() == "end of game":
                        wsobj.close()


    def orient(self, league, team):
        game = utils.check_schedule(league, team)
        if game:
            self.channel = constants.CHANNELS[league] + game[0]["id"]
            self.homeTeam, self.awayTeam = re.findall("\w+", game[0]["shortName"])



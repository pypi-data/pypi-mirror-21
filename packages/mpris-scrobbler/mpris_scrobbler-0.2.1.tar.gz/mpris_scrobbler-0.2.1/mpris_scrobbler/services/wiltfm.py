import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

auth_url = "https://wilt.fm/api/api-token-auth/"
scrobble_url = "https://wilt.fm/api/scrobbles/"


class Wilt(object):

    def __init__(self, username=None, password=None, token=None):
        self.user = username
        self.password = password
        self.logged_in = False

        if not token:
            token = "Token {}".format(self.login())
        self.token = token
        self.last_played = ""

    def save_token(self, user):
        self.conf_dir = "/home/{}/.config/mpris-scrobble".format(user)

        with open(self.conf_dir + "/config", "w") as f:
            f.write(self.token)

    def login(self):
        if self.token:
            self.logged_in = True
            return self.token

        r = urlopen(auth_url,
                    data=urlencode(
                        {"username": self.user, "password": self.password}
                    ).encode("utf-8"))
        r = r.read().strip().decode()
        if "token" in r:
            self.logged_in = True
            r = json.loads(r)
            return r["token"]
        else:
            return "Something went wrong - Not logged in!"

    def verify_scrobble(self, scrob):
        stops = ["", "Spotify"]

        if scrob["artist"] not in stops and scrob["song"] not in stops:
            return scrob["song"] != self.last_played

    def scrobble(self, to_scrobble):
        if self.verify_scrobble(to_scrobble):
            r = Request(scrobble_url)
            r.add_header("Authorization", self.token)
            data = urlencode(to_scrobble).encode("utf-8")
            r = urlopen(r, data=data)
            r = r.read().strip().decode()
            self.last_played = to_scrobble["song"]
            return "Scrobbled: {} - {}".format(
                to_scrobble["artist"], to_scrobble["song"]
            )
        else:
            return None

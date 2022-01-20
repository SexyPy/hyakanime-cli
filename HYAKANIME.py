import requests
import json
from rich.prompt import Prompt
from datetime import datetime

class API:
    def __init__(self) -> None:
        self.email = ""
        self.password = ""
        self.api_key = "AIzaSyD3MTDJytu8TguIlszxjXMxDOxPcm_d9OI"
        self.session = requests.session()

        self.ENDPOINTS = {
            'LOGIN': 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}',
            'ANIME_SEARCH': 'https://backend.hyakanime.fr/search/anime_search/{0}',
            'USER_SEARCH': 'https://backend.hyakanime.fr/user/user_search/{0}',
            'CATALOGUE': 'https://backend.hyakanime.fr/get/plateforme/{0}',
            'CALENDAR': 'https://backend.hyakanime.fr/get/fetch-calendar-hebdo',
            'ANIME': 'https://backend.hyakanime.fr/get/anime/{0}',
        }

    def login(self) -> json:
        data = {"email": self.email, "password": self.password, "returnSecureToken": True}
        return self.session.post(self.ENDPOINTS['LOGIN'].format(self.api_key), data=data).json()

    def anime_search(self, search) -> json:
        return self.session.get(self.ENDPOINTS['ANIME_SEARCH'].format(search)).json()

    def user_search(self, search) -> json:
        return self.session.get(self.ENDPOINTS['USER_SEARCH'].format(search)).json()

    def get_catalogue(self, platform) -> json:
        return self.session.get(self.ENDPOINTS['CATALOGUE'].format(platform)).json()

    def get_calendar(self) -> json:
        return self.session.get(self.ENDPOINTS['CALENDAR']).json()

    def get_anime(self, id_anime) -> json:
        return self.session.get(self.ENDPOINTS['ANIME'].format(id_anime)).json()


class PARSER:
    def __init__(self) -> None:
        self.API = API()

    def parse_login(self):
        login = self.API.login()

    def parse_anime_search(self):
        ask = Prompt.ask(f"[underline]What anime are you looking for[/]")
        anime_search = self.API.anime_search(ask)

        for anime in anime_search:
            print(f"[{anime['id']}] {anime['title']}")

    def parse_user_search(self):
        ask = Prompt.ask(f"[underline]What anime are you looking for[/]")
        user_search = self.API.user_search(ask)

        counter = 0
        for user in user_search:
            print(f"[{counter}] {user['username']}")
            counter += 1

    def parse_get_catalogue(self):
        pass

    def parse_get_calendar(self):
        calendar = self.API.get_calendar()[0]["calendar"]

        for indexD, day in enumerate(calendar):
            if indexD:
                print()

            if day[0]["Timestamp"]:
                print(f"[{datetime.fromtimestamp(int(day[0]['Timestamp'])).strftime('%d/%m/%Y')}]")

            for indexR, release in enumerate(day):
                title = release["Titre"].strip()
                timestamp_convert = str(datetime.fromtimestamp(int(release["Timestamp"])).strftime("%H:%M"))

                season = ""
                if release["NumSaison"]:
                    season = str(release["NumSaison"]).zfill(2)

                episode = ""
                if release["NumEpisode"]:
                    episode = str(release["NumEpisode"]).zfill(2)

                print(f"[{indexR}] {title} - S{season}E{episode} ({timestamp_convert})")

    def parse_get_anime(self):
        pass

PARSER().parse_get_calendar()
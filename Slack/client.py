import requests
import json


class Client(object):
    session = None
    token: str = None
    headers: dict = dict()
    host: str = None

    def __init__(self, token: str):
        self.session = requests.Session()
        self.host = "https://slack.com/api/"
        self.token = token
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
            + "AppleWebKit/537.36 (KHTML, like Gecko) " \
            + "Chrome/70.0.3538.77 Safari/537.36'
        self.headers = {
            "User-Agent": ua,
            "Accepted-Content-Type": "application/x-www-form-urlencoded"
        }

    def request(
        self,
        method: str, path: str,
        query: dict = None, payload: dict = None, files = None
    ):
        method = method.lower()
        url = "{}{}".format(self.host, path)
        args = {
            "url": url,
            "headers": self.headers
        }
        if query is not None:
            query["token"] = self.token
        else:
            query = {"token": self.token }
        args["params"] = query
        if payload is not None:
            args["data"] = payload
        if files is not None:
            args["files"] = files

        response = getattr(self.session, method)(**args)
        if response.status_code in [200, 201, 204]:
            result = json.loads(response.text)
            if not result["ok"]:
                raise Exception(result["error"])
            return result
        else:
            response.raise_for_status()

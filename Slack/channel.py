from .client import Client
from .user import User
import threading


class Channel(Client):
    """
    @namespace  Slack
    @class      Channel
    @brief      Slackチャンネル操作用
    """
    path = "channels"

    def __init__(self, token: str = None, client: Client = None):
        """
        @brief          初期化
        @params[in]     token   SlackのOAuth2トークンを指定
        @params[in]     client  Clientを継承したクラスのオブジェクトを指定
        @details        tokenもしくはclientを指定して
        @n              クラスオブジェクトを初期化します
        """
        if client is not None:
            self.session = client.session
            self.host = client.host
            self.headers = client.headers
            self.token = client.token
        elif token is not None:
            super(Channel, self).__init__(token)
        self.user = User(client=self)

    def info(self, channel: str, include_locale: bool = False):
        path = "{}.info".format(self.path)
        query = {
            "channel": channel,
            "include_locale": include_locale
        }
        return self.request(method="get", path=path, query=query)

    def members(self, channel: str):
        response = self.info(channel=channel)
        users = response["channel"]["members"]
        results = []
        threadlist = list()
        for user_id in users:
            thread = threading.Thread(
                target=self.__get_profile,
                args=([user_id, results]),
            )
            threadlist.append(thread)
            thread.start()
        for thread in threadlist:
            thread.join()
        return results

    def __get_profile(self, user_id: str, results):
        response = self.user.profile(user=user_id)
        results.append(response["profile"])

    def history(
        self, channel: str,
        count: int = 100, inclusive: int = 0,
        latest: str = "", oldest: int = 0, unreads: int = 0
    ):
        query = locals()
        del query["self"]
        path = "{}.history".format(self.path)
        return self.request(method="get", path=path, query=query)

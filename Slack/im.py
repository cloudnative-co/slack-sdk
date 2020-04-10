from .client import Client
from .user import User
import threading


class DirectMessage(Client):
    """
    @namespace  Slack
    @class      DirectMessage
    @brief      Slackのダイレクトメッセージ操作用
    """
    path = "im"

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
            super(DirectMessage, self).__init__(token)

    def open(self, user: str, include_locale:bool = False, return_im: bool = False):
        path = "{}.open".format(self.path)
        data={
            "user": user,
            "include_locale": include_locale,
            "return_im": return_im
        }
        return self.request(method="post", path=path, payload=data)

    def history(
        self,
        channel: str,
        count: int = None,
        inclusive: bool = None,
        latest: str = None,
        oldest: str = None,
        unreads: bool = None
    ):
        path = "{}.history".format(self.path)
        query={
            "channel": channel,
            "count": count,
            "inclusive": inclusive,
            "latest": latest,
            "oldest": oldest,
            "unreads": unreads
        }
        return self.request(method="get", path=path, query=query)

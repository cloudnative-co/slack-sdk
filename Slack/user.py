from .client import Client


class User(Client):
    """
    @namespace  Slack
    @class      User
    @brief      Slackチャンネル操作用
    """
    path = "users"

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
            super(User, self).__init__(token)

    def info(self, user: str, include_locale: bool = False):
        path = "{}.info".format(self.path)
        query={
            "user": user,
            "include_locale": include_locale
        }
        return self.request(method="get", path=path, query=query)

    def profile(self, user: str, include_locale: bool = False):
        path = "{}.profile.get".format(self.path)
        query={
            "user": user,
            "include_locale": include_locale
        }
        return self.request(method="get", path=path, query=query)

    def list(
        self,
        cursor: str = None,
        include_locale: bool = False,
        limit: int = 0,
        presence: bool = False
    ):
        path = "{}.list".format(self.path)
        query={
            "cursor": cursor,
            "include_locale": include_locale,
            "limit": limit,
            "presence": presence
        }
        return self.request(method="get", path=path, query=query)


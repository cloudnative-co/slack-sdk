import json
from .client import Client


class Views(Client):
    """
    @namespace  Slack
    @class      Views
    @brief      Slackダイアログ操作用
    """
    path = "views"

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
            super(Views, self).__init__(token)

    def open(self, trigger_id: str, view: dict):
        path = "{}.open".format(self.path)
        query = {
            "trigger_id": trigger_id,
            "view": json.dumps(view)
        }
        response = self.request(method="post", path=path, query=query)
        return response

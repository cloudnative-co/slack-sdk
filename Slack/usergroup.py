from .client import Client
from .user import User
import threading


class UserGroup(Client):
    """
    @namespace  Slack
    @class      UserGroup
    @brief      Slackユーザーグループ操作用
    """
    path = "usergroups"

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
            super(UserGroup, self).__init__(token)
        self.user = User(client=self)


    def list(
        self,
        include_count: bool = False,
        include_disabled: bool = False,
        include_users: bool = False,
    ):
        path = "{}.list".format(self.path)
        query={
            "include_count": include_count,
            "include_disabled": include_disabled,
            "include_users": include_users
        }
        return self.request(method="get", path=path, query=query)

    def members(self, id, include_disabled: bool = False):
        path = "{}.users.list".format(self.path)
        query={
            "usergroup": id,
            "include_disabled": include_disabled
        }
        response = self.request(method="get", path=path, query=query)
        if not response["ok"]:
            raise Exception(response["error"])
        users = response["users"]
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

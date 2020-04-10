import json
from .client import Client


class Chat(Client):
    """
    @namespace  Slack
    @class      Chat
    @brief      Slack会話操作用
    """
    path = "chat"

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
            super(Chat, self).__init__(token)

    def post_message(
        self,
        channel: str,
        text: str,
        as_user: bool = None,
        attachments: dict = None,
        blocks: dict = None,
        icon_emoji: str = None,
        icon_url: str = None,
        link_names: bool = None,
        mrkdwn: bool = None,
        parse: str = None,
        reply_broadcast: bool = None,
        thread_ts: str = None,
        unfurl_links: bool = None,
        unfurl_media: bool = None,
        username: str = None
    ):
        path = "{}.postMessage".format(self.path)
        if attachments is not None:
            attachments = json.dumps(attachments)
        if blocks is not None:
            blocks = json.dumps(blocks)
        args = locals()
        query = {}
        for arg in args:
            if arg == "self":
                continue
            if args[arg] is None:
                continue
            query[arg] = args[arg]
        return self.request(method="post", path=path, payload=query)

    def update_message(
        self,
        channel: str,
        text: str,
        ts: str,
        as_user: bool = False,
        attachments: dict = None,
        blocks: dict = None,
        link_names: bool = True,
        parse: str = "full",
    ):
        path = "{}.update".format(self.path)
        if attachments is not None:
            attachments = json.dumps(attachments)
        if blocks is not None:
            blocks = json.dumps(blocks)
        query={
            "channel": channel,
            "text" : text,
            "ts": ts,
            "as_user" : as_user,
            "attachments" : attachments,
            "blocks": blocks,
            "link_names": link_names,
            "parse" : parse,
        }
        return self.request(method="post", path=path, payload=query)

    def delete(
        self,
        channel: str,
        ts: str,
        as_user: bool = False
    ):
        path = "{}.delete".format(self.path)
        query={
            "channel": channel,
            "ts": ts,
            "as_user" : as_user,
        }
        return self.request(method="post", path=path, payload=query)

    def permalink(
        self,
        channel: str,
        ts: str
    ):
        path = "{}.getPermalink".format(self.path)
        query={
            "channel": channel,
            "message_ts": ts
        }
        return self.request(method="get", path=path, query=query)


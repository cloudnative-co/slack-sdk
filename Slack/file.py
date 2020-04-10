import io
import json
import requests
import uuid
from requests_toolbelt.multipart.encoder import MultipartEncoder
from .client import Client


class File(Client):
    """
    @namespace  Slack
    @class      File
    @brief      Slackチャンネル操作用
    """
    path = "files"

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
            super(File, self).__init__(token)

    def info(self, file: str):
        path = "{}.info".format(self.path)

        query={
            "file": file
        }
        return self.request(method="get", path=path, query=query)

    def delete(self, file: str):
        path = "{}.delete".format(self.path)

        query={
            "file": file
        }
        return self.request(method="post", path=path, query=query)

    def download(self, file: str = None, file_info: dict = None):
        if file:
            file_info = self.info(file)["file"]
        url = file_info["url_private"]
        headers = self.headers
        headers["Authorization"] = "Bearer {}".format(self.token)
        args = {
            "url": url,
            "headers": headers
        }
        response = self.session.get(**args)
        result = io.BytesIO(response.content)
        return result

    def upload(
        self,
        channels: str = None,
        content: str = None,
        file: io.BytesIO = None,
        filename: str = None,
        filetype: str = None,
        initial_comment: str = None,
        thread_ts = None,
        title: str = None
    ):
        try:
            data = locals()
            del data["self"]
            files = {
                "file": data.pop("file")
            }
            path = "{}.upload".format(self.path)
            return self.request(method="post", path=path, query=data, files=files)
        except Exception as e:
            raise e

    def remote_add(self,
        external_url: str,
        title: str,
        filetype: str = None,
        preview_image = None,
        indexable_file_contents = None
    ):
        try:
            path = "{}.remote.add".format(self.path)
            external_id = str(uuid.uuid4())
            fields={
                'token': self.token,
                'external_id' : external_id,
                'external_url': external_url,
                'title': title
            }
            if preview_image is not None:
                fields["preview_image"] = preview_image
            if filetype is not None:
                fields['filetype'] = filetype
            if indexable_file_contents is not None:
                fields['indexable_file_contents'] = indexable_file_contents
            mp_encoder = MultipartEncoder(fields=fields)
            self.headers['Content-Type'] = mp_encoder.content_type
            result = self.request(method="post", path=path, payload=mp_encoder)
            return result
        except Exception as e:
            raise e

    def remote_share(self, external_id: str, channels: str):
        path = "{}.remote.share".format(self.path)
        query = {
            "token": self.token,
            "external_id": external_id,
            "channels": channels
        }
        result = self.request(method="post", path=path, query=query)
        return result

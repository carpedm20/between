# -*- coding: UTF-8 -*-

"""
between.client
~~~~~~~~~~~~~~

This module contains the client for Between.
"""

import json
import requests
import websocket
from uuid import uuid1
from datetime import datetime
from mimetypes import MimeTypes
from random import random, choice

from .utils import make_url
from .models import Person, Message, Image
from .preloads import sticker_tokens
from .exceptions import LoginError, AuthenticateError, MessageError

class Client(object):
    """A client for the Between.

    See http://github.com/carpedm20/between for complete
    documentation for the API.

    """

    def __init__(self, email, password, debug=True, user_agent=None):
        """A client for the Between

        :param email: Between account `email`
        :param password: Between account password

            import between
            client = between.Client(email, password)

        """
        self.email = email
        self.headers = {'User-Agent': 'python-between/1.0.0'}
        self.uuid = str(uuid1())
        self.me = None
        self.lover = None

        self._session = requests.Session()
        self._request_id = 0

        self.login(email, password)
        self.start()

    def start(self):
        self.get_status()
        self.set_device()
        self.get_endpoints()
        self.authenticate()

    def get(self, url, payload=None, is_json=True):
        r = self._session.get(make_url(url), params=payload, headers=self.headers)

        if is_json:
            return json.loads(r.text)
        else:
            return r.text

    def post(self, url, files=None, payload=None, is_json=True):
        r = self._session.post(make_url(url), data=payload, headers=self.headers, files=files)
        
        if is_json:
            return json.loads(r.text)
        else:
            return r.text

    def delete(self, url, files=None, payload=None, is_json=True):
        r = self._session.delete(make_url(url), data=payload, headers=self.headers, files=files)
        
        if is_json:
            return json.loads(r.text)
        else:
            return r.text

    def login(self, email, password):
        """Login to Between server

        :param email: Between account `email`
        :param password: Between account password
        """
        payload = {
            "email" : email,
            "password" : password,
            "session[type]" : "S_WINDOWS",
            "session[name]" : "carpedm20",
        }
        j = self.get("/authentication/getAccessTokenV2", payload)
        
        if j.has_key("error"):
            raise LoginError(j["error"]["message"])

        self.access_token = j["access_token"]
        self.account_id = j["account_id"]
        self.expires_at = j["expires_at"]
        self.relationship_id = j["relationship_id"]
        self.session_id = j["session_id"] # account_id + "xxx"
        self.user_id = j["user_id"]

        self.headers["x-between-authorization"] = self.access_token

    def authenticate(self):
        payload = {
            "name" : "basicAuthenticate",
            "body" : {
                "access_token" : self.access_token,
                "user_agent" : "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Between-PC/0.3.1 Safari/537.36",
                "device_uuid" : self.uuid
            }
        }
        j = self._send("/authentication", payload)
        if not j["m"]["body"]["success"]:
            raise AuthenticateError(j)

        payload = {"name" : "get"}
        j = self._send("/%s/threads" % self.user_id, payload)

        data = j["m"]["body"]["data"][0]
        self.thread_id = data["id"]
        self.chatroom = data["chatroom"]
        self.chatroom_id = data["chatroom_id"]

        payload = {
            "name" : "batch",
            "body" : {
                "requests":[
                    {
                        "objectName" : "SUBSCRIPTIONS",
                        "path" : "/subscriptions",
                        "subscriptionsReq":{
                            "methodName" : "ADD_V4",
                            "addV4Req":{
                                "subscriptions":[
                                    {
                                        "path" : "/%s" % self.thread_id,
                                        "recursive":True
                                    },
                                    {
                                        "path" : "/%s" % self.chatroom_id,
                                        "recursive":True
                                    },
                                    {
                                        "path" : "/%s/push" % self.account_id,
                                        "recursive":True,
                                        "push_priority" : "HIGH"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "objectName" : "CHAT_ROOM",
                        "path" : "/%s" % self.chatroom_id,
                        "chatRoomReq":{
                            "methodName" : "GET"
                        }
                    }
                ]
            }
        }
        j = self._send("/batch", payload)
        if not j["m"]["body"]["data"][0]["success"]:
            raise AuthenticateError(j)

    def send(self, content):
        """Send a message

        :param content: message content to send
        """
        try:
            content = content.decode('utf-8')
        except:
            pass

        payload = {
            "name" : "batch",
            "body" : {
                "requests":[
                    {
                        "objectName" : "MESSAGES",
                        "path" : "/%s/messages" % self.thread_id,
                        "messagesReq" : {
                            "methodName" : "ADD",
                            "addReq" : {
                                "message" : {
                                    "content" : content
                                }
                            }
                        }
                    },
                    {
                        "objectName" : "CHAT_MEMBER_STATE",
                        "path" : "/chatMemberState",
                        "chatMemberStateReq" : {
                            "methodName" : "EDIT",
                            "editReq" : {
                                "state_param" : {
                                    "state" : "ST_ACTIVE"
                                }
                            }
                        }
                    }
                ]
            }
        }
        j = self._send("/batch", payload)
        #if not j["m"]["body"]["data"][0]["success"]:
        #    raise MessageError(j)

    def send_sticker(self, sticker_id=None):
        """Send a sticker

        :param sticker: message content to send
        """
        if not sticker_id:
            sticker_id = choice(sticker_tokens.keys())

        try:
            token = sticker_tokens[sticker_id]
        except:
            raise MessageError("Don't have sticker token information of %s" % sticker_id)

        payload = {
            "name" : "batch",
            "body" : {
                "requests":[
                    {
                        "objectName" : "MESSAGES",
                        "path" : "/%s/messages" % self.thread_id,
                        "messagesReq" : {
                            "methodName" : "ADD",
                            "addReq" : {
                                "message" : {
                                    "attachments" : [
                                        {
                                            "attachment_type" : "T_STICKER_V2",
                                            "sticker" : {
                                                "sticker_id" : str(sticker_id),
                                                "sticker_token" : token
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    },
                    {
                        "objectName" : "CHAT_MEMBER_STATE",
                        "path" : "/chatMemberState",
                        "chatMemberStateReq" : {
                            "methodName" : "EDIT",
                            "editReq" : {
                                "state_param" : {
                                    "state" : "ST_ACTIVE"
                                }
                            }
                        }
                    }
                ]
            }
        }
        j = self._send("/batch", payload)
        #if not j["m"]["body"]["data"][0]["success"]:
        #    raise MessageError(j)

    def send_image(self, path=None, image_id=None):
        """Send an image

        :param path: path of image to upload
        """

        if not path and not image_id:
            raise MessageError("path or image_id should be passed")

        if not image_id:
            image_id = self.upload_image(path)._id

        payload = {
            "name" : "batch",
            "body" : {
                "requests":[
                    {
                        "objectName" : "MESSAGES",
                        "path" : "/%s/messages" % self.thread_id,
                        "messagesReq" : {
                            "methodName" : "ADD",
                            "addReq" : {
                                "message" : {
                                    "attachments" : [
                                        {
                                            "attachment_type" : "T_IMAGE",
                                            "reference" : image_id
                                        }
                                    ]
                                }
                            }
                        }
                    },
                    {
                        "objectName" : "CHAT_MEMBER_STATE",
                        "path" : "/chatMemberState",
                        "chatMemberStateReq" : {
                            "methodName" : "EDIT",
                            "editReq" : {
                                "state_param" : {
                                    "state" : "ST_ACTIVE"
                                }
                            }
                        }
                    }
                ]
            }
        }
        j = self._send("/batch", payload)
        #if not j["m"]["body"]["data"][0]["success"]:
        #    raise MessageError(j)

    def get_images(self, limit=64):
        """Get uploaded images

        :param limit: the maximum number of images
        """
        payload = {
            "range[limit]" : limit, 
            "file_types[]" : "FT_IMAGE",
            "file_types[]" : "FT_VOUCHER"
        }
        #j = self.get("/%s/messages/byFileType" % self.thread_id, payload)

        url = "/%s/messages/byFileType?range[limit]=%s&file_types[]=FT_IMAGE&file_types[]=FT_VOUCHER" % (self.thread_id, limit)
        j = self.get(url)

        if j["status"] == "ERROR":
            raise MessageError(j)

        print(j)

    def get_recent_messages(self, limit=32):
        """Get recent messages

        :param limit: the maximum number of messages
        """
        payload = {
            "name" : "getV4",
            "body" : {
                "range" : {
                    "limit" : limit
                },
                "glimpse" : True
            }
        }
        j = self._send("/%s/messages" % self.thread_id, payload)

        recent_messages = []
        for message in j["m"]["body"]["data"]:
            recent_messages.append(Message(message))

        return recent_messages

    def mark_read_message(self, message_id):
        """Mark a message as be read

        :param message_id: message_id to mark to be read
        """
        payload = {
            "name" : "readMessages",
            "body" : {
                "message_id" : message_id
            }
        }
        return self._send("/%s/messages" % self.thread_id, payload)

    def _send(self, path, message, c=1, v=1):
        """Send websocket message

        :param path: command to execute
        :param message: message to send
        :param c: (optional) ?
        :param v: (optional) ?
        """
        
        message["type"] = "CALL"

        payload = {
            "c" : c,
            "v" : v,
            "#" : self._request_id,
            "p" : path,
            "m" : message
        }
        msg = str(payload).replace("u'","'").replace("'",'"').replace("True","true")

        try:
            self._websocket.send(msg)
        except:
            self.start()
            self._websocket.send(msg)

        self._request_id += 1

        result = self._websocket.recv()
        return json.loads(result)

    def upload_image(self, path):
        """Upload an image to Between server

        :param path: path of file to upload
        """
        mime_type = MimeTypes().guess_type(path)[0]
        files = {
            'file_body': open(path)
        }
        j = self.post("/%s/files/uploadPhoto" % self.user_id, files=files)
        image = Image(j['image'], _id=j['id'])

        return image

    def get_status(self):
        j = self.get("/%s/views/status" % self.relationship_id)

        for user in j['users']:
            if user['email'] == self.email:
                self.me = Person(user)
            else:
                self.lover = Person(user)

        return j

    def get_endpoints(self):
        j = self.get("/info/endpoints")

        self.message_endpoints = j['message']

        self._websocket_url = "%s&access_token=%s" % (j['websocket'][0], self.access_token)
        self._websocket = websocket.create_connection(self._websocket_url)

        return j

    def run_forever(self, on_message, on_error=None, on_close=None):
        """Long polling method

        :param on_message: method that will executed when message is arrived.
        """
        self._websocket_app = websocket.WebSocketApp(self._websocket_url,
                                                    on_message = on_message,
                                                    on_error = on_error,
                                                    on_close = on_close)
        self.run_forever_mode = True
        self._websocket_app.run_forever()

    def set_device(self, os_type="D_WINDOWS"):
        payload = {
            "type" : os_type
        }
        j = self.get("/%s/device" % self.session_id, payload)

        return j

    def delete_session(self):
        j = self.delete('/%s/' % self.session_id)

        return j

    def __del__(self):
        j = self.get_status()
        j = self.delete_session()

        return j['value']

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
from random import random, choice
from datetime import datetime
from bs4 import BeautifulSoup as bs

from .utils import make_url
from .models import Person
from .exceptions import LoginError

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
        self.headers = {}
        self.uuid = str(uuid1())
        self.me = None
        self.lover = None

        self._session = requests.Session()
        self._request_id = 0

        self.login(email, password)
        self.get_status()
        self.set_device()
        self.get_endpoints()
        self.authentication()

    def get(self, url, payload=None, is_json=True):
        r = self._session.get(make_url(url), params=payload, headers=self.headers)
        if is_json:
            return json.loads(r.text)
        else:
            return r.text

    def post(self, url, payload=None, is_json=True):
        r = self._session.post(make_url(url), data=payload, headers=self.headers)
        if is_json:
            json.loads(r.text)
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

    def authentication(self):
        payload = {
            "name" : "basicAuthenticate",
            "body" : {
                "access_token" : self.access_token,
                "user_agent" : "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Between-PC/0.3.1 Safari/537.36",
                "device_uuid" : self.uuid
            }
        }
        print self.send("/authentication", payload)

        payload = {"name" : "get"}
        print self.send("/%s/threads" % self.user_id, payload)

        payload = {"name" : "batch"}
        print self.send("/batch", payload)


    def send(self, path, message, c=1, v=1):
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
        self._websocket.send(str(payload))
        self._request_id += 1

        #return self._websocket.recv()

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

    def set_device(self, os_type="D_WINDOWS"):
        payload = {
            "type" : os_type
        }
        j = self.get("/%s/device" % self.session_id, payload)

        return j

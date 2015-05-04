# -*- coding: UTF-8 -*-

"""
    between
    ~~~~~~~

    Between of VCNC for Python

    :copyright: (c) 2015 by Taehoon Kim.
    :license: BSD, see LICENSE for more details.
"""

import requests
from uuid import uuid1
from random import random, choice
from datetime import datetime
from bs4 import BeautifulSoup as bs

from .utils import *
from .models import *

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
        pass

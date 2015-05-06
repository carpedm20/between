# -*- coding: UTF-8 -*-

"""
between.bot
~~~~~~~~~~~

This module contains the bot for Between.

run_forever, _get_close_args, _callback methods was referenced from
https://github.com/liris/websocket-client/blob/master/websocket/_app.py
"""

import json
import select
import websocket

from .models import Message
from .client import Client
from .exceptions import LoginError, AuthenticateError, MessageError

from websocket._abnf import ABNF

class Bot(Client):
    """A Bot for the Between.

    See http://github.com/carpedm20/between for complete
    documentation for the API.

    """
    def __init__(self, email, password, on_open=None, on_message=None, 
                on_error=None, on_close=None, on_ping=None, on_pong=None,
                on_cont_message=None, keep_running=True, debug=True, user_agent=None):
        """A bot for the Between

        :param email: Between account `email`
        :param password: Between account password

            import between
            bot = between.bot(email, password)

        """
        self.on_open = on_open
        self.on_message = on_message
        self.on_error = on_error
        self.on_close = on_close
        self.on_ping = on_ping
        self.on_pong = on_pong
        self.keep_running = keep_running
        self.last_ping_tm = 0

        super(Bot, self).__init__(email, password, debug, user_agent)

    def run_forever(self, ping_timeout=None):
        """Long polling method

        :param on_message: method that will executed when message is arrived.
        """
        if not ping_timeout or ping_timeout <= 0:
            ping_timeout = None

        close_frame = None
        
        try:
            self._callback(self.on_open)

            while self._websocket.connected:
                r, w, e = select.select((self._websocket.sock, ), (), (), ping_timeout)
                if not self.keep_running:
                    break
                if ping_timeout and self.last_ping_tm and time.time() - self.last_ping_tm > ping_timeout:
                    self.last_ping_tm = 0
                    raise WebSocketTimeoutException("ping timed out")

                if r:
                    op_code, frame = self._websocket.recv_data_frame(True)
                    if op_code == ABNF.OPCODE_CLOSE:
                        close_frame = frame
                        break
                    elif op_code == ABNF.OPCODE_PING:
                        self._callback(self.on_ping, frame.data)
                    elif op_code == ABNF.OPCODE_PONG:
                        self._callback(self.on_pong, frame.data)
                    elif op_code == ABNF.OPCODE_CONT and self.on_cont_message:
                        self._callback(self.on_cont_message, frame.data, frame.fin)
                    else:
                        data = json.loads(frame.data)
                        self._callback(self.on_message, data)

        except Exception as e:
            self._callback(self.on_error, e)
        finally:
            self._websocket.close()
            self._callback(self.on_close,
                *self._get_close_args(close_frame.data if close_frame else None))
            self._websocket = None

    def _get_close_args(self, data):
        import inspect
        if not self.on_close or len(inspect.getargspec(self.on_close).args) != 3:
            return []

        if data and len(data) >= 2:
            code = 256*six.byte2int(data[0:1]) + six.byte2int(data[1:2])
            reason = data[2:].decode('utf-8')
            return [code, reason]

        return [None, None]

    def _callback(self, callback, *args):
        if callback:
            try:
                callback(self, *args)
            except Exception as e:
                error(e)
                if isEnabledForDebug():
                    _, _, tb = sys.exc_info()
                    traceback.print_tb(tb)

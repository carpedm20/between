# -*- coding: utf-8 -*-

"""
requests.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Between's exceptions.
"""

class LoginError(IOError):
    """An Login error occurred."""

class AuthenticateError(IOError):
    """An Login error occurred."""

class MessageError(IOError):
    """An error occurred from message communication."""

class BotError(IOError):
    """An error occurred by bot execution."""

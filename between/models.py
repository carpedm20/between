# -*- coding: utf-8 -*-

"""
between.models
~~~~~~~~~~~~~~

This module contains the primary objects.
"""


class Person(object):
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

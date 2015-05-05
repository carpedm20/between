# -*- coding: utf-8 -*-

"""
between.models
~~~~~~~~~~~~~~

This module contains the primary objects.
"""
from datetime import datetime

class Base(object):
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                if key == "from":
                    setattr(self, "_from", dictionary["from"])
                else:
                    setattr(self, key, dictionary[key])
        for key in kwargs:
            if key == "from":
                setattr(self, "_from", kwargs["from"])
            else:
                setattr(self, key, kwargs[key])

class Person(Base):
    def __repr__(self):
        return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        return u'<Person %s (%s)>' % (self.nickname, self.email)

class Image(Base):
    def __repr__(self):
        return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        return u'<Image %s (%s)>' % (self.source, self._id)

class Message(Base):
    def __repr__(self):
        return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        if hasattr(self, 'content'):
            return u'<Message "%s" from %s (%s)>' % (self.content, self._from, self.datetime)
        else:
            return u'<Message %s from %s (%s)>' % (self.attachments[0]['attachment_type'], self._from, self.datetime)

    @property
    def datetime(self):
        return datetime.fromtimestamp(self.created_time/1000).strftime('%Y-%m-%d %H:%M:%S')

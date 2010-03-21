#!/usr/bin/python

class RepositoryType:
    @property
    def Binary():
        return 0

    @property
    def Source():
        return 1

class Repository:

    _base_url = ""
    _type = RepositoryType.Binary 

    def __init__(self, from_config=""):
        pass

    def base_url(self):
        return self._base_url

    def type(self):
        return self._type

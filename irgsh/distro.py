#!/usr/bin/python

from repository import Repository

class Distro(object):

    _upstream = "";
    _name = "";
    _repository = Repository()

    def __init__(self, name, from_config = ""):
        self._name = name

    def upstream(self):
        return self._upstream

    @property
    def name(self):
        return self._name

    def repository(self):
        return self._repository

    def arch(self):
        return self._arch

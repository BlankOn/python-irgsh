#! /usr/bin/python

class BinaryPackage:
    def __init__(self, name, version = None, arch = None, depends = [], conflicts = [])
        self._name = name
        self._version = version
        self._arch = arch
        self._depends = depends
        self._conflicts = conflicts

    def __str__(self):
        return self._name + "_" + self.version

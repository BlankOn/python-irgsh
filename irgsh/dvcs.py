#!/usr/bin/python

from log import Log

class DvcsIface(object):
    _name = ""
    _url = ""
    _tag = None
    _revision = None
    _branch = ""
    _log = None

    def __init__(self, url = ""):
        self._url = url
        self._log = Log()

    @property
    def url(self):
        return self._url

    @property
    def branch(self):
        return self._branch

    @branch.setter
    def branch(self, branch):
        self._branch = branch

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, tag):
        self._tag = tag

    @property
    def revision(self):
        return self._revision

    @revision.setter
    def revision(self, revision):
        self._revision = revision

    @property
    def name(self):
        return self._name

    def export(self, destination):
        # Destination must be either an empty directory or non-existant directory
        return False

class DvcsLoader:
    _instance = None

    @property
    def instance(self):
        return self._instance

    def __init__(self, name, url):
        obj = __import__("irgsh.dvcs_%s" % name, None, None, ["dvcs_%s" % name])
        dvcs = eval("obj.dvcs_%s" % name)

        self._instance = dvcs(url)    

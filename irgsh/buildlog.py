#! /usr/bin/python

from commonlog import LogDevice, LogDeviceGzip
import sys

class BuildLog:
    class __impl:
        _handle = None
        _stderr = None
        _stdout = None
        _filename = None
       
        @property
        def filename(self):
            return self._filename

        def __init__(self, filename = None):
            self.reopen(filename)

        def reopen(self, filename = None):
            if filename is not None:
                self._filename = filename
                if self._handle is not None:
                    self.close()

                if filename.endswith(".gz"):
                    self._handle = LogDeviceGzip(filename, "w")
                else:
                    self._handle = LogDevice(filename, "w")
                self._stdout = sys.stdout
                self._stderr = sys.stderr
                sys.stdout = self._handle
                sys.stderr = self._handle

        def close(self):
            if self._handle is not None:
                self._handle.close()
                sys.stdout = self._stdout
                sys.stderr = self._stderr
                self._stdout = None
                self._stderr = None 
                self._handle = None

        def handle(self):
            if self._handle is None:
                return sys.stdout
            else:
                return self._handle

        def closed(self):
            return self._handle == None

    __instance = None
    def __init__(self, filename = None):
        if BuildLog.__instance is None:
            BuildLog.__instance = BuildLog.__impl(filename)

        if BuildLog.__instance.closed():
            BuildLog.__instance.reopen(filename)

        self.__dict__['_BuildLog__instance'] = BuildLog.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr):
        return setattr(self.__instance, attr)


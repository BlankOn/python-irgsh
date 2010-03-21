#! /usr/bin/python

from commonlog import LogDevice
import sys

class BuildLog:
    class __impl:
        _handle = None
        _stderr = None
        _stdout = None

        def __init__(self, filename = None):

            if filename != None:
                if self._handle != None:
                    self.close()

                self._handle = LogDevice(filename, "w")
                self._stdout = sys.stdout
                self._stderr = sys.stderr
                sys.stdout = self._handle
                sys.stderr = self._handle

        def close(self):
            if self._handle != None:
                self._handle.close()
                sys.stdout = self._stdout
                sys.stderr = self._stderr
                self._stdout = None
                self._stderr = None 

        def handle(self):
            if self._handle == None:
                return sys.stdout
            else:
                return self._handle

    __instance = None
   
    def __init__(self, filename = None):
        if BuildLog.__instance == None:
            BuildLog.__instance = BuildLog.__impl(filename)

        self.__dict__['_BuildLog__instance'] = BuildLog.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr):
        return setattr(self.__instance, attr)


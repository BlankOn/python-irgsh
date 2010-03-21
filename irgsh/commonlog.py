#! /usr/bin/python

import sys

class LogDevice(object):
    def __init__(self, *args):
        self.device = file(*args)

    def __getattr__(self, name):
        return getattr(self.device, name)

    def write(self, s):
        self.device.write(s)
        sys.__stdout__.write(s)

class CommonLog:
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
        if CommonLog.__instance == None:
            CommonLog.__instance = CommonLog.__impl(filename)

        self.__dict__['_CommonLog__instance'] = CommonLog.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr):
        return setattr(self.__instance, attr)


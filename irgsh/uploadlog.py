#! /usr/bin/python

import sys

from commonlog import LogDevice 

class UploadLog:
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

        def write(self, msg):
            self.handle().write(msg + "\n")

    __instance = None
 
    __instance = None
   
    def __init__(self, filename = None):
        if UploadLog.__instance == None:
            UploadLog.__instance = UploadLog.__impl(filename)

        self.__dict__['_UploadLog__instance'] = UploadLog.__instance

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr):
        return setattr(self.__instance, attr)


#! /usr/bin/python

class UploadGeneralError(Exception):
    _msg = None

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        print self._msg

class UploadUploaderConfigurationError(UploadGeneralError): 
    def __init__(self, msg):
        self._msg = msg



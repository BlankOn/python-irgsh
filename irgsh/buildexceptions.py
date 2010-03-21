#! /usr/bin/python

class BuildGeneralError(Exception):
    _msg = None

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg

class BuildDownloadError(BuildGeneralError):
    def __init__(self, msg):
        self._msg = msg

class BuildSourcePreparationError(BuildGeneralError):
    def __init__(self, msg):
        self._msg = msg

class BuildBuilderGeneralError(BuildGeneralError):
    def __init__(self, msg):
        self._msg = msg

class BuildBuilderConfigurationError(BuildGeneralError): 
    def __init__(self, msg):
        self._msg = msg

class BuildBuilderFailureError(BuildGeneralError):
    def __init__(self, msg):
        self._msg = msg


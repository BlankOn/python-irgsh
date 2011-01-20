class IrgshException(StandardError):
    pass

class BuildFailedError(IrgshException):
    def __init__(self, source):
        self.source = source
    def __str__(self):
        return 'Build failed: %s' % self.source

class UploadFailedError(IrgshException):
    def __init__(self, changes, code, log=None):
        self.changes = changes
        self.code = code
        self.log = log
    def __str__(self):
        return 'Build failed: %s (%s)' % (self.changes, self.code)


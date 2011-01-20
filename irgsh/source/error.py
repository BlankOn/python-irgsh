from irgsh.error import IrgshException

class SourcePackageBuilderException(IrgshException):
    pass

class SourcePackagePreparationError(SourcePackageBuilderException):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        import urllib2
        if isinstance(self.msg, urllib2.HTTPError):
            msg = 'Download error (code: %s): %s' % \
                  (self.msg.code, self.msg.geturl())
        else:
            msg = str(self.msg)

        return 'Error preparing source package: %s' % msg

class SourcePackageBuildError(SourcePackageBuilderException):
    def __init__(self, code, msg, args):
        self.code = code
        self.msg = msg

    def __str__(self):
        return 'Error building source package (code: %s)' % \
               self.code


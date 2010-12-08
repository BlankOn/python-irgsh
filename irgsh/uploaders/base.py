from subprocess import PIPE

class UploadFailedError(Exception):
    pass

class BaseUploader(object):
    def __init__(self, distribution, **opts):
        self.distribution = distribution

    def upload(self, changes, stdout=PIPE, stderr=PIPE):
        raise NotImplementedError()


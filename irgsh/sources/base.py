import logging

class InvalidSourceLocationError(Exception):
    def __init__(self, location, msg=None):
        self.location = location
        self.msg = msg

        desc = 'Invalid source location: %s' % self.location
        if msg is not None:
            desc = '%s (%s)' % (desc, msg)
        super(InvalidSourceLocationError, self).__init__(desc)

class BaseSource(object):
    """Package source definition.

    A package source can be a directory, tarball, or even a pointer to a
    version control system.
    """

    def __init__(self, location, **opts):
        self.location = location

        self.log = logging.getLogger('irgsh.sources')

    def export(self, target):
        raise NotImplementedError()


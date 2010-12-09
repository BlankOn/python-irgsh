import logging

from ..error import InvalidSourceLocationError, InvalidSourceNameError

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

sources = {}

def register_source_class(name, cls):
    sources[name] = cls

def get_source_class(name):
    return sources.get(name, None)

def build_source(name, location, **opts):
    cls = get_source_class(name)
    if cls is None:
        raise InvalidSourceNameError(name)

    return cls(location, **opts)


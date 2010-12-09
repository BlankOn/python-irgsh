class Specification(object):
    def __init__(self, location, orig=None,
                 source_type='tarball', source_opts={}):
        self.location = location
        self.orig = orig
        self.source_type = source_type
        self.source_opts = source_opts

        self._source = None

    def get_source(self):
        if self._source is None:
            from .sources.base import build_source
            self._source = build_source(self.source_type,
                                        self.location,
                                        **self.source_opts)
        return self._source


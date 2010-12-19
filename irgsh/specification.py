class Specification(object):
    def __init__(self, location, orig=None,
                 source_type='tarball', source_opts=None):
        self.location = location
        self.source_type = source_type

        self.orig = None
        if type(orig) in [str, unicode]:
            orig = orig.strip()
            if len(orig) > 0:
                self.orig = orig

        self.source_opts = {}
        if source_opts is not None:
            self.source_opts = source_opts

        self._source = None

    def get_source(self):
        if self._source is None:
            from .sources.base import build_source
            self._source = build_source(self.source_type,
                                        self.location,
                                        **self.source_opts)
        return self._source


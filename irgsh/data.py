class Distribution(object):
    def __init__(self, name, mirror, dist, components=None, extra=None):
        self.name = name
        self.mirror = mirror
        self.dist = dist

        self.components = ['main']
        if components is not None:
            self.components = components
        if type(self.components) in [str, unicode]:
            self.components = self.components.split()

        self.extra = []
        if extra is not None:
            self.extra = extra
        if type(self.extra) in [str, unicode]:
            self.extra = self.extra.splitlines()

class Specification(object):
    def __init__(self, source, source_type='tarball', source_opts=None,
                 orig=None, extra_orig=None):
        self.source = source
        self.source_type = source_type
        self.orig = orig

        self.source_opts = {}
        if source_opts is not None:
            self.source_opts = source_opts

        if orig is None or extra_orig is None:
            extra_orig = []
        self.extra_orig = extra_orig


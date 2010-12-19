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


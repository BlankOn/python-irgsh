class Distribution(object):
    def __init__(self, name, mirror, dists, components=['main'], extra=[]):
        self.name = name
        self.mirror = mirror
        self.dists = dists
        self.components = components
        self.extra = extra


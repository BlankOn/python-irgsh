class Distribution(object):
    def __init__(self, name, mirror, dist, components=['main'], extra=[]):
        self.name = name
        self.mirror = mirror
        self.dist = dist
        self.components = components
        self.extra = extra


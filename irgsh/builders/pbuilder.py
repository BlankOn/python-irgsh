import os
from subprocess import Popen
try:
    import simplejson as json
except ImportError:
    import json

from . import BaseBuilder, BuildFailedError
from ..utils import read_rcfile

class Pbuilder(BaseBuilder):
    def __init__(self, distribution, pbuilder_path, **opts):
        super(Pbuilder, self).__init__(distribution, **opts)

        self.pbuilder_path = pbuilder_path
        self.path = os.path.join(pbuilder_path, self.distribution.name)
        self.configfile = os.path.join(self.path, 'pbuilder.conf')

    def init(self):
        # Create directory structure
        paths = [self.path]
        paths += [os.path.join(self.path)
                  for path in ['aptcache', 'result', 'build', 'hook']]

        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)

        # Create distribution configuration
        fname = os.path.join(self.path, 'distribution.json')
        if not os.path.exists(fname):
            f = open(fname, 'w')
            f.write(json.dumps({'name': self.distribution.name,
                                'mirror': self.distribution.mirror,
                                'dist': self.distribution.dist,
                                'components': self.distribution.components,
                                'extra': self.distribution.extra}))
            f.close()

        # Create pbuilder configuration
        if not os.path.exists(self.configfile):
            def join(*name):
                return os.path.join(self.path, *name)
            def escape(value):
                if ' ' in value:
                    return '"%s"' % value
                return value

            components = ' '.join(self.distribution.components)
            othermirror = ' | '.join(self.distribution.extra)

            config = {'BASETGZ': join('base.tgz'),
                      'APTCACHE': join('aptcache'),
                      'BUILDRESULT': join('result'),
                      'BUILDPLACE': join('build'),
                      'HOOKDIR': join('hook'),
                      'MIRRORSITE': self.distribution.mirror,
                      'DISTRIBUTION': self.distribution.dist,
                      'COMPONENTS': components,
                      'OTHERMIRROR': othermirror}

            f = open(self.configfile, 'w')
            f.write('\n'.join(['%s=%s' % (key, escape(value))
                               for key, value in config.items()]))
            f.close()

    def reinit(self):
        fname = os.path.join(self.path, 'distribution.json')
        if os.path.exists(fname):
            os.unlink(fname)

        if os.path.exists(self.configfile):
            os.unlink(self.configfile)

        self.init()

    def create(self, stdout=None, stderr=None):
        # TODO: check if pbuilder.conf exists
        cmd = 'sudo pbuilder --create --configfile %s' % self.configfile

        p = Popen(cmd.split(), stdout=stdout, stderr=stderr)
        p.communicate()

        return p.returncode

    def update(self, stdout=None, stderr=None):
        # TODO: check if pbuilder.conf exists
        cmd = 'sudo pbuilder --update --configfile %s' % self.configfile

        p = Popen(cmd.split(), stdout=stdout, stderr=stderr)
        p.communicate()

        return p.returncode

    def build(self, dsc, resultdir, stdout=None, stderr=None):
        # TODO: check if pbuilder.conf exists
        cmds = []
        cmds.append('sudo pbuilder --build')
        cmds.append('--configfile %s' % self.configfile)
        cmds.append('--buildresult %s' % resultdir)
        cmds.append(dsc)

        cmd = ' '.join(cmds)
        p = Popen(cmd.split(), stdout=stdout, stderr=stderr)
        p.communicate()

        if p.returncode != 0:
            raise BuildFailedError(dsc)
        else:
            return self.get_changes_file(dsc)


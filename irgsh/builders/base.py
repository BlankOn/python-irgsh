from subprocess import PIPE

from debian_bundle.deb822 import Changes

from ..utils import get_architecture

class BuildFailedError(Exception):
    def __init__(self, source):
        self.source = source
    def __str__(self):
        return 'Build failed: %s' % self.source

class BaseBuilder(object):
    def __init__(self, distribution, **opts):
        self.distribution = distribution
        self._architecture = None

    @property
    def architecture(self):
        if self._architecture is None:
            self._architecture = get_architecture()
        return self._architecture

    def build(self, dsc, resultdir, stdout=PIPE, stderr=PIPE):
        '''
        Build package given its dsc file.

        returns the name of the changes file.
        '''
        raise NotImplementedError()

    def get_changes_file(self, dsc):
        changes = Changes(open(dsc))
        version = changes['Version'].split(':')[-1]

        fname = '%s_%s_%s.changes' % (changes['Source'], version,
                                      self.architecture)
        return fname


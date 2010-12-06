from debian_bundle.deb822 import Changes 

from ..utils import get_architecture

class BuildFailedError(Exception):
    def __init__(self, source):
        self.source = source
    def __str__(self):
        return 'Build failed: %s' % self.source

class BaseBuilder(object):
    def __init__(self, distro, **opts):
        self.distro = distro
        self._architecture = None

    @property
    def architecture(self):
        if self._architecture is None:
            self._architecture = get_architecture()
        return self._architecture

    def get_changes_file(self, dsc):
        changes = Changes(open(dsc))
        version = changes['Version'].split(':')[-1]

        changes_name = '%s_%s_%s.changes' % (changes['Source'], version,
                                             self.architecture)
        fname = os.path.join(self.result_directory, changes_name)

        return fname


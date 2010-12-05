import logging
import tempfile
from cStringIO import StringIO
import os
import re
from subprocess import Popen, PIPE

from debian_bundle.deb822 import Sources
from debian_bundle.changelog import Changelog

class InvalidControlFile(Exception):
    pass

class SourcePackage(object):
    def __init__(self, directory, orig=None):
        assert directory is not None

        self.directory = directory
        self.orig = orig

        self._metadata_populated = False

        self._binaries = None
        self._name = None
        self._directory = None
        self._maintainer = None
        self._changed_by = None
        self._version = None
        self._distribution = None
        self._orig = None

        self.log = logging.getLogger('irgsh.packages')

    def generate_dsc(self):
        version = version.split(':')[-1]
        package_version = '%s-%s' % (self.name, version)

        tmpdir = tempfile.mkdtemp('-irgsh-builder')
        if self.orig is None:
            self.generate_dsc_native(package_version, tmpdir)
        else:
            self.generate_dsc_with_orig(package_version, tmpdir)

        return os.path.join(tmpdir, '%s_%s.dsc' % (self.name, version))

    def generate_dsc_native(self, package_version, tmpdir):
        """Generate dsc for native package."""

        current_dir = os.getcwd()
        os.chdir(tmpdir)

        cmd = 'dpkg-source -b %s' % self.directory
        p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
        p.communicate()

        os.chdir(current_dir)

    def generate_dsc_with_orig(self, package_version, tmpdir):
        """Generate dsc for non-native package."""
        pass


    def parse_metadata(self):
        #
        # Read control file
        #
        self.log.debug('Reading debian/control file')
        fname = os.path.join(self.directory, 'debian', 'control')
        content = open(fname).read()

        # There might be a case when the source package is not defined
        # in the beginning
        name = None
        maintainer = None
        for block in re.split(r'\n\n+', content):
            f = StringIO(block)
            source = Source(f)
            name = source.get('Source', None)
            maintainer = source.get('Maintainer', None)
            if name is not None and maintainer is not None:
                break

        if name is None or maintainer is None:
            raise InvalidControlFile()

        self._name = name
        self._maintainer = maintainer

        #
        # Read changelog file
        #
        self.log.debug('Reading debian/changelog file')
        fname = os.path.join(self.directory, 'debian', 'changelog')
        changelog = Changelog(open(fname))

        self._changed_by = changelog.author
        self._version = changelog.version.full_version
        self._distribution = changelog.distributions

        self.log.debug('Source: %s (%s) %s' % (self._name, self._version, self._distribution))
        self._metadata_popupated = True

    def populate_binaries(self):
        # TODO
        pass

    @property
    def last_changelog(self):
        if not self._metadata_popupated:
            self.parse_metadata()
        return self._last_changelog

    @property
    def name(self):
        if not self._metadata_popupated:
            self.parse_metadata()
        return self._name

    @property
    def maintainer(self):
        if not self._metadata_popupated:
            self.parse_metadata()
        return self._maintainer

    @property
    def changed_by(self):
        if not self._metadata_popupated:
            self.parse_metadata()
        return self._changed_by

    @property
    def version(self):
        if not self._metadata_popupated:
            self.parse_metadata()
        return self._version

    @property
    def distribution(self):
        if not self._metadata_popupated:
            self.parse_metadata()
        return self._distribution

    @property
    def binaries(self):
        if self._binaries is None:
            self.populate_binaries()
        return self._binaries


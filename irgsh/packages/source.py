import logging
import tempfile
from cStringIO import StringIO
import os
import tarfile
import re
import shutil
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

    def generate_dsc(self, target, stdout=PIPE, stderr=PIPE):
        version = self.version.split(':')[-1]
        package_version = '%s-%s' % (self.name, version)

        if self.orig is None:
            self._generate_dsc_native(package_version, target, stdout, stderr)
        else:
            self._generate_dsc_with_orig(package_version, target,
                                         stdout, stderr)

        return '%s_%s.dsc' % (self.name, version)

    def _generate_dsc_native(self, package_version, target,
                             stdout=PIPE, stderr=PIPE):
        """Generate dsc for native package."""
        current_dir = os.getcwd()
        try:
            os.chdir(target)

            directory = self._find_changelog(self.directory, package_version)
            if directory is None:
                raise ValueError, 'Unable to find debian/changelog in the source package'

            cmd = 'dpkg-source -b %s' % directory
            p = Popen(cmd.split(), stdout=stdout, stderr=stderr)
            p.communicate()

        finally:
            os.chdir(current_dir)

    def _generate_dsc_with_orig(self, package_version, target,
                                stdout=PIPE, stderr=PIPE):
        """Generate dsc for non-native package."""

        # Check orig file
        tar = tarfile.open(self.orig)
        first = tar.next()

        if not first.isdir() or \
           not package_version.startswith(first.name):
            raise ValueError, "Orig file's contents mismatch " \
                              "with package version (%s vs %s)" % \
                              (first.name, package_version)

        current_dir = os.getcwd()
        try:
            os.chdir(target)

            # Find source directory
            sourcedir = self._find_changelog(self.directory)
            if sourcedir is None:
                raise ValueError, 'Unable to find debian/changelog in the source package'

            # Extract to .orig directory
            tar.extractall(target)
            dirname = os.path.join(target, first.name)
            os.rename(dirname, '%s.orig' % dirname)

            # Build the source package
            try:
                shutil.copytree(sourcedir, dirname)

                cmd = 'dpkg-source -b -sr %s' % dirname
                p = Popen(cmd.split(), stdout=stdout, stderr=stderr)
                p.communicate()

            finally:
                shutil.rmtree(dirname)
        finally:
            os.chdir(current_dir)

    def _find_changelog(self, dirname, package_version=None):
        # Check for debian/changelog
        if os.path.exists(os.path.join(dirname, 'debian', 'changelog')):
            return dirname

        if package_version is not None:
            # Check whether the source is inside a known subdirectory
            subdir = os.path.join(dirname, package_version)
            if not os.path.exists(subdir):
                return None
            if not os.path.exists(os.path.join(subdir, 'debian', 'changelog')):
                return None
            return subdir

        # There should be only one directory
        items = os.listdir(dirname)
        if len(items) != 1:
            return None

        subdir = os.path.join(dirname, items[0])
        if not os.path.exists(os.path.join(subdir, 'debian', 'changelog')):
            return None

        return subdir

    def parse_metadata(self):
        #
        # Read control file
        #
        self.log.debug('Reading debian/control file')
        dirname = self._find_changelog(self.directory)
        if dirname is None:
             raise ValueError, 'Unable to find debian/control in the source package'

        fname = os.path.join(dirname, 'debian', 'control')
        content = open(fname).read()

        # There might be a case when the source package is not defined
        # in the beginning
        name = None
        maintainer = None
        for block in re.split(r'\n\n+', content):
            f = StringIO(block)
            source = Sources(f)
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
        fname = os.path.join(dirname, 'debian', 'changelog')
        changelog = Changelog(open(fname))

        self._changed_by = changelog.author
        self._version = changelog.version.full_version
        self._distribution = changelog.distributions

        self.log.debug('Source: %s (%s) %s' % (self._name, self._version, self._distribution))
        self._metadata_populated = True

    def populate_binaries(self):
        # TODO
        pass

    @property
    def last_changelog(self):
        if not self._metadata_populated:
            self.parse_metadata()
        return self._last_changelog

    @property
    def name(self):
        if not self._metadata_populated:
            self.parse_metadata()
        return self._name

    @property
    def maintainer(self):
        if not self._metadata_populated:
            self.parse_metadata()
        return self._maintainer

    @property
    def changed_by(self):
        if not self._metadata_populated:
            self.parse_metadata()
        return self._changed_by

    @property
    def version(self):
        if not self._metadata_populated:
            self.parse_metadata()
        return self._version

    @property
    def distribution(self):
        if not self._metadata_populated:
            self.parse_metadata()
        return self._distribution

    @property
    def binaries(self):
        if self._binaries is None:
            self.populate_binaries()
        return self._binaries

def _test_run_native():
    from subprocess import Popen
    from ..sources.tarball import Tarball
    try:
        dirname = tempfile.mkdtemp()
        target = tempfile.mkdtemp()

        source = Tarball('http://archive.ubuntu.com/ubuntu/pool/main/a/apt/apt_0.7.25.3ubuntu7.tar.gz')
        source.export(dirname)

        pkg = SourcePackage(dirname)
        pkg.generate_dsc(target)

        cmd = 'find %s -ls' % target
        p = Popen(cmd.split())
        p.communicate()

    finally:
        shutil.rmtree(dirname)
        shutil.rmtree(target)

def _test_run_non_native():
    from subprocess import Popen
    from urllib import urlretrieve
    from ..sources.tarball import Tarball
    try:
        dirname = tempfile.mkdtemp()
        target = tempfile.mkdtemp()

        source = Tarball('http://archive.ubuntu.com/ubuntu/pool/universe/n/nginx/nginx_0.7.65-1ubuntu2.debian.tar.gz')
        source.export(dirname)

        orig, tmp = urlretrieve('http://archive.ubuntu.com/ubuntu/pool/universe/n/nginx/nginx_0.7.65.orig.tar.gz')

        pkg = SourcePackage(dirname, orig)
        pkg.generate_dsc(target)

        cmd = 'find %s -ls' % target
        p = Popen(cmd.split())
        p.communicate()

    finally:
        shutil.rmtree(dirname)
        shutil.rmtree(target)
        os.unlink(orig)

def _test_run():
    _test_run_native()
    _test_run_non_native()

if __name__ == '__main__':
    _test_run()


import tempfile
import os
import shutil
import tarfile
import gzip
import logging
from subprocess import Popen, PIPE

try:
    from debian.deb822 import Sources
except ImportError:
    from debian_bundle.deb822 import Sources

from irgsh.utils import find_debian, get_package_version, retrieve
from .error import SourcePackageBuildError, SourcePackagePreparationError

class SourcePackageBuilder(object):
    def __init__(self, source, source_type='tarball',
                 source_opts=None, orig=None):
        if source_opts is None:
            source_opts = {}
        self.source = source
        self.source_type = source_type
        self.source_opts = source_opts
        self.orig = orig

        if not source_type in ['patch', 'tarball', 'bzr']:
            raise ValueError, 'Unsupported source type: %s' % source_type
        if source_type == 'patch' and orig is None:
            raise ValueError, \
                  'A patch has to be accompanied with an orig file'

        self.log = logging.getLogger('irgsh.source.packager')

    def build(self, target):
        '''Build source package.

        This function returns the .dsc filename
        '''
        try:
            cwd = os.getcwd()
            build_path = tempfile.mkdtemp('-irgsh-srcpkg')

            # Prepare source directory
            package, version = self.prepare_source(build_path)
            source = '%s-%s' % (package, version)

            # Build
            self.log.debug('Building source package: source=%s type=%s opts=%s orig=%s' % (self.source, self.source_type, self.source_opts, self.orig))

            os.chdir(build_path)
            cmd = 'dpkg-source -b %s' % source
            p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE,
                      preexec_fn=os.setsid)
            out, err = p.communicate()

            if p.returncode != 0:
                raise SourcePackageBuildError(p.returncode, out, err)

            # Move result to the given target directory,
            # existing files will be replaced
            dsc = '%s_%s.dsc' % (package, version)
            files = [dsc]

            dsc_path = os.path.join(build_path, dsc)
            src = Sources(open(dsc_path))
            if not src.has_key('Files'):
                raise KeyError, 'Invalid source package'
            files += [item['name'] for item in src['Files']]

            self.log.debug('Moving source package files: %s' % ', '.join(files))

            for fname in files:
                target_path = os.path.join(target, fname)
                if os.path.exists(target_path):
                    os.unlink(target_path)
                shutil.move(os.path.join(build_path, fname), target_path)
                os.chmod(target_path, 0644)

            self.log.debug('Source package built: %s' % dsc)

            return dsc

        finally:
            shutil.rmtree(build_path)
            os.chdir(cwd)

    def prepare_source(self, target):
        try:
            tmp = tempfile.mkdtemp('-irgsh-srcpkg-prepare')

            self.log.debug('Preparing source code directory')

            # Download and extract source
            source_path = os.path.join(tmp, 'source')
            os.makedirs(source_path)
            self.log.debug('Downloading source code, type: %s' % self.source_type)
            source = self.download_source(source_path)
            self.log.debug('Source code downloaded')

            # Download orig
            orig = None
            orig_path = os.path.join(tmp, 'orig')
            os.makedirs(orig_path)
            if self.orig is not None:
                self.log.debug('Downloading original file')
                orig = self.download_orig(orig_path)
                self.log.debug('Original file downloaded')

            # Combine source and orig
            combined_path = os.path.join(tmp, 'combine')
            os.makedirs(combined_path)
            self.log.debug('Combining source and orig, type: %s' % self.source_type)
            combined_path = self.combine(source, orig, combined_path)
            self.log.debug('Source and orig combined')

            # Check for debian directory
            combined_path = find_debian(combined_path)
            if combined_path is None:
                raise ValueError, 'Unable to find debian directory'

            # Get version information
            package, version = get_package_version(combined_path)

            self.log.debug('Package: %s_%s' % (package, version))

            # Move source directory
            self.log.debug('Moving source code directory')

            final_path = os.path.join(target, '%s-%s' % (package, version))
            shutil.move(combined_path, final_path)

            # Move and rename orig file, if available
            if orig is not None:
                upstream = version.split('-')[0]
                orig_path = os.path.join(target, '%s_%s.orig.tar.gz' % \
                                                  (package, upstream))
                shutil.move(orig, orig_path)

            return package, version

        except StandardError, e:
            raise SourcePackagePreparationError(e)

        finally:
            shutil.rmtree(tmp)

    def download_orig(self, target):
        fname = retrieve(self.orig)
        orig_name = os.path.basename(self.orig)
        orig_path = os.path.join(target, orig_name)
        shutil.move(fname, orig_path)
        return orig_path

    def download_source(self, target):
        func = getattr(self, 'download_source_%s' % self.source_type)
        return func(target)

    def download_source_patch(self, target):
        fname = retrieve(self.source)
        patch_name = os.path.basename(self.source)
        patch_path = os.path.join(target, patch_name)
        shutil.move(fname, patch_path)
        return patch_path

    def download_source_tarball(self, target):
        try:
            tmp = tempfile.mkdtemp('-irgsh-tarball')

            tmpname = retrieve(self.source)

            source_name = os.path.basename(self.source)
            source_path = os.path.join(tmp, source_name)
            shutil.move(tmpname, source_path)

            tar = tarfile.open(source_path)
            tar.extractall(target)
            tar.close()

            return target
        except tarfile.ReadError, e:
            raise StandardError(e)

        finally:
            shutil.rmtree(tmp)

    def download_source_bzr(self, target):
        from .bazaar import BazaarExporter
        bzr = BazaarExporter(self.source, **self.source_opts)
        bzr.export(target)

        return target

    def extract_orig(self, orig, target):
        self.log.debug('Extracting orig file')

        tar = tarfile.open(orig)
        tar.extractall(target)
        tar.close()

        return self.find_orig_path(target)

    def combine(self, source, orig, extra_orig, target):
        self.log.debug('Combining source and orig, type: %s' % self.source_type)
        func = getattr(self, 'combine_%s' % self.source_type)
        return func(source, orig, extra_orig, target)

    def combine_patch(self, source, orig, target):
        if orig is None:
            raise ValueError, 'A patch has to be accompanied with an orig file'

        # Extract orig
        orig_path = self.extract_orig(orig, os.path.join(target, 'build'))

        # Apply patch
        try:
            cwd = os.getcwd()
            patch_path = os.path.abspath(source)
            patch = gzip.open(patch_path, 'rb')

            os.chdir(orig_path)
            cmd = 'patch -p1'
            p = Popen(cmd.split(), stdin=PIPE, stdout=PIPE, stderr=PIPE,
                      preexec_fn=os.setsid)
            p.stdin.write(patch.read())
            p.communicate()

            if p.returncode != 0:
                raise ValueError, 'Patch application failed'

            return orig_path
        finally:
            os.chdir(cwd)

    def combine_tarball(self, source, orig, target):
        if orig is not None:
            return self.combine_tarball_orig(source, orig, target)
        return source

    def combine_tarball_orig(self, source, orig, target):
        # Extract orig
        orig_path = self.extract_orig(orig, target)

        # Copy all files inside source
        cmd = 'cp -a %s/* %s/' % (source.rstrip('/'), orig_path.rstrip('/'))
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE,
                  preexec_fn=os.setsid)
        p.communicate()

        return find_debian(orig_path)

    def combine_bzr(self, source, orig, target):
        return self.combine_tarball(source, orig, target)

    def find_orig_path(self, dirname):
        # Find the correct orig directory
        # Rule: if orig directory contains only one directory,
        #       then that directory is the real orig directory
        #       otherwise, the orig directory is already real
        items = os.listdir(dirname)
        if len(items) == 1:
            if os.path.isdir(os.path.join(dirname, items[0])):
                dirname = os.path.join(dirname, items[0])

        return dirname


import os
import urllib
import shutil
import tempfile

from .packages.source import SourcePackage

class Packager(object):
    def __init__(self, specification, builder, resultdir,
                 stdout=None, stderr=None):
        self.specification = specification
        self.builder = builder
        self.resultdir = resultdir
        self.stdout = stdout
        self.stderr = stderr

    def build(self):
        '''Build package.

        This method will sequentially call export_source, retrieve_orig,
        genereate_dsc, and build_package.

        To call those four methods individually, use the following.

            >>> dsc_dir = "/tmp/dsc/"
            >>> source_dir = "/tmp/src/"
            >>> self.export_source(source_dir)
            >>> orig_path = self.retrieve_orig()
            >>> dsc = self.generate_dsc(dsc_dir, source_dir, orig_path)
            >>> dsc_path = os.path.join(dsc_dir, dsc)
            >>> self.build_package(dsc_path)
        '''
        try:
            target = tempfile.mkdtemp('-irgsh-builder')
            dsc = self._generate_dsc(target)

            dsc_path = os.path.join(target, dsc)
            result = self.build_package(dsc_path)
            return result

        finally:
            shutil.rmtree(target)

    def _generate_dsc(self, target):
        try:
            dirname = tempfile.mkdtemp('-irgsh-builder-source')
            self.export_source(dirname)

            orig_path = self.retrieve_orig()

            dsc = self.generate_dsc(target, dirname, orig_path)

            if orig_path is not None:
                os.remove(orig_path)

            return dsc

        finally:
            shutil.rmtree(dirname)

    def export_source(self, target):
        '''Extract source file to the given target directory.
        '''
        source = self.specification.get_source()
        source.export(target)

    def retrieve_orig(self):
        '''Download orig file, if available.
        '''
        orig = self.specification.orig
        orig_path = None
        if orig is not None:
            orig_path, tmp = urllib.urlretrieve(orig)
        return orig_path

    def generate_dsc(self, target, source_dir, orig_path):
        '''Generate dsc file from given source directory and path to the
        orig file in the target directory.
        '''
        pkg = SourcePackage(source_dir, orig_path)
        return pkg.generate_dsc(target)

    def build_package(self, dsc_path):
        '''Build a package given its dsc file (fullpath).
        '''
        return self.builder.build(dsc_path, self.resultdir, self.stdout, self.stderr)

def _test_run():
    from subprocess import Popen
    from .sources.tarball import Tarball
    from .builders.pbuilder import Pbuilder
    from .distribution import Distribution
    from .specification import Specification

    def lsdir(path):
        cmd = 'find %s -ls' % path
        p = Popen(cmd.split())
        p.communicate()

    try:
        target = tempfile.mkdtemp()
        pbuilder_path = tempfile.mkdtemp()

        location = 'http://archive.ubuntu.com/ubuntu/pool/universe/n/nginx/nginx_0.7.65-1ubuntu2.debian.tar.gz'
        orig = 'http://archive.ubuntu.com/ubuntu/pool/universe/n/nginx/nginx_0.7.65.orig.tar.gz'
        specification = Specification(location, orig, 'tarball')

        distro = dict(name='lucid',
                      mirror='http://mirror.liteserver.nl/pub/ubuntu/',
                      dist='lucid',
                      components=['main', 'universe'])
        distribution = Distribution(**distro)

        builder = Pbuilder(distribution, pbuilder_path)

        # the following two should be done automatically
        builder.init()
        builder.create()

        packager = Packager(specification, builder, target)
        packager.build()

        lsdir(pbuilder_path)
        lsdir(target)

    finally:
        shutil.rmtree(target)
        print 'Please remove the following directory:'
        print '-', pbuilder_path

if __name__ == '__main__':
    _test_run()


import os
import urllib
import shutil
import tempfile

from .source import prepare_source_package

class Packager(object):
    def __init__(self, specification, builder,
                 stdout=None, stderr=None):
        self.specification = specification
        self.builder = builder
        self.stdout = stdout
        self.stderr = stderr

    def build(self, target):
        '''Build package.
        '''

        try:
            tmp = tempfile.mkdtemp('-irgsh-builder')
            dsc = self.prepare_source_package(tmp)
            dsc_path = os.path.join(tmp, dsc)

            self.build_package(dsc_path, target)

        finally:
            shutil.rmtree(tmp)

    def build(self, target):
        '''Build package.
        '''
        try:
            target = tempfile.mkdtemp('-irgsh-builder')
            dsc = self._generate_dsc(target)

            dsc_path = os.path.join(target, dsc)
            result = self.build_package(dsc_path)
            return result

        finally:
            shutil.rmtree(target)

    def prepare_source_package(self, target):
        spec = self.specification
        return prepare_source_package(target, spec.location, spec.source_type,
                                      spec.source_opts)

    def build_package(self, dsc_path, target)
        '''Build a package given its dsc file (fullpath).
        '''
        return self.builder.build(dsc_path, target, self.stdout, self.stderr)

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


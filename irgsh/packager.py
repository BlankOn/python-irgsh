import os
import urllib
import shutil
import tempfile

from .packages.source import SourcePackage

class Packager(object):
    def __init__(self, specification, builder, resultdir,
                 stdout=None, stderr=None):
        self.specification = speficiation
        self.builder = builder
        self.resultdir = resultdir
        self.orig = orig
        self.stdout = stdout
        self.stderr = stderr

    def build(self):
        try:
            target = tempfile.mkdtemp('-irgsh-builder')
            fname = self._generate_dsc(target)

            dsc = os.path.join(target, fname)
            result = self.builder.build(dsc, self.resultdir,
                                        self.stdout, self.stderr)

            return result

        finally:
            shutil.rmtree(target)

    def _generate_dsc(self, target):
        try:
            dirname = tempfile.mkdtemp('-irgsh-builder-source')
            source = self.specification.get_source()
            source.export(dirname)

            orig = self.specification.orig
            orig_path = None
            if orig is not None:
                (orig_path, tmp) = urllib.urlretrieve(orig)

            pkg = SourcePackage(dirname, orig_path)
            dsc = pkg.generate_dsc(target, self.stdout, self.stderr)

            if orig_path is not None:
                os.remove(orig_path)

            return dsc

        finally:
            shutil.rmtree(dirname)

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


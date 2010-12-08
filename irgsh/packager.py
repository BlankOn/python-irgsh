import os
import urllib
import shutil
import tempfile
from subprocess import PIPE

from .packages.source import SourcePackage

class Packager(object):
    def __init__(self, source, builder, resultdir, orig=None,
                 stdout=PIPE, stderr=PIPE):
        self.source = source
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
            result = builder.build(dsc, self.resultdir,
                                   self.stdout, self.stderr)

            return result

        finally:
            shutil.rmtree(target)

    def _generate_dsc(self, target):
        try:
            dirname = tempfile.mkdtemp('-irgsh-builder-source')
            self.source.export(dirname)

            orig = None
            if self.orig is not None:
                (orig, tmp) = urllib.urlretrieve(self.orig)

            source = SourcePackage(dirname, orig)
            dsc = source.generate_dsc(target, self.stdout, self.stderr)

            if orig is not None:
                os.remove(orig)

            return dsc

        finally:
            shutil.rmtree(dirname)


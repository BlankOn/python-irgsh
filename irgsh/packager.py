import os
import urllib
import shutil
import tempfile
from subprocess import PIPE

from .packages.source import SourcePackage

class Packager(object):
    def __init__(self, source, orig=None):
        self.source = source
        self.orig = orig

    def build(self, builder, stdout=PIPE, stderr=PIPE):
        try:
            target = tempfile.mkdtemp('-irgsh-builder')
            fname = self._generate_dsc(target, stdout, stderr)

            dsc = os.path.join(target, fname)
            result = builder.build(dsc, stdout, stderr)

            return result

        finally:
            shutil.rmtree(target)

    def _generate_dsc(self, target, stdout=PIPE, stderr=PIPE):
        try:
            dirname = tempfile.mkdtemp('-irgsh-builder-source')
            self.source.export(dirname)

            orig = None
            if self.orig is not None:
                (orig, tmp) = urllib.urlretrieve(self.orig)

            source = SourcePackage(dirname, orig)
            dsc = source.generate_dsc(target, stdout, stderr)

            if orig is not None:
                os.remove(orig)

            return dsc

        finally:
            shutil.rmtree(dirname)


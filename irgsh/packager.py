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


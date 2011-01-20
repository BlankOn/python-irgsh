import os
import urllib
import shutil
import tempfile

from .source import prepare_source_package

class Packager(object):
    def __init__(self, specification, builder):
        self.specification = specification
        self.builder = builder

    def build(self, target, logger=None):
        '''Build package.
        '''

        try:
            tmp = tempfile.mkdtemp('-irgsh-builder')
            dsc = self.prepare_source_package(tmp)
            dsc_path = os.path.join(tmp, dsc)

            self.build_package(dsc_path, target, logger)

        finally:
            shutil.rmtree(tmp)

    def prepare_source_package(self, target):
        spec = self.specification
        return prepare_source_package(target, spec.location, spec.source_type,
                                      spec.source_opts)

    def build_package(self, dsc_path, target, logger=None)
        '''Build a package given its dsc file (fullpath).
        '''
        return self.builder.build(dsc_path, target, logger)


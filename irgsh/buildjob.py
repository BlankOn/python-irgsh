#! /usr/bin/python

from buildexceptions import BuildDownloadError
from sourcepackage import SourcePackage
from dvcs import DvcsIface
import shutil
import urllib
import tempfile
import os

class BuildJob(object):

    """ BuildJob defines a build job
    """
    def __init__(self, diff, orig=None):
        """ Constructor
        :param diff a Dvcs object
        :param orig the orig tarball object
        """
        self._diff = diff
        self._orig = orig

    def build(self, builder):
        """ Build the package
        :param builder the Builder object
        """
        dsc = self.generate_dsc()
        try:
            dir = os.path.dirname(dsc)
            results = builder.build(dsc)
        except:
            raise
        finally:
            shutil.rmtree(dir)

        return results
    
    #privates
    def generate_dsc(self):
        source_dir = tempfile.mkdtemp("-irgsh-builder-source")
        if self._diff.export(source_dir) == False:
            raise BuildDownloadError("Unable to export source code")

        orig_file = None
        if self._orig is not None:
            (orig_file, h) = urllib.urlretrieve(self._orig)

        s = SourcePackage(source_dir, orig_file)
        dsc = s.generate_dsc()
        if orig_file is not None:
            os.remove(orig_file)

        shutil.rmtree(source_dir)
        return dsc

if __name__ == '__main__':
    
    from distro import Distro
    from builder_pbuilder import Builder
    from dvcs_bzr import DvcsBzr
    d = Builder(Distro("ombilin"))
    #dvcs = DvcsBzr("http://dev.blankonlinux.or.id/bzr/ombilin/apt")
    #dvcs.tag = "0.7.25.3ubuntu3+blankon2.1"

    dvcs = DvcsBzr("http://dev.blankonlinux.or.id/bzr/ombilin/libcanberra")
    dvcs.tag = "0.22-1ubuntu2+blankon2"
    bj = BuildJob(dvcs, "http://mirror.unej.ac.id/ubuntu/pool/main/libc/libcanberra/libcanberra_0.22.orig.tar.gz")
    print bj.build(d)

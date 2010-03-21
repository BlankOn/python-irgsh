#! /usr/bin/python

from buildexceptions import *
from debian_bundle.deb822 import Changes 
from debian_bundle.deb822 import Packages
import os
import tempfile
import shutil
from subprocess import Popen
from subprocess import PIPE

from distro import Distro

class BuilderIface(object):
    """The thing which builds. Generic interface
    """

    _source = None

    def __init__(self, distro, build_directory = None, results_directory = None):
        """Creates a Builder instance
        
        :param distro: The Distro object
        :param build_directory: The directory in which builder will build the source package
        :param results_directory: The directory in which builder will copy the results
        """
        self._distro = distro
        self._build_directory = build_directory
        self._results_directory = results_directory
        self._build_architecture = None 

    @property
    def build_architecture(self):
        """ Returns the build architecture of this Builder
        """
        return self._build_architecture

    def build_source_package(self, source_package):
        """ Builds a SourcePackage
        """
        self._source = source_package.generate_dsc()
        return self.build(self._source)

    def build(self, source):
        """ Builds the thing
        Implementation class shall return the results()
        and set self._source to source
        """
        pass

    @property
    def build_directory(self):
        """ Returns the directory where the build takes place
        """
        return self._build_directory

    @property
    def results_directory(self):
        """ Returns the directory containing build results
        """
        return self._results_directory
    
    #privates
    def result(self):
        """ Returns the .changes file name as a result of the build
        """
        if self._source == None:
            return None

        dsc = Changes(file(self._source))
        versions = str(dsc["Version"]).split(":")
        version = None
        if len(versions) > 1:
            # for case "1:2.29.2ubuntu2"
            version = versions[1]
        else:
            version = versions[0]
 
        changes_file = self.results_directory + "/" + dsc["Source"] + "_" + version + "_" + self._build_architecture + ".changes"

        if os.path.exists(changes_file) == False:
            raise BuildBuilderFailureError("Building of %s failed" % (self._source))

        return changes_file

from sourcepackage import SourcePackage
from buildlog import BuildLog

if __name__ == '__main__':
    log = BuildLog("/tmp/log")
    d = Builder(Distro("ombilin"))
    #d.build("/tmp/apt_0.7.25.3ubuntu1.dsc")
    print d.build_architecture
    s = SourcePackage("/tmp/gimp-2.6.7", "/tmp/gimp_2.6.7.orig.tar.bz2")
    d.build_source_package(s)
    log.close()

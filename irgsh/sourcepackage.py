#! /usr/bin/python

from debian_bundle.deb822 import Packages
from debian_bundle.changelog import Changelog
import tarfile
import os
import shutil
import tempfile
from subprocess import Popen
from buildlog import BuildLog
from buildexceptions import BuildSourcePreparationError

class SourcePackage(object):

    _binaries = []
    _name = None
    _directory = None
    _maintainer = None
    _changed_by = None
    _version = None
    _distribution = None
    _orig = None
    _log = None

    def __init__(self, directory, orig = None):
        self._orig = orig
        self._directory = directory
        self._log = BuildLog()

    def last_changelog(self):
        if self._last_changelog == None:
            self.parse_metadata()

        return self._last_changelog

    @property
    def name(self):
        if self._name == None:
            self.parse_metadata()

        return self._name

    @property
    def maintainer(self):
        if self._maintainer == None:
            self.parse_metadata()

        return self._maintainer

    @property
    def changed_by(self):
        if self._changed_by == None:
            self.parse_metadata()

        return self._changed_by

    @property
    def version(self):
        if self._version == None:
            self.parse_metadata()

        return self._version

    @property
    def distribution(self):
        if self._distribution == None:
            self.parse_metadata()

        return self._distribution

    @property
    def binaries(self):
        if len(self._binaries) == 0:
            self.populate_binaries()

        return self._binaries

    def generate_dsc(self):
        dir = tempfile.mkdtemp("-irgsh-builder")
        if self._orig == None:
            self.generate_dsc_native(dir)
        else:
            self.generate_dsc_with_orig(dir)

        return dir + "/" + self.name + "_" + str(self._version) + ".dsc"

    # privates
    def generate_dsc_native(self, location):
        current_dir = os.getcwd()
        try:
            s.makedirs(location, 0700)
        except Exception as e:
            pass

        os.chdir(location)
        
        p = Popen("dpkg-source -b " + self._directory, shell=True, stdout=self._log.handle(), stderr=self._log.handle())
        os.waitpid(p.pid, 0)
        os.chdir(current_dir)

    def generate_dsc_with_orig(self, location):
        current_dir = os.getcwd()
        try:
            os.makedirs(location, 0700)
        except Exception as e:
            pass

        t = tarfile.open(self._orig)
        first_data = t.next()

        package_version = self.name + "-" + str(self._version)
        if first_data.isdir() and package_version.startswith(first_data.name):
            os.chdir(location)
            t.extractall(location)
            dirname = location + "/" + first_data.name
            os.rename(dirname, dirname + ".orig")
            shutil.copytree(self._directory, dirname)
            p = Popen("dpkg-source -b -sr " + dirname, shell=True, stdout=self._log.handle(), stderr=self._log.handle())
            os.waitpid(p.pid, 0)
            shutil.rmtree(dirname)
            os.chdir(current_dir)
        else:
            raise BuildSourcePreparationError("Orig's contents mismatch with package versioning")


    def populate_binaries(self):
        pass

    def parse_metadata(self):
        if self._directory != None:
            p = Packages(file(self._directory + "/debian/control")) 
            self._maintainer = p["Maintainer"]
            self._name = p["Source"]
            
            c = Changelog(file(self._directory + "/debian/changelog"))
            self._changed_by = c.author
            self._version = c.version
            self._distribution = c.distributions

if __name__ == '__main__':
    s = SourcePackage("/tmp/gimp-2.6.7", "/tmp/gimp_2.6.7.orig.tar.bz2")
    s.generate_dsc("/tmp/o") 

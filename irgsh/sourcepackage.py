#! /usr/bin/python

from debian_bundle.deb822 import Sources
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
        if self._last_changelog is None:
            self.parse_metadata()

        return self._last_changelog

    @property
    def name(self):
        if self._name is None:
            self.parse_metadata()

        return self._name

    @property
    def maintainer(self):
        if self._maintainer is None:
            self.parse_metadata()

        return self._maintainer

    @property
    def changed_by(self):
        if self._changed_by is None:
            self.parse_metadata()

        return self._changed_by

    @property
    def version(self):
        if self._version is None:
            self.parse_metadata()

        return self._version

    @property
    def distribution(self):
        if self._distribution is None:
            self.parse_metadata()

        return self._distribution

    @property
    def binaries(self):
        if len(self._binaries) == 0:
            self.populate_binaries()

        return self._binaries

    def generate_dsc(self):
        versions = str(self.version).split(":")
        version = None
        if len(versions) > 1:
            # for case "1:2.29.2ubuntu2"
            version = versions[1]
        else:
            version = versions[0]
        self._package_version = self.name + "-" + version 
 
        dir = tempfile.mkdtemp("-irgsh-builder")
        if self._orig is None:
            self.generate_dsc_native(dir)
        else:
            self.generate_dsc_with_orig(dir)

        return dir + "/" + self.name + "_" + version + ".dsc"

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

        if first_data.isdir() and self._package_version.startswith(first_data.name):
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
            raise BuildSourcePreparationError("Orig's contents mismatch with package versioning (%s vs %s)" % (first_data.name, self._package_version))


    def populate_binaries(self):
        pass

    def parse_metadata(self):
        if self._directory is not None:
            try:
                p = Sources(file(self._directory + "/debian/control")) 
                if p.has_key("Maintainer") and p.has_key("Source"):
                    self._maintainer = p["Maintainer"]
                    self._name = p["Source"]
                else:
                    # /debian/control has a initial whitespace, need to strip
                    f = open(self._directory + "/debian/control")
                    w = open(self._directory + "/debian/control.stripped", "w")
                    start = False
                    for line in f:
                        if line.startswith("Source: ") == True:
                            start = True
                        if start == True:
                            w.write(line)
                    w.close()
                    f.close()

                    p = Sources(file(self._directory + "/debian/control.stripped")) 
                    try:
                        self._maintainer = p["Maintainer"]
                        self._name = p["Source"]
                    except Exception as e:
                        raise BuildSourcePreparationError("Control file in %s has error: %s" % (self._directory + "/debian/control", e))
            except Exception as e:
                raise BuildSourcePreparationError("Control file in %s has error: %s" % (self._directory + "/debian/control", e))

            c = Changelog(file(self._directory + "/debian/changelog"))
            self._changed_by = c.author
            self._version = c.version
            self._distribution = c.distributions

if __name__ == '__main__':
    s = SourcePackage("/tmp/gimp-2.6.7", "/tmp/gimp_2.6.7.orig.tar.bz2")
    print s.generate_dsc() 

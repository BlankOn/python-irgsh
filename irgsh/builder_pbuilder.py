#! /usr/bin/python

from buildexceptions import *
import os
from stat import *
import shutil
from subprocess import Popen
from subprocess import PIPE

from distro import Distro
from builder import BuilderIface
from buildlog import BuildLog

class builder_pbuilder(BuilderIface):
    """The thing which builds. Uses Pbuilder.
    """

    _conf = None
    _extra_component_hook = "D01extracomponents"
    def __init__(self, distro, build_directory = None, results_directory = None):
        """Creates a Builder instance
        
        :param distro: The Distro object
        :param build_directory: The directory in which pbuilder will build the source package, if not specified uses the default directory of pbuilder build directory
        :param results_directory: The directory in which pbuilder will copy the results, if not specified, uses the default directory of pbuilder results directory
        """
        self._distro = distro
        self._path = "/var/lib/irgsh/pbuilder"
        self._build_directory = build_directory
        self._results_directory = results_directory
        self._build_architecture = Popen("dpkg-architecture -qDEB_BUILD_ARCH", shell=True, stdout=PIPE).communicate()[0].strip()

        self._conf = self._path + "/" + self._distro.name + "/pbuilder.conf" 
        if os.path.exists(self._conf) == False:
            raise BuildBuilderConfigurationError("Unable to open %s" % (self._conf))
        self._conf_results_directory = None

        self._mirror = ""
        self._hookdir = ""
        file = open(self._conf)
        for line in file:
            if line.startswith("BUILDRESULT"):
                self._conf_results_directory = line.replace("BUILDRESULT", "").strip("=").strip().strip("\"").strip()
            elif line.startswith("MIRRORSITE="):
                self._mirror = line.replace("MIRRORSITE", "").strip("=").strip().strip("\"").strip()
            elif line.startswith("HOOKDIR="):
                self._hookdir = line.replace("HOOKDIR", "").strip("=").strip().strip("\"").strip()

        file.close()

    """ /reimp
    """
    def build(self, source):
        self._source = source
        current_dir = os.getcwd()
        dir = os.path.dirname(source)
        os.chdir(dir)
        
        # Clears hook file before building
        # It will be regenerated when necessary prior building
        # in generate_arguments()
        if self._hookdir:
            hookfile = os.path.join(self._hookdir, self._extra_component_hook)
            if os.path.isfile(hookfile):
                os.unlink(hookfile)

        log = BuildLog()
        args = self.generate_build_arguments(source)
        print "Building with arguments: %s" % args
        p = Popen("sudo pbuilder " + args, shell=True, stdout=log.handle(), stderr=log.handle())
        os.waitpid(p.pid, 0)

        os.chdir(current_dir)
        result = self.result()
        return result

    @property
    def build_directory(self):
        if self._build_directory == None:
            build_directory = None

            file = open(self._conf)
            for line in file:
                if line.startswith("BUILDPLACE"):
                    build_directory = line.replace("BUILDPLACE", "").strip("=").strip()
                    break
            file.close()

            if results_directory == None:
                raise BuilderBuildConfigurationError("Build directory is not defined in %s configuration file" % (self._conf))

            return build_directory
        else:
            return self._build_directory

    @property
    def results_directory(self):
        if self._results_directory == None:

            results_directory = self._conf_results_directory
            if results_directory == None:
                raise BuilderBuildConfigurationError("Results directory is not defined in %s configuration file" % (self._conf))
            return results_directory
        else:
            return self._results_directory

    #privates
    def generate_arguments(self):
        args = ""
        if self._build_directory != None:
            args += " --buildplace " + self._build_directory

        if self._results_directory != None:
            args += " --buildresult " + self._results_directory

        if self._components != None:
            if os.path.isdir(self._hookdir):
                script = "#!/bin/sh\n"
                script += "echo \"deb %s %s %s\" >> /etc/apt/sources.list\n" % (self._mirror, self._distro.name, self._components)
                script += "apt-get update\n"

                hook = os.path.join(self._hookdir, self._extra_component_hook)
                f = open(hook, "w")
                f.write(script)
                f.close()
                os.chmod(hook, S_IRUSR | S_IXUSR | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH) 

        path = self._path + "/" + self._distro.name 
        args += " --configfile " + path + "/pbuilder.conf "

        return args

    def generate_build_arguments(self, source):
        args = " build "

        args += self.generate_arguments()
        args += source 
        return args

from sourcepackage import SourcePackage
from buildlog import BuildLog

if __name__ == '__main__':
    d = Builder(Distro("ombilin"))
    #d.build("/tmp/apt_0.7.25.3ubuntu1.dsc")

    l = BuildLog("/tmp/log")
    print d.build_architecture
    s = SourcePackage("/tmp/gimp-2.6.7", "/tmp/gimp_2.6.7.orig.tar.bz2")
    print d.build_source_package(s)

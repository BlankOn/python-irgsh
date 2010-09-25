#!/usr/bin/python

import log
from dvcs import DvcsIface
import urllib2
import tarfile
import os

class dvcs_tarball(DvcsIface):
    def export(self, destination):
        filename = os.path.basename(self._url)
        if filename == "":
            print "URL %s doesn't contain filename" % self._url
            return False

        filename = os.path.join(destination, filename)
        self._log.write("Exporting %s to %s" % (self._url, destination))
        result = False        

        try:
            f = urllib2.urlopen(self._url)
            local = open(filename, "w")
            local.write(f.read())
            local.close()

        except Exception as e:
            print "Unable to export: %s" % e
            return result
        
        try:
            t = tarfile.open(filename)
            t.extractall(destination)
            t.close()
            os.unlink(filename)
            result = True
        except Exception as e:
            print "Unable to open %s as tarball: %s" % (destination, e)


        return result

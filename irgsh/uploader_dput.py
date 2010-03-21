#!/usr/bin/python

from subprocess import Popen
from uploadexceptions import *
from uploader import UploaderIface
from uploadlog import UploadLog
import tempfile
import shutil
import os

class UploaderDput(UploaderIface):
    """ Upload using Debian's dput
    """

    _host = None
    _distribution = None
    _changes = None
    _dir = None

    def __init__(self, host, distribution, changes):
        self._host = host
        self._distribution = distribution
        self._changes = changes
        self._log = UploadLog()

    # /reimp
    def pre_upload(self):
        conf = "/etc/dput-%s.cf" % (self._distribution)
        if os.path.exists(conf) == False:
            raise UploadUploaderConfigurationError("Missing %s configuration file" % (conf))

        self._dir = tempfile.mkdtemp("-irgsh-uploader")
        self._log.write("Processing the upload request in %s" % (self._dir))
        f = open(conf)
        w = open(self._dir + "/dput.cf", "w")
        command = "touch %s/uploaded" % (self._dir)
        for line in f:
            if line.startswith("post_upload_command"):
                line = "post_upload_command = %s\n" % (command)

            w.write(line)
        w.close()
        f.close()

    def post_successful_upload(self):
        """ Does cleaning up after a successful upload
        """
        os.remove(self._dir + "/dput.cf")
        self._log.write("Upload is successful")

    def post_failed_upload(self):
        """ Does cleaning up after a failed upload
        """
        self._log.write("Upload is failed")

    def post_upload(self):
        shutil.rmtree(self._dir)

    def do_upload(self):

        p = Popen("dput -c %s/dput.cf %s" % (self._dir, self._changes), shell=True, stdout=self._log.handle(), stderr=self._log.handle())
        os.waitpid(p.pid, 0)

        return os.path.exists("%s/uploaded" % (self._dir))

if __name__ == '__main__':
    u = UploaderDput("", "ombilin", "/var/lib/irgsh/pbuilder/ombilin/result/gimp_2.6.7-1ubuntu1+blankon2_i386.changes")
    u.upload()

import shutil
import os
from subprocess import Popen
import tempfile

from . import BaseUploader, UploadFailedError

class Dput(BaseUploader):
    def upload(self, changes, stdout=None, stderr=None):
        try:
            dirname = tempfile.mkdtemp('-irgsh-uploader')
            config = '/etc/dput.cf'

            cmd = 'dput -c %s %s' % (config, changes)
            p = Popen(cmd.split(), stdout=stdout, stderr=stderr)
            p.communicate()

        finally:
            shutil.rmtree(dirname)


import shutil
import os
from subprocess import Popen
import tempfile

from . import BaseUploader, UploadFailedError

CONFIG_TEMPLATE = '''\
[DEFAULT]
allow_dcut              = 1
hash                    = md5
allow_unsigned_uploads  = 1
run_lintian             = 0
run_dinstall            = 0
check_version           = 0
scp_compress            = 0
post_upload_command     =
pre_upload_command      =
allowed_distributions   = %(name)s
progress_indicator      = 2
default_host_main       = %(name)s

[%(name)s]
login                   = incoming
fqdn                    = irgsh.blankonlinux.or.id
method                  = scp
incoming                = incoming/
'''

class Dput(BaseUploader):
    def upload(self, changes, stdout=None, stderr=None):
        try:
            fd, config = tempfile.mkstemp('-irgsh-dput')
            self._create_config(config)

            cmd = 'dput -c %s %s' % (config, changes)
            p = Popen(cmd.split(), stdout=stdout, stderr=stderr)
            p.communicate()

            if p.returncode != 0:
                raise UploadFailedError, 'Fail to upload %s: %s' % \
                                         (changes, p.returncode)

        finally:
            os.unlink(config)

    def _create_config(self, target):
        config = CONFIG_TEMPLATE % {'name': self.distribution.name}
        f = open(target, 'w')
        f.write(config)
        f.close()


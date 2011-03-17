import logging
import os
from subprocess import Popen, PIPE
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
login                   = %(user)s
fqdn                    = %(host)s
method                  = scp
incoming                = %(path)s
'''

class Dput(BaseUploader):
    def __init__(self, distribution, **opts):
        super(Dput, self).__init__(distribution, **opts)

        self.log = logging.getLogger('irgsh.uploaders.dput')
        self.user = opts['user']
        self.host = opts['host']
        self.path = opts['path']

    def upload(self, changes, stdout=PIPE, stderr=PIPE):
        self.log.debug('Uploading %s' % changes)

        try:
            fd, config = tempfile.mkstemp('-irgsh-dput')
            self._create_config(config)

            cmd = 'dput -c %s %s' % (config, changes)
            p = Popen(cmd.split(), stdout=stdout, stderr=stderr,
                      preexec_fn=os.setsid)
            p.communicate()

            if p.returncode != 0:
                self.log.error('Upload failed, returncode: %s' % p.returncode)
                raise UploadFailedError(changes, p.returncode)

        finally:
            os.unlink(config)

    def _create_config(self, target):
        param = {'name': self.distribution.name,
                 'host': self.host,
                 'path': self.path,
                 'user': self.user}
        config = CONFIG_TEMPLATE % param

        f = open(target, 'w')
        f.write(config)
        f.close()


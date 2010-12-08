import logging
import tempfile
from urlparse import urlparse
import tarfile
import urllib2
import os

from . import BaseSource, InvalidSourceLocationError, \
              register_source_class

class Tarball(BaseSource):
    def __init__(self, location, **opts):
        super(Tarball, self).__init__(location, **opts)

        self.log = logging.getLogger('irgsh.sources.tarball')

    def export(self, target):
        try:
            fd, tmp = tempfile.mkstemp()
            self.export_source(self.location, tmp, target)
        finally:
            os.unlink(tmp)

    def export_source(self, source, tmp, target):
        self.log.debug('Exporting %s to %s' % (self.location, target))

        # Check location
        parse = urlparse(source)
        filename = os.path.basename(parse.path)
        if filename == '':
            raise InvalidSourceLocationError(source)

        # Download file
        try:
            f = urllib2.urlopen(source)
            local = open(tmp, 'wb')
            local.write(f.read())
            local.close()
        except Exception as e:
            self.log.error('Unable to export %s: %s' % (source, e))
            raise

        # Extract tarball
        try:
            t = tarfile.open(tmp)
            t.extractall(target)
            t.close()
        except Exception as e:
            self.log.error('Unable to extract tarball %s: %s' % \
                           (source, e))
            raise

register_source_class('tarball', Tarball)

def _test_run():
    import shutil
    from subprocess import Popen
    try:
        tmpdir = tempfile.mkdtemp()
        print 'Target:', tmpdir

        tarball = Tarball('http://archive.ubuntu.com/ubuntu/pool/universe/n/nginx/nginx_0.7.65.orig.tar.gz')
        tarball.export(tmpdir)

        cmd = 'find %s -ls' % tmpdir
        p = Popen(cmd.split())
        p.communicate()

    finally:
        shutil.rmtree(tmpdir)

if __name__ == '__main__':
    _test_run()


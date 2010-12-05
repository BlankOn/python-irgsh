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

    def export(self, target):
        try:
            tmp = tempfile.mkstemp()
            self.export_source(self.location, tmp, target)
        finally:
            os.unlink(tmp)

    def export_source(self, source, tmp, target):
        self.log.debug('Exporting %s to %s' % (self.location, target)

        # Check location
        parse = urlparse(location)
        filename = os.path.basename(parse.path)
        if filename == '':
            raise InvalidSourceLocationError(self.location)

        # Download file
        try:
            f = urllib2.urlopen(source)
            local = open(tmp, 'wb')
            local.write(f.read())
            local.close()
        except Exception as e:
            self.log.error('Unable to export %s: %s' % (self.location, e))
            raise

        # Extract tarball
        try:
            t = tarfile.open(tmp)
            t.extractall(target)
            t.close()
        except Exception as e:
            self.log.error('Unable to extract tarball %s: %s' % \
                           (self.location, e))
            raise

register_source_class('tarball', Tarball)


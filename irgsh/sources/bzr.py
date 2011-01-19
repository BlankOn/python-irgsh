import logging

from bzrlib.branch import Branch
import bzrlib.export

from . import BaseSource, InvalidSourceLocationError, \
              register_source_class

class BZR(BaseSource):
    def __init__(self, location, **opts):
        super(BZR, self).__init__(location, **opts)

        self.tag = opts.get('tag', None)
        self.revision = opts.get('revision', None)

        self.log = logging.getLogger('irgsh.sources.bzr')

    def export(self, target):
        self.log.debug('Exporting %s to %s' % (self.location, target))

        # Check branch
        try:
            remote = Branch.open(self.location)
        except Exception, e:
            raise InvalidSourceLocationError(self.location, e)

        # Get revision id
        revid = None
        if self.revision is not None:
            try:
                revid = remote.get_rev_id(self.revision)
            except Exception, e:
                desc = "Unknown revision '%s'" % self.revision
                raise InvalidSourceLocationError(self.location, desc)

        elif self.tag is not None:
            try:
                revid = remote.tags.lookup_tag(self.tag)
            except Exception, e:
                desc = "Unknown tag '%s'" % self.tag
                raise InvalidSourceLocationError(self.location, desc)

        else:
            revid = remote.last_revision()

        # Get tree
        try:
            tree = remote.repository.revision_tree(revid)
        except Exception, e:
            desc = 'Unable to open revision %s: %s' % (revid, e)
            raise InvalidSourceLocationError(self.location, desc)

        # Export tree
        try:
            bzrlib.export.export(tree, target, None)
        except Exception, e:
            desc = 'Unable to export %s to %s: %s' % (self.location, target, e)
            raise InvalidSourceLocationError(self.location, desc)

register_source_class('bzr', BZR)

def _test_run():
    import shutil
    import tempfile
    from subprocess import Popen
    try:
        tmpdir = tempfile.mkdtemp()
        print 'Target:', tmpdir

        bzr = BZR('http://www.gnome.org/~jdub/bzr/planet/devel/trunk/')
        bzr.export(tmpdir)

        cmd = 'find %s -ls' % tmpdir
        p = Popen(cmd.split())
        p.communicate()

    finally:
        shutil.rmtree(tmpdir)

if __name__ == '__init__':
    _test_run()


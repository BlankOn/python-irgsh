import logging

from bzrlib.branch import Branch
import bzrlib.export

class BazaarExporter(object):
    def __init__(self, source, **opts):
        self.source = source
        self.tag = opts.get('tag', None)
        self.revision = opts.get('revision', None)

        self.log = logging.getLogger('irgsh.sources.bzr')

    def export(self, target):
        self.log.debug('Exporting %s to %s' % (self.source, target))

        # Check branch
        try:
            remote = Branch.open(self.source)
        except Exception, e:
            raise ValueError, 'Invalid Bazaar repository: %s' % self.source

        # Get revision id
        revid = None
        if self.revision is not None:
            try:
                revid = remote.get_rev_id(self.revision)
            except Exception, e:
                raise ValueError, 'Invalid Bazaar revision: %s' % self.revision

        elif self.tag is not None:
            try:
                revid = remote.tags.lookup_tag(self.tag)
            except Exception, e:
                raise ValueError, 'Invalid Bazaar tag: %s' % self.tag

        else:
            revid = remote.last_revision()

        # Get tree
        try:
            tree = remote.repository.revision_tree(revid)
        except Exception, e:
            raise ValueError, 'Unable to open Bazaar tree: %s (%s)' % \
                              (str(e), revid)

        # Export tree
        try:
            bzrlib.export.export(tree, target, None)
        except Exception, e:
            raise ValueError, 'Unable to export Bazaar tree: %s' % str(e)


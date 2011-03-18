import logging

from bzrlib.branch import Branch
import bzrlib.export

class BazaarExporter(object):
    def __init__(self, source, **opts):
        self.source = source
        self.tag = opts.get('tag', None)
        self.revision = opts.get('revision', None)

        self.log = logging.getLogger('irgsh.source')

    def export(self, target):
        self.log.debug('Exporting %s to %s' % (self.source, target))

        # Check branch
        remote = Branch.open(self.source)

        # Get revision id
        revinfo = None
        revid = None
        if self.revision is not None:
            revid = remote.get_rev_id(self.revision)
            revinfo = 'rev: %s' % self.revision
        elif self.tag is not None:
            revid = remote.tags.lookup_tag(self.tag)
            revinfo = 'tag: %s' % self.tag
        else:
            revid = remote.last_revision()
            revinfo = 'last'

        # Get tree
        tree = remote.repository.revision_tree(revid)

        # Export tree
        self.log.debug('Downloading bazaar tree: %s (%s)' % (self.source, revinfo))
        bzrlib.export.export(tree, target, None)


#!/usr/bin/python

import log
from dvcs import DvcsIface
from bzrlib.branch import Branch
import bzrlib.export

class DvcsBzr(DvcsIface):
    def export(self, destination):
        self._log.write("Exporting %s to %s" % (self._url, destination))
        result = False        

        if self._tag == None and self._revision == None:
            self._log.write("TAG and REVISION are undefined") 
            return result

        try:
            remote = Branch.open(self._url)

        except Exception as e:
            self._log.write("Unable to open %s: %s" % (self._url, e))
            return result

        revid = ''
        tree = None
        if self._revision != None:
            try:
                revid = remote.get_rev_id(self._revision)
            except Exception as e:
                self._log.write("Unable to find revision %s: %s" % (self._revision, e))
                return result
        elif self._tag != None:
            try:
                revid = remote.tags.lookup_tag(self._tag)
            except Exception as e:
                self._log.write("Unable to find tag %s: %s" % (self._tag, e))
                return result
        
        try:
            tree = remote.repository.revision_tree(revid)
        except Exception as e:
            self._log.write("Unable to open the revision %s: %s" % (revid, e))
            return result

        try:
            bzrlib.export.export(tree, destination, "dir")
            result = True
        except Exception as e:
            self._log.write("Unable to export %s to %s: %s" % (self._url, destination, e))
            
        return result 

if __name__ == '__main__':
    bzr = DvcsBzr("https://code.launchpad.net/anna")
    bzr = DvcsBzr("http://dev.blankonlinux.or.id/bzr/ombilin/gimp/")
    #bzr.revision = 'Arch-1:anna@bazaar.ubuntu.com%anna--MAIN--0--patch-1'
    bzr.tag = "gimp_2.6.7-1ubuntu1+blankon2"
    bzr.export("/tmp/gimp")

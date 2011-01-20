import os
import shutil
from urllib import urlretrieve

try:
    from debian.deb822 import Sources
except ImportError:
    from debian_bundle.deb822 import Sources

class SourceDownloader(object):
    def __init__(self, source, base=None):
        self.source = source

        if base is None:
            base = os.path.dirname(source)
        self.base = base

    def download(self, target):
        dsc = os.path.basename(self.source)
        dsc_path = os.path.join(target, dsc)

        # Download .dsc file
        tmp, headers = urlretrieve(self.source)
        shutil.move(tmp, dsc_path)

        # Download required files
        src = Sources(open(dsc_path))
        files = [info['name'] for info in src['Files']]

        for fname in files:
            url = os.path.join(self.base, fname)
            tmp, headers = urlretrieve(url)

            path = os.path.join(target, fname)
            shutil.move(tmp, path)

        return dsc


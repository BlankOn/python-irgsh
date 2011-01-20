from .downloader import SourceDownloader
from .packager import SourcePackageBuilder

def prepare_source_package(target, source, source_type='tarball',
                           source_opts=None, orig=None):
    if source_opts is None:
        source_opts = {}

    if source_type == 'dsc':
        downloader = SourceDownloader(source, source_opts.get('base', None))
        return downloader.download(target)
    else:
        packager = SourcePackageBuilder(source, source_type, source_opts, orig)
        return packager.build(target)


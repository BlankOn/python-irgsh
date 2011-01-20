from subprocess import Popen, PIPE
import os

_architecture = None
def get_architecture():
    """Get build architecture"""
    global _architecture
    if _architecture is None:
        p = Popen("dpkg-architecture -qDEB_BUILD_ARCH".split(),
                  stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        _architecture = stdout.strip()

    return _architecture

def find_changelog(source_dir, package_version=None):
    # Check for debian/changelog
    if os.path.exists(os.path.join(source_dir, 'debian', 'changelog')):
        return source_dir

    if package_version is not None:
        # Check whether the source is inside a known subdirectory
        subdir = os.path.join(source_dir, package_version)
        if not os.path.exists(os.path.join(subdir, 'debian', 'changelog')):
            return None
        return subdir

    # There should be only one directory
    items = os.listdir(source_dir)
    if len(items) != 1:
        return None

    subdir = os.path.join(source_dir, items[0])
    if not os.path.exists(os.path.join(subdir, 'debian', 'changelog')):
        return None

    return subdir

def find_debian(dirname):
    '''
    Find debian directory
    '''
    # check for debian directory inside the given directory
    debian = os.path.join(dirname, 'debian')
    if os.path.exists(debian) and os.path.isdir(debian):
        return dirname

    # if it's not there, make sure we have exactly one directory inside
    items = os.listdir(dirname)
    if len(items) != 1:
        return None
    dirname = os.path.join(dirname, items[0])
    if not os.path.isdir(dirname):
        return None

    # and inside it, there should be a debian directory
    debian = os.path.join(dirname, 'debian')
    if os.path.exists(debian) and os.path.isdir(debian):
        return dirname

    # if not, we found nothing
    return None

def get_package_version(dirname):
    try:
        from debian.changelog import Changelog
    except ImportError:
        from debian_bundle.changelog import Changelog

    changelog = os.path.join(dirname, 'debian', 'changelog')

    ch = Changelog(open(changelog))
    package = ch.package
    version = str(ch.version).split(':')[-1]

    return package, version


import urllib2
import os
import tempfile
from subprocess import Popen, PIPE

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

def find_debian(dirname):
    '''
    Find debian directory
    '''
    # check directory existance
    if not os.path.exists(dirname):
        return None

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

    # Remove epoch
    version = str(ch.version).split(':')[-1]

    # Remove debian version
    p = version.split('-')
    if len(p) > 1:
        p = p[:-1]
    version = '-'.join(p)

    return package, version

def retrieve(url):
    ext = os.path.splitext(url)[1]
    tmp = tempfile.mkstemp(ext)[1]

    p = urllib2.urlopen(url)
    f = open(tmp, 'wb')
    f.write(p.read())
    f.close()

    return tmp


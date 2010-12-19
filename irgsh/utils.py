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


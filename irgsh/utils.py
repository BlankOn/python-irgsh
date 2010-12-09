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


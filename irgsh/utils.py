import tempfile
from subprocess import Popen, PIPE
import os

_architecture = None
def get_architecture():
    """Get build architecture"""
    global _architecture
    if _architecture is None:
        from subprocess import Popen, PIPE
        p = Popen("dpkg-architecture -qDEB_BUILD_ARCH".split(), stdout=PIPE)
        stdout, stderr = p.communicate()
        _architecture = stdout.strip()

    return _architecture


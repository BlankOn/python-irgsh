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

def read_rcfile(fname):
    fd, tmp1 = tempfile.mkstemp()
    fd, tmp2 = tempfile.mkstemp()

    try:
        script = ' ; '.join([
            'set > %s' % tmp1,
            'source %s' % fname,
            'set > %s' % tmp2,
            'diff %s %s | grep ">"' % (tmp1, tmp2),
        ])
        cmd = ['bash', '-c', script]
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()

        config = {}
        for line in out.splitlines():
            key, val = line[2:].split('=', 1)
            config[key] = val

        return config

    finally:
        os.unlink(tmp1)
        os.unlink(tmp2)


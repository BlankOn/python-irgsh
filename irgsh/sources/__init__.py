from .base import BaseSource, InvalidSourceLocationError, \
                  register_source_class, get_source_class, build_source

# Make sure to load the sources modules so they will be registered
from . import tarball, bzr


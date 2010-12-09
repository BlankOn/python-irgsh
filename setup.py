#!/usr/bin/python

from setuptools import setup

def get_version():
    import irgsh
    return irgsh.__version__

setup(name='irgsh', 
      version=get_version(),
      description='Python interface to irgsh',
      url='http://irgsh.blankonlinux.or.id',
      packages=['irgsh'],
      maintainer='BlankOn Developers',
      maintainer_email='blankon-dev@googlegroups.com',
     )


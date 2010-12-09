#!/usr/bin/python

from setuptools import setup

def get_version():
    import irgsh
    return irgsh.__version__

packages = ['irgsh', 'irgsh.builders', 'irgsh.packages', 'irgsh.sources',
            'irgsh.uploaders']

setup(name='irgsh', 
      version=get_version(),
      description='Python interface to irgsh',
      url='http://irgsh.blankonlinux.or.id',
      packages=packages,
      maintainer='BlankOn Developers',
      maintainer_email='blankon-dev@googlegroups.com',
     )


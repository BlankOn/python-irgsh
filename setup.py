#!/usr/bin/python

from setuptools import setup

def get_version():
    import irgsh
    return irgsh.__version__

packages = ['irgsh', 'irgsh.builders', 'irgsh.source', 'irgsh.uploaders']

setup(name='python-irgsh',
      version=get_version(),
      description='Irgsh Python Library',
      url='http://irgsh.blankonlinux.or.id',
      packages=packages,
      maintainer='BlankOn Developers',
      maintainer_email='blankon-dev@googlegroups.com',
      install_requires=['setuptools', 'python-debian', 'simplejson', 'pyliblzma'],
     )


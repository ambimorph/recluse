#!/usr/bin/env python

from distutils.core import setup

setup(name='recluse',
      version='0.1.7',
      description='Reproducible Experimentation for Computational Linguistics Use',
      long_description=open('README.rst').read(),
      author='L. Amber Wilcox-O\'Hearn',
      author_email='amber@cs.toronto.edu',
      url='https://github.com/lamber/recluse',
      package_dir = {'':'code'},
      packages=['recluse', 'recluse.test'],
      license='COPYING',
     )

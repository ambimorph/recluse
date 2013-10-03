#!/usr/bin/env python

from distutils.core import setup
import versioneer

versioneer.versionfile_build='recluse/_version.py'
versioneer.versionfile_source='recluse/_version.py'
versioneer.tag_prefix = 'recluse-'
versioneer.parentdir_prefix = 'recluse-'


setup(name='recluse',
      description='Reproducible Experimentation for Computational Linguistics Use',
      long_description=open('README.rst').read(),
      author='L. Amber Wilcox-O\'Hearn',
      author_email='amber@cs.toronto.edu',
      url='https://github.com/lamber/recluse',
      scripts=['scripts/nltkbasedsegmentertokeniserrunner'],
      packages=['recluse', 'recluse.test'],
      package_data={"recluse.test": ["data/*"]},
      license='COPYING',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass()
     )

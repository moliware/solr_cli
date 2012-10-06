# -*- coding: utf-8 -*-
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from solr_cli import __version__


REQUIRED = ['mysolr>=0.7.1', 'pygments']
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python',
    'Environment :: Console'
]


setup(name='solr_cli',
      version=__version__,
      description='Command line client for Apache Solr',
      long_description = open('README.rst').read(),
      author='Miguel Olivares',
      author_email='miguel@moliware.com',
      url='http://github.com/moliware/solr_cli',
      install_requires=REQUIRED,
      classifiers=CLASSIFIERS,
      py_modules=['solr_cli'],
      test_suite='tests',
      entry_points={
        'console_scripts': [
            'solr_cli = solr_cli:main',
        ]
    }
)

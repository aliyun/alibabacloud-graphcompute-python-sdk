#!/usr/bin/env python

import re
import sys
from os import path

try:
    from setuptools import setup,find_packages
except ImportError:
    from distutils.core import setup,find_packages

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.rst')) as f:
    readme = f.read()

install_requires=['gremlinpython>=3.4.2']

if sys.version_info < (3,2):
    install_requires += ['futures>=3.0.5']

setup(
    name='graphcompute',
    version='1.0.2',
    description='Aliyun GraphCompute Python SDK',
    long_description=readme,
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    url='https://www.aliyun.com/product/graphcompute',
    license='Apache License 2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ]
)

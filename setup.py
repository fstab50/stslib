"""

stslib :  Copyright 2017 Blake Huber

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

see: https://www.gnu.org/licenses/#GPL

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
contained in the program LICENSE file.

"""

import os
import sys
from setuptools import setup, find_packages
from subprocess import check_call
from codecs import open
import stslib


def read(fname):
    basedir = os.path.dirname(sys.argv[0])
    return open(os.path.join(basedir, fname)).read()


basedir = os.path.dirname(sys.argv[0])

requires = [
    'awscli>=1.14.1',
    'boto3>=1.7.1',
    'pytz>=2017.1',
]

setup(
    name='stslib',
    version=stslib.__version__,
    description='Library for bulk generation of Amazon STS temporary credentials',
    long_description=read('DESCRIPTION.rst'),
    url='https://github.com/fstab50/stslib',
    author=stslib.__author__,
    author_email=stslib.__email__,
    license='GPL-3.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux'
    ],
    keywords='Amazon Web Services iam credentials AWS access key secret key',
    packages=find_packages(exclude=['docs', 'tests*', 'notes']),
    install_requires=requires,
    python_requires='>=3.5, <4',
    zip_safe=False
)

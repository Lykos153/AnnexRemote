#!/usr/bin/env python3

# annexremote Setup
# Copyright (C) 2017 Silvio Ankermann
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of version 3 of the GNU General Public License as published by
# the Free Software Foundation
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
long_description= """Helper module to easily develop special remotes for git annex.
AnnexRemote handles all the protocol stuff for you, so you can focus on the remote itself.
It implements the complete external special remote protocol and fulfils all specifications regarding whitespaces etc.
Changes to the protocol are normally adopted within hours after they've been published without changing 
the interface for the remote."""

setup(
    name='annexremote',
    version='1.1.0',
    description='git annex special remotes made easy',
    long_description=long_description,
    url='https://github.com/Lykos153/AnnexRemote',
    author='Silvio Ankermann',
    author_email='silvio@booq.org',
    license='GPLv3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='git-annex remote',
    py_modules=["annexremote"],

    extras_require={
        'test': ['coverage'],
    },
)

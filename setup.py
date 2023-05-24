#!/usr/bin/env python
#
# Distutils setup script for retain
# ---------------------------------------------------------------------------

from setuptools import setup, find_packages
import retain

setup (
    name="retain",
    version=retain.__version__,
    description="Delete all but the specified files/directories",
    install_requires=[
        'click >= 8.0.0',
    ],
    packages=find_packages(),
    url=retain.__url__,
    license=retain.__license__,
    author=retain.__author__,
    author_email=retain.__email__,
    entry_points = {'console_scripts' : 'retain=retain:main'},
    classifiers = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)


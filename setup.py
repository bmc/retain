#!/usr/bin/env python
#
# Distutils setup script for retain
# ---------------------------------------------------------------------------

from setuptools import setup, find_packages
import re
import sys
import os
import retain

setup (name="retain",
       version=retain.__version__,
       description="Delete all but the specified files/directories",
       packages=find_packages(),
       url=retain.__url__,
       license=retain.__license__,
       author=retain.__author__,
       author_email=retain.__email__,
       entry_points = {'console_scripts' : 'retain=retain:main'})


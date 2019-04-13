#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
'''
retain - Command-line utility that removes all files except the ones
         specified on the command line.

Usage:
  retain --help
  retain [options] <filename>...

Options:
  --help                      This message.
  --directory <dir>, -d <dir> The directory to operate on [default: .]
  --no-exec, -n               Show what would be done, but do not actually
                              do it.
  --recursive, -r             Delete directories, too (recursively).
  --verbose, -v               Enable verbose messages
  --version                   Display version and exit.
'''

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

from docopt import docopt
import sys
import os
import stat
import shutil
from typing import Sequence

# Info about the module
__version__   = '1.3.0'
__author__    = 'Brian Clapper'
__email__     = 'bmc@clapper.org'
__url__       = 'http://github.com/bmc/retain'
__copyright__ = '© 2003-2019 Brian M. Clapper'
__license__   = 'BSD-style license'

# Package stuff

# ---------------------------------------------------------------------------
# Classes
# ---------------------------------------------------------------------------

class RetainException(Exception):
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value


class Verbose:
    def __init__(self, verbose: bool = False):
        self._verbose = verbose

    def println(self, msg: str):
        if self._verbose:
            sys.stderr.write(msg + "\n")

    def __call__(self, msg: str):
        self.println(msg)


class FileRetainer:

    def __init__(self, argv: Sequence[str]):
        self._parseParams(argv)
        self._verbose = Verbose(self._be_verbose)

    def retain(self):
        verbose = self._verbose

        verbose(f'Changing directory to "{self._dir}"')
        try:
            os.chdir(self._dir)

        except OSError as ex:
            raise RetainException(str(ex))

        for dir_file in os.listdir("."):
            self._process_file(dir_file)

    # -----------------------------------------------------------------------
    # Private Methods
    # -----------------------------------------------------------------------

    def _process_file(self, dir_file: str):
        verbose = self._verbose
        if dir_file in self._files:
            verbose(f'Retaining "{dir_file}"')
            return
        
        verbose(f'Deleting "{dir_file}"')
        if not self._no_exec:
            try:
                mode = os.stat(dir_file)[stat.ST_MODE]
                if stat.S_ISDIR(mode):
                    if not self._recursive:
                        sys.stderr.write(f'Skipping directory "{dir_file}"')
                    else:
                        shutil.rmtree(dir_file)
                else:
                    os.unlink(dir_file)
        
            except OSError as ex:
                print(f'Warning: Cannot delete "{dir_file}": {ex}',
                      file=sys.stderr)


    def _parseParams(self, argv):
        # Parse the command-line parameters

        opts = docopt(__doc__, version=__version__)
        self._files = opts["<filename>"]

        self._no_exec    = opts["--no-exec"]
        self._be_verbose = opts["--verbose"]
        self._recursive  = opts["--recursive"]
        self._dir        = opts["--directory"] or "."

        if self._no_exec:
            self._verbose = True

# ---------------------------------------------------------------------------
# Main Program
# ---------------------------------------------------------------------------

def main():

    try:
        retainer = FileRetainer(sys.argv)
        retainer.retain()

    except RetainException as ex:
        sys.stderr.write(str (ex) + "\n")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()

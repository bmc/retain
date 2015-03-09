#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
'''
retain - Command-line utility that removes all files except the ones
         specified on the command line.

Usage:
------

retain [-fnrsv] [-d directory] filename [...]


Options:
--------

--directory <dir>   The directory to operate on. Defaults to the current
-d <dir>            directory

--force, -f         Do not ask for confirmation if file to retain          

--no-exec, -n       Show what would be done, but do not actually do it (implies -v)

--recursive, -r     Delete directories, too (recursively)

"--safe, -s         If a file is not found, program exits, nothing is deleted (overrides any previous -f option)",

--verbose, -v       Enable verbose messages


Description:
------------

retain is the opposite of "rm" or "del": It takes a series of file names on
the command line, and it deletes all files in the specified directory except
the specified files.


Copyright and License:
----------------------

Copyright © 2008 Brian M. Clapper

This is free software, released under the following BSD-like license:

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. The end-user documentation included with the redistribution, if any,
   must include the following acknowlegement:

      This product includes software developed by Brian M. Clapper
      (bmc@clapper.org, http://www.clapper.org/bmc/). That software is
      copyright © 2008 Brian M. Clapper.

    Alternately, this acknowlegement may appear in the software itself, if
    and wherever such third-party acknowlegements normally appear.

THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESSED OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL BRIAN M. CLAPPER BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 
'''

# $Id$

# Info about the module
__version__   = '2.0.0'
__author__    = 'Brian Clapper'
__email__     = 'bmc@clapper.org'
__url__       = 'http://github.com/bmc/retain'
__copyright__ = '© 2003-2011 Brian M. Clapper'
__license__   = 'BSD-style license'

# Package stuff

__all__     = ["retain"]

# Use the built-in 'set' type if using Python 2.4 or better. Otherwise, use
# the old sets module.
try:
    set
except NameError:
    from sets import Set as set, ImmutableSet as frozenset

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

from getopt import getopt, GetoptError
import string
import sys
import os
from sets import Set
import stat
import shutil

# ---------------------------------------------------------------------------
# Classes
# ---------------------------------------------------------------------------

class RetainException(Exception):
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return `self.__value`

    def get_value(self):
        return self.__value

    value = property(get_value, doc="Get the string for the exception")

class RetainUsageException(RetainException):
    def __init__(self, value):
        RetainException.__init__(self, value)

class Verbose:
    def __init__(self, verbose=0):
        self.__verbose = verbose

    def println(self, msg):
        if self.__verbose:
            sys.stderr.write(msg + "\n")

    def __call__(self, msg):
        self.println(msg)

class FileRetainer:

    def __init__(self, argv):
        self.__parseParams(argv)
        self.__verbose = Verbose(self.__verbose)

    def retain(self):
        verbose = self.__verbose

        verbose("Changing directory to " + self.__dir)
        try:
            os.chdir(self.__dir)

        except OSError, ex:
            raise RetainException(str(ex))

        for dirFile in os.listdir("."):
            self.__process_file(dirFile)

    # -----------------------------------------------------------------------
    # Private Methods
    # -----------------------------------------------------------------------

    def __process_file(self, dirFile):
        verbose = self.__verbose
        if dirFile in self.__files:
            verbose("Retaining " + dirFile)
            return
        
        verbose("Deleting " + dirFile)
        if not self.__no_exec:
            try:
                mode = os.stat(dirFile)[stat.ST_MODE]
                if stat.S_ISDIR(mode):
                    if not self.__recursive:
                        sys.stderr.write("Skipping directory \"" +
                                         dirFile +
                                         "\" because -r (--recursive) " +
                                         "was not specified.\n");
                    else:
                        shutil.rmtree(dirFile)
                else:
                    os.unlink(dirFile)
        
            except OSError, ex:
                sys.stderr.write("Warning: Can't unlink \"" + dirFile +
                                 "\": " + str (ex) + "\n")
    def __parseParams(self, argv):
        # Parse the command-line parameters

        try:
            opts, args = getopt(argv[1:],
                                "nvrfsd:",
                                ["directory=",
                                 "no-exec",
                                 "recursive",
                                 "verbose",
                                 "force",
                                 "safe"])
        except GetoptError, ex:
            self.__usage(argv[0], str (ex))   # throws an exception

        self.__no_exec   = 0
        self.__verbose   = 0
        self.__recursive = 0
        self.__force     = 0
        self.__safe      = 0
        self.__dir       = "."

        for o, a in opts:
            if o in ("--no-exec", "-n"):
                self.__no_exec = 1
                self.__verbose = 1
                continue

            if o in ("--verbose", "-v"):
                self.__verbose = 1
                continue

            if o in ("--directory", "-d"):
                self.__dir = a
                continue

            if o in ("--recursive", "-r"):
                self.__recursive = 1
                continue

            if o in ("--force", "-f"):
                self.__force = 1
                self.__safe = 0
                continue

            if o in ("--safe", "-s"):
                self.__safe = 1
                self.__force = 0
                continue
        
        files = []
        if len(args) > 0:
            self.__files = set(args[0:])
            
            if not self.__force:
                self.__checkFiles(self.__files)
        else:
            self.__usage(argv[0], "Missing file(s) to retain.")


    def __checkFiles(self, files):
        for fname in files:
            if self.__dir != ".":
                fpath = self.__dir + os.path.sep + fname
            else:
                fpath = fname

            if not (os.path.isfile(fpath)) and not (self.__recursive and os.path.isdir(fpath)):
                if self.__safe:
                    raise RetainException, fpath + " not found, canceling execution."
                else:
                    answer = raw_input(fpath + " was not found, continue? (y/n)\n")
                    if answer.lower() != "y":
                        raise RetainException, "User canceled execution"

    def __usage(self, prog, msg):
        u = [
"",
"retain, version %s" % __version__,
"",
"Usage: %s [-fnrsv] [-d directory] filename [...]" % os.path.basename(prog),
"",
"Retain all the specified files, removing anything else.",
"",
"OPTIONS",
"",
"--directory <dir>",
"-d <dir>           Directory to operate on. Defaults to current directory",
"--force, -f         Do not ask for confirmation if file is not found (overrides any previous -s option)",          
"--no-exec, -n      Show what would be done, but don't really do it (implies -v)",
"--recursive, -r    Delete directories, too (recursively)",
"--safe, -s         If a file is not found, program exits, nothing is deleted (overrides any previous -f option)",
"--verbose, -v      Enable verbose messages"
            ]

        result = []

        if msg != None:
            result.append(msg)

        for i in range (len (u)):
            result.append(u[i])

        raise RetainUsageException, result

# ---------------------------------------------------------------------------
# Main Program
# ---------------------------------------------------------------------------

def main():

    try:
        retainer = FileRetainer(sys.argv)
        retainer.retain()

    except RetainUsageException, ex:
        for i in ex.value:
            sys.stderr.write(i + "\n")
        sys.exit(1)

    except RetainException, ex:
        sys.stderr.write(str (ex) + "\n")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()

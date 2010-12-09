# Introduction

*retain* is a command-line utility that removes all files except the ones
specified in its argument list. Conceptually, it's the opposite of
*rm* (or *del* on Windows).

# Usage

*retain* [OPTIONS] *filename* [...]

## Options

* `--directory`: The directory to operate on. Defaults to the current directory.
* `--no-exec` or `-n`: Show what would be done, but don't do it.
* `--recursive` or `-r`: Remove subdirectories, too (recursively).
* `--verbose` or `-v`: Display verbose messages

# Installation

The usual:

1. Unpack the tarball.
2. Change your directory to the resulting `retain-x.x.x` directory.
3. Run `python setup.py install`

# Author

Brian M. Clapper, [bmc@clapper.org](mailto:bmc@clapper.org)

# Copyright and License

Copyright &copy; 2008-2010 Brian M. Clapper.

*retain* is released under a BSD License. Please see the accompanying
License file.

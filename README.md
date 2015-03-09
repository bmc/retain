# Introduction

*retain* is a command-line utility that removes all files except the ones
specified in its argument list. Conceptually, it's the opposite of
*rm* (or *del* on Windows).

# Usage

*retain* [-fnrsv] [-d directory] *filename* [...]

## Options

* `--directory` or `-d`: The directory to operate on. Defaults to the current directory.
* `--force` or `-f`: Do not ask for confirmation if file is not found (overrides any previous `-s` option)
* `--no-exec` or `-n`: Show what would be done, but don't do it (implies `-v`).
* `--recursive` or `-r`: Remove subdirectories, too (recursively).
* `--safe` or `-s`: If a file is not found, program exits, nothing is deleted (overrides any previous `-f` option)
* `--verbose` or `-v`: Display verbose messages

# Installation

The usual:

1. Unpack the tarball.
2. Change your directory to the resulting `retain-x.x.x` directory.
3. Run `python setup.py install`

# Author

Brian M. Clapper, [bmc@clapper.org](mailto:bmc@clapper.org)

# Copyright and License

Copyright &copy; 2008-2011 Brian M. Clapper.

*retain* is released under a BSD License. Please see the accompanying
License file.

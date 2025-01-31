# Introduction

*retain* is a command-line utility that removes all files except the ones
specified in its argument list. Conceptually, it's the opposite of
*rm* (or *del* on Windows).

# Usage

*retain* [options] _<filename>_...

## Options

After installing `retain`, type

```
retain --help
```

to see the complete command line usage.

# Installation

Note: I'm currrently no longer publishing this to the Python package
index. Installation from source, though, is simple enough:

Clone this repo and `cd` into it. Then:

```shell
$ pip install build
$ python -m build
$ pip install dist/retain-1.3.0-py3-none-any.whl
```

(The version number might be slightly different.)

# Author

Brian M. Clapper, [bmc@clapper.org](mailto:bmc@clapper.org)

# Copyright and License

## Copyright and License

*retain* is copyright © 2003-2025 Brian M. Clapper.

Prior to version 1.1.0, *retain* was released under a 3-clause BSD license.
As of version 1.1.0 *retain* is released under the Apache Software License,
version 2.0. See [the license file](LICENSE.md) and
<https://www.apache.org/licenses/LICENSE-2.0> for more details.

#!/usr/bin/env python
"""
retain - Delete all files except the ones on the command line. Run with
         "--help" for complete details.
"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

import os
import shutil
import sys
from dataclasses import dataclass
from typing import Callable, Optional
from typing import Sequence as Seq

import click

# Info about the module
__version__ = "1.3.0"
__author__ = "Brian Clapper"
__email__ = "bmc@clapper.org"
__url__ = "https://github.com/bmc/retain"
__copyright__ = "2003-2023 Brian M. Clapper"
__license__ = "Apache Software License"

# ---------------------------------------------------------------------------
# Classes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Params:
    dry_run: bool
    verbose: bool
    recursive: bool
    keep_hidden: bool
    fail_early: bool
    files_to_keep: Seq[str]


# ---------------------------------------------------------------------------
# Internal Functions
# ---------------------------------------------------------------------------


def warn(msg: str, use_prefix: bool = True) -> None:
    if use_prefix:
        msg = f"WARNING: {msg}"

    print(msg, file=sys.stderr)


def process_file(
    file: str, params: Params, verbose: Callable[[str], None]
) -> None:
    """
    Assumes the current working directory is now params.directory,
    and processes one file within that directory.
    """

    if file in params.files_to_keep:
        verbose(f'Retaining "{file}".')
        return

    if params.keep_hidden and (file[0] == "."):
        verbose(f'Skipping hidden file "{file}".')
        return

    try:
        if os.path.isdir(file):
            if not params.recursive:
                warn(f'Skipping directory "{file}".', use_prefix=False)
            else:
                verbose(f'Recursively deleting directory "{file}"...')
                if not params.dry_run:
                    shutil.rmtree(file)
        else:
            verbose(f'Deleting file "{file}".')
            if not params.dry_run:
                os.unlink(file)

    except OSError as e:
        msg = f"""Can't delete "{file}": {e} """
        if params.fail_early:
            raise click.ClickException(msg)
        else:
            warn(msg)


def retain_files(params: Params) -> None:
    def _no_verbose(msg: str) -> None:
        pass

    def _verbose(msg: str) -> None:
        print(msg)

    verbose = _verbose if params.verbose else _no_verbose

    for file in os.listdir("."):
        # os.listdir() does not return "." or ".."
        process_file(file, params=params, verbose=verbose)


# ---------------------------------------------------------------------------
# Main Program
# ---------------------------------------------------------------------------


@click.command()
@click.option(
    "-D",
    "--keep-hidden",
    is_flag=True,
    help='Automatically retain all "hidden" files (i.e., files '
    'whose names start with ".").',
)
@click.option(
    "-e",
    "--fail-early",
    is_flag=True,
    help="Normally, if a deletion fails, retain prints a "
    "warning and keeps going. With this option, retain "
    "aborts the first time it fails to delete a file.",
)
@click.option(
    "-n",
    "--dry-run",
    "--no-exec",
    "--show-only",
    is_flag=True,
    help="Show what would be done, but don't actually do it."
    "Implies --verbose.",
)
@click.option(
    "-r",
    "--recursive",
    is_flag=True,
    help="Delete directories, too (recursively).",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Display what's being done as it's being done.",
)
@click.version_option(version=__version__)
@click.argument("file", nargs=-1, required=True)
def retain(
    dry_run: bool,
    recursive: bool,
    keep_hidden: bool,
    fail_early: bool,
    verbose: bool,
    file: Seq[str],
) -> None:
    """
    Remove all files except the ones specified on the command line. Think of
    "retain" as the opposite of "rm": It selectively keeps files, instead of
    selectively deleting them. (It's a great tool for cleaning up your
    "Downloads" directory, for instance.)

    Each FILE is assumed to be in the current directory; paths outside
    the current directory are skipped. That includes paths below the current
    directory. Currently "retain" won't allow you to delete all but some files
    in directories below the current directory. That is, something like this
    won't work:

    $ retain -r a b subdir/foo

    The intend of that command is to delete all files and directories in
    the current directory EXCEPT for "a" and "b", and to clean out subdirectory
    "subdir" except for "subdir/foo", not deleting "subdir".

    Currently, "retain" simply doesn't support that level of complexity.
    You can delete all but the specified files in the current directory,
    implicitly leaving subdirectories alone (no --recursive option specified);
    or, you can delete all but the specified files and directories in the
    current directory, deleting all other files and directories (--recursive
    specified.)
    """

    adjusted_files = []
    for f in file:
        parent_dir = os.path.dirname(f)
        if parent_dir in ("", "."):
            adjusted_files.append(f)
        else:
            warn(
                f"""Ignoring specified path "{f}": It's outside the """
                "current directory."
            )

    params = Params(
        dry_run=dry_run,
        recursive=recursive,
        keep_hidden=keep_hidden,
        fail_early=fail_early,
        verbose=verbose or dry_run,
        files_to_keep=adjusted_files,
    )
    retain_files(params)


if __name__ == "__main__":
    retain()

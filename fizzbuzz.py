#!/usr/bin/env python3

"""Standalone script example in Python.

The code for this script is contained in a single file and is
self-documented. With ``--help``, you can get the purpose of the
script as well as the options it accepts. You should put enough
documentation for other people, including your future self, to
understand the purpose of the script and how to invoke it.

Currently, this script is a simple fizzbuzz generator.

You can also run tests with::

    $ python3 -m pytest -v --log-level=debug --doctest-modules \
              --cov=fizzbuzz ./fizzbuzz.py
    $ python3 -m coverage html

To adapt this template to your needs, there are several steps:

 1. Rename this script to a proper name. The name have to end with
    ``.py`` if you want to include tests.

 2. Adapt command-line options in ``parse_args()``.

 3. Include your logic in ``main()`` (or in additional functions).

This file is released under the CC0-1.0 license (public domain).
"""

import argparse
import logging
import logging.handlers
import os
import sys

logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])


class CustomFormatter(argparse.RawDescriptionHelpFormatter,
                      argparse.ArgumentDefaultsHelpFormatter):
    pass


def parse_args(args=sys.argv[1:]):
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__,
        formatter_class=CustomFormatter)

    g = parser.add_mutually_exclusive_group()
    g.add_argument("--debug", "-d", action="store_true",
                   default=False,
                   help="enable debugging")
    g.add_argument("--silent", "-s", action="store_true",
                   default=False,
                   help="don't log")

    # TODO: modify these options
    g = parser.add_argument_group("fizzbuzz settings")
    g.add_argument("--fizz", metavar="N",
                   default=3,
                   type=int,
                   help="Modulo value for fizz")
    g.add_argument("--buzz", metavar="N",
                   default=5,
                   type=int,
                   help="Modulo value for buzz")

    parser.add_argument("start", type=int, help="Start value")
    parser.add_argument("end", type=int, help="End value")

    return parser.parse_args(args)


def setup_logging(options):
    """Configure logging."""
    root = logging.getLogger("")
    root.setLevel(logging.WARNING)
    logger.setLevel(options.debug and logging.DEBUG or logging.INFO)
    if not options.silent:
        if not sys.stderr.isatty():
            facility = logging.handlers.SysLogHandler.LOG_DAEMON
            sh = logging.handlers.SysLogHandler(address='/dev/log',
                                                facility=facility)
            sh.setFormatter(logging.Formatter(
                "{0}[{1}]: %(message)s".format(
                    logger.name,
                    os.getpid())))
            root.addHandler(sh)
        else:
            ch = logging.StreamHandler()
            ch.setFormatter(logging.Formatter(
                "%(levelname)s[%(name)s] %(message)s"))
            root.addHandler(ch)


def fizzbuzz(n, fizz, buzz):
    """Compute fizzbuzz nth item given modulo values for fizz and buzz.

    >>> fizzbuzz(5, fizz=3, buzz=5)
    'buzz'
    >>> fizzbuzz(3, fizz=3, buzz=5)
    'fizz'
    >>> fizzbuzz(15, fizz=3, buzz=5)
    'fizzbuzz'
    >>> fizzbuzz(4, fizz=3, buzz=5)
    4
    >>> fizzbuzz(4, fizz=4, buzz=6)
    'fizz'

    """
    if n % fizz == 0 and n % buzz == 0:
        return "fizzbuzz"
    if n % fizz == 0:
        return "fizz"
    if n % buzz == 0:
        return "buzz"
    return n


def main(options):
    """Compute a fizzbuzz set of strings and return them as an array."""
    logger.debug("compute fizzbuzz from {} to {}".format(options.start,
                                                         options.end))
    return [str(fizzbuzz(i,
                         fizz=options.fizz, buzz=options.buzz))
            for i in range(options.start, options.end+1)]


if __name__ == "__main__":
    options = parse_args()
    setup_logging(options)

    try:
        print("\n".join(main(options)))
    except Exception as e:
        logger.exception("%s", e)
        sys.exit(1)
    sys.exit(0)


# Unit tests
import pytest                   # noqa: E402
import shlex                    # noqa: E402


@pytest.mark.parametrize("args, expected", [
    ("0 0", ["fizzbuzz"]),
    ("3 5", ["fizz", "4", "buzz"]),
    ("9 12", ["fizz", "buzz", "11", "fizz"]),
    ("14 17", ["14", "fizzbuzz", "16", "17"]),
    ("14 17 --fizz=2", ["fizz", "buzz", "fizz", "17"]),
    ("17 20 --buzz=10", ["17", "fizz", "19", "buzz"]),
])
def test_main(args, expected):
    options = parse_args(shlex.split(args))
    assert main(options) == expected

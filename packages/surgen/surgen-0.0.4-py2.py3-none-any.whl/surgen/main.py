"""surgen, a codebase upgrade tool

Usage:
  surgen [-d -i -v <procedure_dir> <target_dir>]

Options:
  <procedure_dir>         the directory containing surgen procedure files [default: ./procedures/]
  <target_dir>            the directory to operate on. [default: .]
  -d, --dry-run           skips execution if provided
  -i, --ignore-errors     continues if a procedure fails
  -v, --verbose           show verbose output
  -h, --help              show this usage guide
"""
import os
import docopt
import logging
import sys
from .surgen import Surgen, surgen_from_directory

DEFAULT_PROCEDURE_DIR = os.path.join(os.curdir, "surgen_procedures")
DEFAULT_TARGET_DIR = os.curdir

def main(argv=sys.argv[1:]):
    options = docopt.docopt(__doc__,  argv=argv, options_first=True)
    level = logging.DEBUG if options["--verbose"] else logging.INFO
    s = surgen_from_directory(options.get("<procedure_dir>") or DEFAULT_PROCEDURE_DIR)
    return s.operate(options.get("<target_dir>") or DEFAULT_TARGET_DIR,
                     options["--ignore-errors"], options["--dry-run"])

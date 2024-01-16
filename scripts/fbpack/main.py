"""Flipbook Packer
This module is the main entry point for the Flipbook Packer application when used with the command line interface.
There are `bat` files found in the `../../bin` directory that can be used to run this module from a Windows terminal.
"""
import sys
import logging
import argparse
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))
from fbpack import layout

__all__: list[str] = []


_logger: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


parser: argparse.ArgumentParser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", required=True, type=str, help="absolute path to the image files.")
parser.add_argument("-t", "--type", type=str, default="atlas", help="the type of atlas to generate. available types are `atlas`, `stagger`, and `super`.")
parser.add_argument("-r", "--rows", type=int, help="the number of rows in the atlas. this is a required flag if using type `atlas`.")
parser.add_argument("-c", "--cols", type=int, help="the number of rows in the atlas. this is a required flag if using type `atlas`.")

args: argparse.Namespace = parser.parse_args()

source_path: Path = Path(args.path)

if not source_path.exists():
    _logger.error(f"the specified source path does not exist - {source_path.absolute()}")
    raise ValueError("the specified source path does not exist.")

if args.type == "atlas":
    if args.rows is None or args.cols is None:
        raise ValueError("the number of rows and columns must be specified when generating an atlas. please use the `-r` and `-c` flags to set the rows and columns after the type.")
    layout.traditional_atlas(args.rows, args.cols, source_path)

elif args.type == "stagger":
    layout.stagger_packed_atlas(source_path)

elif args.type == "super":
    layout.super_packed_atlas(source_path)

else:
    raise ValueError(f"the specified type is not supported - {args.type}")

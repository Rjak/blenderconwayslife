# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

"""Run GOL from the command line."""

import argparse
import os
import sys

from goldriver import GOLDriver


DEFAULT_CONFIG_PATH = './golconfig.cfg'


def parse_args():
    parser = argparse.ArgumentParser()
    help_msg = f"optional config file path (defaults to {DEFAULT_CONFIG_PATH})"
    parser.add_argument("--config", help=help_msg, default=DEFAULT_CONFIG_PATH)
    return parser.parse_args()


def main(parsed_args):
    cfg_path = parsed_args.config
    if not os.path.exists(cfg_path):
        sys.exit(f"config file {cfg_path} not found")

    driver = GOLDriver(cfg_path)
    driver.go()


if __name__ == '__main__':
    args = parse_args()
    main(args)

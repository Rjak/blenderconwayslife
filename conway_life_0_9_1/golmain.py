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
import os
import sys

from goldriver import GOLDriver

"""Used only to run GOL from the command line."""


def usage():
    print("usage: python %s <config file>")
    print("where:")
    print("\tconfig file - optional config file (defaults to golconfig.cfg)")
    sys.exit("invalid arguments")

driver = None

if len(sys.argv) <= 1:
    driver = GOLDriver()
elif len(sys.argv) == 2:
    cfg_path = sys.argv[1]
    if not os.path.exists(cfg_path):
        sys.exit("config file {} not found".format(cfg_path))
    driver = GOLDriver(cfg_path)
else:
    usage()

driver.go()

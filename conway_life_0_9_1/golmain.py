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
import random
import time

from goldriver import GOLDriver

#
# Interesting Random Seeds
#
# 9743119 - Goes to 1200, gliders, oscillators, blooms
# 716382 - Orig, interesting
# 18264181563811 - Very busy up to 700, no gliders
GOL_SEED = 12
random.seed(GOL_SEED)

driver = GOLDriver()
driver.go()

#!/usr/bin/python
#
#       Copyright (C) 2014 Stephen M. Cameron
#       Author: Stephen M. Cameron
#
#       This file is part of mister-nouveau-artboto.
#
#       mister-nouveau-artboto is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       mister-nouveau-artboto is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with mister-nouveau-artboto; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

import sys
import Image
import math

xdim = 2048;
ydim = 1024;

outputimg = Image.new("RGB", (xdim, ydim));

for x in range(0, int(xdim)):
   for y in range(0, int(ydim)):
      outputimg.putpixel((x, y), (255, 255, 255));

outputimg.save("output.png");


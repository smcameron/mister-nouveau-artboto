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
import ImageDraw
import math
import random

xdim = 2048;
ydim = 1024;
maxspeed = 0.10;
minspeed = 0.001;
maxpenwidth = xdim / 30;
minpenwidth = xdim / 400;

outputimg = Image.new("RGB", (xdim, ydim));
draw = ImageDraw.Draw(outputimg);

def clear_image():
   for x in range(0, int(xdim)):
      for y in range(0, int(ydim)):
         outputimg.putpixel((x, y), (255, 255, 255));

class pen:
   def __init__(self):
      self.x = random.random() * xdim;
      self.y = 1.0 * ydim;
      self.direction = 90 * math.pi / 180.0;
      self.direction += (((random.random() * 2.0) - 1.0) * 10 * math.pi / 180.0);
      self.speed = random.random() * (maxspeed - minspeed) + minspeed;
      self.angle = (((random.random() * 2.0) - 1.0) * 30 * math.pi / 180.0);
      self.width = random.random() * random.random() * (maxpenwidth - minpenwidth) + minpenwidth;

   def move(self):
      self.x = self.x + math.cos(self.direction) * self.speed;
      self.y = self.y - math.sin(self.direction) * self.speed;

   def paint(self):
      x1 = self.x + math.cos(self.angle) * self.width / 2.0;
      y1 = self.y + math.sin(self.angle) * self.width / 2.0;
      x2 = self.x - math.cos(self.angle) * self.width / 2.0;
      y2 = self.y - math.sin(self.angle) * self.width / 2.0;
      draw.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=0);

clear_image();

for i in range(20):
   p = pen();
   for j in range(45000):
      p.move();
      p.paint();

outputimg.save("output.png");


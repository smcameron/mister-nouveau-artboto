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
from PIL import \
    Image, \
    ImageDraw
import math
import random

xdim = 2048;
ydim = 1024;
maxspeed = 0.10;
minspeed = 0.001;
maxpenwidth = xdim / 30;
minpenwidth = xdim / 400;
maxangspeed = 0.10 * math.pi / 180.0;
maxangaccel = maxangspeed / 10.0;
brightfactor = 1.5;

outputimg = Image.new("RGB", (xdim, ydim));
draw = ImageDraw.Draw(outputimg);

def choose_colors():
   d = 0.2;
   fr = random.random() * d;
   fg = random.random() * d;
   fb = random.random() * d;
   lr = fr + random.random() *  ((1.0 - d) * 0.99);
   lg = fg + random.random() *  ((1.0 - d) * 0.99);
   lb = fb + random.random() *  ((1.0 - d) * 0.99);
   return (fr * 255, fg * 255, fb * 255), (lr * 255, lg * 255, lb * 255);

def brighten_color(rgb):
   (r, g, b) = rgb
   r = int(min(brightfactor * r, 255));
   g = int(min(brightfactor * g, 255));
   b = int(min(brightfactor * b, 255));
   return (r, g, b);

def clear_image():
   for x in range(0, int(xdim)):
      for y in range(0, int(ydim)):
         outputimg.putpixel((x, y), (255, 255, 255));

def paintpixel(xy, rgb):
   (x, y) = xy
   (r, g, b) = rgb
   if (x >= 0 and x < xdim and y >= 0 and y < ydim):
      outputimg.putpixel((x, y), (r, g, b));

class pen:
   def __init__(self):
      self.x = random.random() * xdim;
      self.y = 1.0 * ydim;
      self.direction = 90 * math.pi / 180.0;
      self.direction += (((random.random() * 2.0) - 1.0) * 10 * math.pi / 180.0);
      if (random.random() < 0.5):
         self.direction += math.pi;
         self.y = 0;
      self.speed = random.random() * (maxspeed - minspeed) + minspeed;
      self.angle = (((random.random() * 2.0) - 1.0) * 30 * math.pi / 180.0);
      self.width = random.random() * random.random() * (maxpenwidth - minpenwidth) + minpenwidth;
      self.angularspeed = ((random.random() * 2.0) - 1.0) * maxangspeed;
      self.angularaccel = ((random.random() * 2.0) - 1.0) * maxangaccel;

   def move(self):
      self.x = self.x + math.cos(self.direction) * self.speed;
      self.y = self.y - math.sin(self.direction) * self.speed;
      self.direction += self.angularspeed;
      self.angularspeed += self.angularaccel;
      if (self.angularspeed < -maxangspeed and self.angularaccel < 0.0):
         self.angularspeed = -maxangspeed;
         self.angularaccel = ((random.random() * 2.0) - 1.0) * maxangaccel;
      if (self.angularspeed > maxangspeed and self.angularaccel > 0.0):
         self.angularspeed = maxangspeed;
         self.angularaccel = ((random.random() * 2.0) - 1.0) * maxangaccel;

   def paint(self):
      x1 = self.x + math.cos(self.angle) * self.width / 2.0;
      y1 = self.y + math.sin(self.angle) * self.width / 2.0;
      x2 = self.x - math.cos(self.angle) * self.width / 2.0;
      y2 = self.y - math.sin(self.angle) * self.width / 2.0;
      draw.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=0);
      paintpixel((int(x1), int(y1)), (0, 255, 0));
      paintpixel((int(x2), int(y2)), (0, 255, 0));
      x1 = xdim - x1;
      x2 = xdim - x2;
      draw.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=0);
      paintpixel((int(x1), int(y1)), (0, 255, 0));
      paintpixel((int(x2), int(y2)), (0, 255, 0));

def sample_gradient(y, frgb, lrgb):
   (fr, fg, fb) = frgb
   (lr, lg, lb) = lrgb
   r = (float(y) / float(ydim)) * (float(lr) - float(fr)) + float(fr);
   g = (float(y) / float(ydim)) * (float(lg) - float(fg)) + float(fg);
   b = (float(y) / float(ydim)) * (float(lb) - float(fb)) + float(fb);

   return (int(r), int(g), int(b));

clear_image();

for i in range(20):
   p = pen();
   for j in range(45000):
      p.move();
      p.paint();

firstcolor, lastcolor = choose_colors();

for x in range(xdim):
   for y in range(ydim):
      r, g, b = outputimg.getpixel((x, y));
      if (r == 255):
         r, g, b = sample_gradient(y, firstcolor, lastcolor);
      else:
         if (g == 255):
            if (y < ydim / 2.0):
               r, g, b = brighten_color(sample_gradient(y, lastcolor, firstcolor));
            else:
               r, g, b = brighten_color(sample_gradient(y, firstcolor, lastcolor));
         else:
            r, g, b = sample_gradient(y, lastcolor, firstcolor);
      outputimg.putpixel((x, y), (r, g, b));

outputimg.save("output.png");


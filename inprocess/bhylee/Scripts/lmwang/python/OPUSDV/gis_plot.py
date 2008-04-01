#
#  UrbanSim software.
#  Copyright (C) 1998-2004 University of Washington
#  
#  You can redistribute this program and/or modify it under the
#  terms of the GNU General Public License as published by the
#  Free Software Foundation (http://www.gnu.org/copyleft/gpl.html).
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  file LICENSE.htm for copyright and licensing information, and the
#  file ACKNOWLEDGMENTS.htm for funding and other acknowledgments.
#
#  Author: Paul Waddell
#  Date: August 24, 2004


from matplotlib.matlab import *
from numarray import *
from string import *
file = "c:\gis\honolulu\export\demoahu"
input = open(file+".hdr")
info = input.readlines()

for record in info:
    if record.startswith("ncols"):
        ncols = split(record)
        maxy = int(ncols[1])
    if record.startswith("nrows"):
        nrows = split(record)
        maxx = int(nrows[1])

#print maxx, maxy

grid = fromfile(file+".flt", Float32, (maxx,maxy))
grid2 = transpose(grid)
jet()
im = imshow(grid,origin='upper')
axis('off')
savefig('grid_plot', dpi=120)
show()


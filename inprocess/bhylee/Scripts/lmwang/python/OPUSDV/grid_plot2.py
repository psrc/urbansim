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

from numarray import *
import time
import MySQLdb
from matplotlib.matlab import *
from numarray import nd_image

starttime = time.clock()
Con = MySQLdb.connect(host="trondheim.cs.washington.edu",port=3306,
    user="******", passwd="******",db="PSRC_2000_baseyear")
Cursor = Con.cursor()
sql = "SELECT GRID_ID,RESIDENTIAL_UNITS,RELATIVE_X,RELATIVE_Y FROM gridcells"
Cursor.execute(sql)
a = array(Cursor.fetchall())
Con.close
#print a
size = max(a,axis=0)
print 'maxx= ', size[2], 'maxy= ',size[3]
extent = 0, size[2], 0, size[3]

grid = zeros((size[2]+1,size[3]+1))
print 'grid= ',grid
x = a[:,2]
y = a[:,3]
z = a[:,1]
grid[x,y] = z
grid2 = transpose(grid/.99999)
endtime = time.clock()
elapsedtime = endtime-starttime
print 'Generating a grid from the database with', size[2]*size[3], 'cells took', elapsedtime, 'seconds.'
starttime = time.clock()

jet()
im = imshow(grid2,origin='upper',extent=extent)
axis('off')
savefig('grid_plot', dpi=120)
show()
endtime = time.clock()
elapsedtime = endtime-starttime
print 'Displaying the grid image took', elapsedtime, 'seconds.'


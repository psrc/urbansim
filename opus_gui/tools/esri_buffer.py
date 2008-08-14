#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

import os, sys, arcgisscripting


def opusRun(progressCB,logCB,params):

    gp = arcgisscripting.create()

    my_dict = {}
    for key, val in params.iteritems():
        my_dict[str(key)] = str(val)

    input = my_dict['input_shapefile']
    output = my_dict['output_shapefile']
    buffer = my_dict['buffer_size']

    print "Executing buffer"
    gp.buffer(input, output, buffer)
    print "Finised buffer"

def opusHelp():
    help = 'This is a very basic buffer tool using the ESRI geoprocessing framework.\n' \
           '\n' \
           'The input and output parameters will accept paths to shapefiles (c:\\test.shp), ' \
           'personal or file geodatabase feature classes (c:\\test.gdb\\test_fc or c:\\test.mdb\\test_fc), ' \
           'or SDE feature classes (Database Connections\\Your Database Connection.sde\\your feature class).\n' \
           '\n' \
           'input_shapefile: path to the input shapefile or feature class\n' \
           'output_shapefile: path to the output shapefile or feature class\n' \
           'buffer_size: buffer size in the units that the shapefile or feature class is in\n'
    return help



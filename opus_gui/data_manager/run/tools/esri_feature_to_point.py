# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys
import imp

def opusRun(progressCB,logCB,params):
    f, filename, description = imp.find_module('arcgisscripting', ['c:/Python25/Lib/site-packages'])
    arcgisscripting = imp.load_module('arcgisscripting', f, filename, description)

    gp = arcgisscripting.create()

    my_dict = {}
    for key, val in params.iteritems():
        my_dict[str(key)] = str(val)

    input = my_dict['in_features']
    output = my_dict['out_features']


    logCB("Executing feature to point\n")
    gp.FeatureToPoint_management (input, output)
    logCB("Finised feature to point\n")

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



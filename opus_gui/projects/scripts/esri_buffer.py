#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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





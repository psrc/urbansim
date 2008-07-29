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

import os, sys, subprocess

def opusRun(progressCB,logCB,params):
    my_dict = {}
    for key, val in params.iteritems():
        my_dict[str(key)] = str(val)
    
    dbname = my_dict['dbname']
    schema = my_dict['schema_name']
    shapefile = my_dict['shapefile_path']
    table_name = my_dict['output_table_name']
    host = os.environ['POSTGRESHOSTNAME']
    user = os.environ['POSTGRESUSERNAME']
    password = os.environ['POSTGRESPASSWORD']
    ogr2ogr_cmd = 'ogr2ogr -f PostgreSQL PG:"host=%s user=%s dbname=%s password=%s" %s -lco PRECISION=NO -nln %s.%s' \
                    % (host, user, dbname, password, shapefile, schema, table_name)
    print ogr2ogr_cmd

    p = subprocess.Popen((ogr2ogr_cmd),
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    stdout_text, stderr_text = p.communicate()

    print stdout_text
    print '================================'
    print stderr_text    

    



    
    
    
    
    
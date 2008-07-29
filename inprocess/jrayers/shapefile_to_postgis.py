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
    
    dbname = my_dict['Database Name']
    schema = my_dict['Schema Name']
    shapefile = my_dict['Shapefile Path']
    table_name = my_dict['Table Name']
    host = os.environ['POSTGRESHOSTNAME'] #'trondheim.cs.washington.edu'
    user = os.environ['POSTGRESUSERNAME'] #'urbansim'
    password = os.environ['POSTGRESPASSWORD'] #'Urbo**sauR' 
    overwrite = my_dict['Overwrite']

    if overwrite:
        overwrite_option = '-overwrite'
    else:
        overwrite_option = ''

    ogr2ogr_cmd = 'ogr2ogr -f PostgreSQL PG:"host=%s user=%s dbname=%s password=%s" %s -lco PRECISION=NO SCHEMA=%s %s -nln %s' \
                    % (host, user, dbname, password, shapefile, schema, overwrite_option, table_name)
    p = subprocess.Popen((ogr2ogr_cmd),
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    stdout_text, stderr_text = p.communicate()

    print stdout_text
    print '================================'
    print stderr_text    

    



    
    
    
    
    
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


import os, sys, string
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core.database_management.opus_database import OpusDatabase

def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)
        
    
    # get parameter values
    db_connection = param_dict['database_server_connection']
    database_name = param_dict['database_name']
    path = param_dict['path']
    
    dbs_config = DatabaseServerConfiguration(database_configuration=db_connection)
    opus_db = OpusDatabase(database_server_configuration=dbs_config, database_name=database_name)

    #create database if it doesn't already exist
    
    opus_db.DoQuery('''Create Table housing_pums ( pumano int, hhpumsid int,
                                   hhid int, hhtype int, 
                                   childpresence int, hhldtype int, 
                                   hhldsize int, hhldinc int,
                                   groupquarter int )''')
    opus_db.DoQuery('''load data local infile '%s/housing_pums.dat' into table housing_pums'''%(path))
    
    opus_db.DoQuery('''Create Table person_pums ( pumano int, hhpumsid int,
                                  hhid int, personid int,
                                  gender int, age int, 
                                  race int, employment int )''')
    opus_db.DoQuery('''load data local infile '%s/person_pums.dat' into table person_pums''' %(path))

    opus_db.DoQuery('''Create Table housing_marginals ( county int, pumano int,
                                         tract int, bg int,
                                         hhtotal int, childpresence1 int,
                                         childpresence2 int, hhldtype1 int,
                                         hhldtype2 int, hhldtype3 int,
                                         hhldtype4 int, hhldtype5 int,
                                         hhldsize1 int, hhldsize2 int,
                                         hhldsize3 int, hhldsize4 int,
                                         hhldsize5 int, hhldsize6 int,
                                         hhldsize7 int, hhldinc1 int,
                                         hhldinc2 int, hhldinc3 int,
                                         hhldinc4 int, hhldinc5 int,
                                         hhldinc6 int, hhldinc7 int,
                                         hhldinc8 int, groupquarter1 int, 
                                         groupquarter2 int )''')
    opus_db.DoQuery('''load data local infile '%s/housing_marginals.dat' into table housing_marginals'''%(path))

    opus_db.DoQuery('''Create Table person_marginals ( county int, pumano int,
                                        tract int, bg int,
                                        gender1 int, gender2 int,
                                        age1 int, age2 int, 
                                        age3 int, age4 int, 
                                        age5 int, age6 int, 
                                        age7 int, age8 int, 
                                        age9 int, age10 int, 
                                        race1 int, race2 int, 
                                        race3 int, race4 int, 
                                        race5 int, race6 int, 
                                        race7 int, employment1 int,
                                        employment2 int, employment3 int,
                                        employment4 int )''')
    opus_db.DoQuery('''load data local infile '%s/person_marginals.dat' into table person_marginals'''%(path))
# Figure out a way to automate this process based on the number of hhtypes and the independent tables must only contain variables corresponding 
# to the particular housing type
    hhld_variables = 'childpresence, hhldtype, hhldsize, hhldinc'
    gq_variables = 'groupquarter'
    opus_db.DoQuery('''create table hhld_pums select pumano, hhpumsid, hhid, %s from housing_pums where hhtype = 1'''%(hhld_variables))
    opus_db.DoQuery('''create table gq_pums select pumano, hhpumsid, hhid, %s from housing_pums where hhtype = 2'''%(gq_variables))
    #dbc.close()
    #db.commit()
    #db.close()

    opus_db.close()
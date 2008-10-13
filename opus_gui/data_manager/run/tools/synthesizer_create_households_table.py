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

import os, sys
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core.database_management.opus_database import OpusDatabase

def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.iteritems():
        param_dict[str(key)] = str(val)
        
    
    # get parameter values
    database_name = param_dict['database_name']
    database_server_connection = param_dict['database_server_connection']
    raw_pums_households_table_name = param_dict['raw_pums_households_table_name']
            
    query1 = """
            create table hh_temp
            select PUMA5, 0 as pumano,
                   SERIALNO, 0 as hhpumsid,
                   UNITTYPE, 0 as hhtype,
                   NOC, 0 as childpresence,
                   HHT, 0 as hhldtype,
                   PERSONS, 0 as hhldsize,
                   HINC, 0 as hhldinc,
                   0 as groupquarter
            from %s;
            
            update hh_temp
            set pumano = PUMA5,
            hhpumsid = SERIALNO;
            
            update hh_temp
            set hhtype = 1
            where UNITTYPE = 0;
            
            update hh_temp
            set hhtype = 2
            where UNITTYPE = 1 or UNITTYPE = 2;
            
            update hh_temp
            set childpresence = 1
            where NOC <> '00';
            
            update hh_temp
            set childpresence = 2
            where NOC = '00';
            
            update hh_temp
            set childpresence = -99
            where hhtype = 2;
            
            update hh_temp
            set hhldtype = 1
            where HHT = 1;
            
            update hh_temp
            set hhldtype = 2
            where HHT = 2;
            
            update hh_temp
            set hhldtype = 3
            where HHT = 3;
            
            update hh_temp
            set hhldtype = 4
            where HHT = 4 or HHT = 6;
            
            update hh_temp
            set hhldtype = 5
            where HHT = 5 or HHT = 7;
            
            update hh_temp
            set hhldtype = -99
            where hhtype = 2;
            
            update hh_temp
            set hhldsize = 1
            where persons = '01';
            
            update hh_temp
            set hhldsize = 2
            where persons = '02';
            
            update hh_temp
            set hhldsize = 3
            where persons = '03';
            
            update hh_temp
            set hhldsize = 4
            where persons = '04';
            
            update hh_temp
            set hhldsize = 5
            where persons = '05';
            
            update hh_temp
            set hhldsize = 6
            where persons = '06';
            
            update hh_temp
            set hhldsize = 7
            where cast(persons as signed) >= 7;
            
            update hh_temp
            set hhldsize = -99
            where hhtype = 2;
            
            update hh_temp
            set hhldinc = 1
            where cast(HINC as signed) <= 14999;
            
            update hh_temp
            set hhldinc = 2
            where (cast(HINC as signed) >= 15000) AND (cast(HINC as signed) <= 24999);
            
            update hh_temp
            set hhldinc = 3
            where (cast(HINC as signed) >= 25000) AND (cast(HINC as signed) <= 34999);
            
            update hh_temp
            set hhldinc = 4
            where (cast(HINC as signed) >= 35000) AND (cast(HINC as signed) <= 44999);
            
            update hh_temp
            set hhldinc = 5
            where (cast(HINC as signed) >= 45000) AND (cast(HINC as signed) <= 59999);
            
            update hh_temp
            set hhldinc = 6
            where (cast(HINC as signed) >= 60000) AND (cast(HINC as signed) <= 99999);
            
            update hh_temp
            set hhldinc = 7
            where (cast(HINC as signed) >= 100000) AND (cast(HINC as signed) <= 149999);
            
            update hh_temp
            set hhldinc = 8
            where cast(HINC as signed) >= 150000;
            
            update hh_temp
            set hhldinc = -99
            where hhtype = 2;
            
            update hh_temp
            set groupquarter = 1
            where UNITTYPE = 1;
            
            update hh_temp
            set groupquarter = 2
            where UNITTYPE = 2;
            
            update hh_temp
            set groupquarter = -99
            where UNITTYPE = 0;
            """ % (raw_pums_households_table_name)
    query2 = """
            create table housing_pums
            select pumano, hhpumsid,hhtype, childpresence, hhldtype, hhldsize, hhldinc, groupquarter
            from hh_temp;
            
            ALTER TABLE housing_pums ADD COLUMN hhid INTEGER NOT NULL AUTO_INCREMENT AFTER hhpumsid, add primary key (hhid);
            """  
            
    # create engine and connection
    logCB("Openeing database connection\n")
    dbs_config = DatabaseServerConfiguration(database_configuration=database_server_connection)
    opus_db = OpusDatabase(database_server_configuration=dbs_config, database_name=database_name)

    # Do Query       
    logCB("Running 1st set of queries...\n")
    opus_db.DoQuery(query1)
    logCB("Running 2nd set of queries...\n")
    opus_db.DoQuery(query2)
    
    # Finish up
    logCB("Closing database connection\n")
    opus_db.close()
    logCB('Finished running queries\n')
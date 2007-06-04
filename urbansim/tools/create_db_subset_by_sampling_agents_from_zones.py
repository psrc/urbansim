#
# Opus software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.store.scenario_database import ScenarioDatabase
import os
import sys
import MySQLdb
from opus_core.logger import logger

class GenerateDBSubsetBySamplingAgentsFromZones(object):
    def make_database_subset(self, proportion=1.0):
        con = ScenarioDatabase(hostname = DB_server_settings.db_host_name,
                               username = DB_server_settings.db_user_name, 
                               password = DB_server_settings.db_password,
                               database_name = DB_settings.input_database_name)
               
        number_of_households = con.GetResultsFromQuery("""select count(*) from $$.households""")[1][0]       
        number_of_gridcells = con.GetResultsFromQuery("""select count(*) from $$.gridcells""")[1][0]
        number_of_gridcells = number_of_gridcells * proportion
             
        commands_to_execute = \
        """drop database if exists %(output_database_name)s ; 
        create database %(output_database_name)s ; use %(output_database_name)s ;
        
        create table scenario_information as select * from %(input_database_name)s.scenario_information; 
        update scenario_information set parent_database_url = 'jdbc:mysql://%(db_host_name)s/%(input_database_name)s';
        
        create table gridcells as (select * from $$.gridcells order by rand() limit %(number_of_gridcells)i) ; 
        create index gridcells_grid_id on gridcells (grid_id);
        
        create table households as select hh.* from $$.households as hh, gridcells as gc where hh.grid_id = gc.grid_id;
        
        create table jobs as select j.* from $$.jobs as j, gridcells as gc where j.grid_id = gc.grid_id;
        
        create table development_event_history as select deh.* from 
        $$.development_event_history as deh, gridcells as gc where deh.grid_id = gc.grid_id;
        
        create table gridcells_in_geography as select gig.* from
        $$.gridcells_in_geography as gig, gridcells as gc where gig.grid_id = gc.grid_id;
        
        create index gridcells_zone_id on gridcells (zone_id); 
        create table zones as select distinct z.* 
        from $$.zones as z where z.zone_id in (select distinct zone_id from gridcells); 
        create index zones_zone_id on zones (zone_id);
        
        create table travel_data1 as select td.* 
        from $$.travel_data as td, zones where td.from_zone_id = zones.zone_id; 
        
        create table travel_data as select td.* from travel_data1 as td, zones where td.to_zone_id = zones.zone_id; 
        drop table travel_data1;
        
        create table annual_employment_control_totals as select * from $$.annual_employment_control_totals; 
        
        update annual_employment_control_totals set total_home_based_employment = 
        total_home_based_employment * ((select count(*) from jobs) / (select count(*) from $$.jobs)); 
        
        update annual_employment_control_totals set total_non_home_based_employment = 
             total_non_home_based_employment * ((select count(*) from jobs) / (select count(*) from $$.jobs));
        
        create table annual_household_control_totals as select * from $$.annual_household_control_totals; 
        
        update annual_household_control_totals set total_number_of_households = total_number_of_households * (
        (select count(*) from households) / (select count(*) from $$.households))""" % \
                            {"output_database_name":DB_settings.output_database_name, 
                             "input_database_name":DB_settings.input_database_name, 
                             "db_host_name":DB_server_settings.db_host_name,
                             "number_of_gridcells": number_of_gridcells}
        
        commands_to_execute = commands_to_execute.replace('\n', ' ')
        command_list = str.split(commands_to_execute, ';')
        for command in command_list:
            command = command.strip()
            logger.log_status(command)
            con.DoQuery(command)
            
        con.close()
        logger.log_status(DB_settings.output_database_name + ' created successfully!')
         
if __name__=='__main__':
    if len(sys.argv) == 3:
        try: import wingdbstub
        except: pass
        hostname = sys.argv[1]
        proportion = float(sys.argv[2])
    
        class DB_server_settings(object):
            db_host_name = hostname
            db_user_name = os.environ['MYSQLUSERNAME']
            db_password = os.environ['MYSQLPASSWORD']    
        
        class DB_settings(object):
            input_database_name = "PSRC_2000_baseyear"
            output_database_name = ''
    
        DB_settings.output_database_name = DB_settings.input_database_name + '_sampled_' + str(int(100*proportion)) + '_percent'
        GenerateDBSubsetBySampling().make_database_subset(proportion)
    
    else:
        print "usage: \n create_database_subset_by_sampling.py hostname proportion"
        print "       ex: python create_database_subset_by_sampling.py myserver.mydomain.org 0.5"


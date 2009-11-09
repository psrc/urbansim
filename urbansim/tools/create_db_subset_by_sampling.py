# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
import sys
from opus_core.logger import logger

class GenerateDBSubsetBySampling(object):
    def make_database_subset(self, db_server, db, output_db_name, proportion=1.0):
                
        number_of_gridcells = db.GetResultsFromQuery("""select count(*) from gridcells""")[1][0]
        number_of_gridcells = number_of_gridcells * proportion
             
        commands_to_execute = \
        """drop database if exists %(output_database_name)s ; 
        create database %(output_database_name)s ; use %(output_database_name)s ;
        
        create table scenario_information as select * from %(input_database_name)s.scenario_information; 
        
        create table gridcells as (select * from gridcells order by rand() limit %(number_of_gridcells)i) ; 
        create index gridcells_grid_id on gridcells (grid_id);
        
        create table households as select hh.* from households as hh, gridcells as gc where hh.grid_id = gc.grid_id;
        
        create table jobs as select j.* from jobs as j, gridcells as gc where j.grid_id = gc.grid_id;
        
        create table buildings as select j.* from buildings as j, gridcells as gc where j.grid_id = gc.grid_id;
        
        create table development_event_history as select deh.* from 
        development_event_history as deh, gridcells as gc where deh.grid_id = gc.grid_id;
        
        create table gridcells_in_geography as select gig.* from
        gridcells_in_geography as gig, gridcells as gc where gig.grid_id = gc.grid_id;
        
        create index gridcells_zone_id on gridcells (zone_id); 
        create table zones as select distinct z.* 
        from zones as z where z.zone_id in (select distinct zone_id from gridcells); 
        create index zones_zone_id on zones (zone_id);
        
        create table travel_data1 as select td.* 
        from travel_data as td, zones where td.from_zone_id = zones.zone_id; 
        
        create table travel_data as select td.* from travel_data1 as td, zones where td.to_zone_id = zones.zone_id; 
        drop table travel_data1;
        
        create table annual_employment_control_totals as select * from annual_employment_control_totals; 
        
        update annual_employment_control_totals set total_home_based_employment = 
        total_home_based_employment * ((select count(*) from jobs) / (select count(*) from jobs)); 
        
        update annual_employment_control_totals set total_non_home_based_employment = 
             total_non_home_based_employment * ((select count(*) from jobs) / (select count(*) from jobs));
        
        create table annual_household_control_totals as select * from annual_household_control_totals; 
        
        update annual_household_control_totals set total_number_of_households = total_number_of_households * (
        (select count(*) from households) / (select count(*) from households))""" % \
                            {"output_database_name":output_db_name, 
                             "input_database_name":db.database_name, 
                             "number_of_gridcells": number_of_gridcells}
        
        commands_to_execute = commands_to_execute.replace('\n', ' ')
        command_list = str.split(commands_to_execute, ';')
        for command in command_list:
            command = command.strip()
            logger.log_status(command)
            db_server.execute(command)
            
        logger.log_status(output_db_name + ' created successfully!')
         
if __name__=='__main__':
    if len(sys.argv) == 3:
        try: import wingdbstub
        except: pass
        hostname = sys.argv[1]
        proportion = float(sys.argv[2])
        input_db_name = "PSRC_2000_baseyear"
        output_db_name = input_db_name + '_sampled_' + str(int(100*proportion)) + '_percent'
        
        from opus_core.database_management.flatten_scenario_database_chain import FlattenScenarioDatabaseChain
        from opus_core.database_management.database_server import DatabaseServer
        from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration


        from_database_configuration = ScenarioDatabaseConfiguration(
                                            database_name = input_db_name,
                                            host_name = hostname,                                           
                                        )
        to_database_configuration = ScenarioDatabaseConfiguration(
                                            database_name = 'temporary_flattened_scenario_database',
                                            host_name = hostname,                                          
                                        )

        FlattenScenarioDatabaseChain().copy_scenario_database(
                              from_database_configuration = from_database_configuration, 
                              to_database_configuration = to_database_configuration,
                              tables_to_copy = [])
        
        db_server = DatabaseServer(to_database_configuration)   
    
        db = db_server.get_database('temporary_flattened_scenario_database')
    
        GenerateDBSubsetBySampling().make_database_subset(db_server, db, output_db_name, proportion)
        
        db.close()
        db_server.drop_database('temporary_flattened_scenario_database') 
                
    else:
        print "usage: \n create_database_subset_by_sampling.py proportion"
        print "       ex: python create_database_subset_by_sampling.py 0.5"
    


#
# Opus software. Copyright (C) 2005-2008 University of Washington
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


import sys

from copy import copy
from optparse import Option, OptionParser, OptionValueError
from opus_core.logger import logger


class GenerateDBSubsetByCoords(object):
    def make_database_subset(self, db_server, db, output_db_name, low_point, high_point):
        commands_to_execute = ("""
drop database if exists %(output_database_name)s ; 
create database %(output_database_name)s ; use %(output_database_name)s ;

create table scenario_information as select * from %(input_database_name)s.scenario_information; 

create table gridcells as select * from gridcells 
    where relative_x >= %(low_x)s and relative_x <= %(high_x)s and
        relative_y >= %(low_y)s and relative_y <= %(high_y)s; 
create index gridcells_grid_id on gridcells (grid_id);

create table households as select hh.* from households as hh, gridcells as gc where hh.grid_id = gc.grid_id;

create table buildings as select b.* from buildings as b, gridcells as gc where b.grid_id = gc.grid_id;

create table jobs as select j.* from jobs as j, gridcells as gc where j.grid_id = gc.grid_id;

create table development_event_history as select deh.* from 
development_event_history as deh, gridcells as gc where deh.grid_id = gc.grid_id;

create table jobs_for_estimation as select j.* from
jobs_for_estimation as j, gridcells as gc where j.grid_id = gc.grid_id;

create table households_for_estimation as select h.* from
households_for_estimation as h, gridcells as gc where h.grid_id = gc.grid_id;

create table gridcell_fractions_in_zones as select f.* from 
gridcell_fractions_in_zones as f, gridcells as gc where f.grid_id = gc.grid_id;

create index gridcell_fractions_in_zones_zone_id on gridcell_fractions_in_zones (zone_id); 

create index gridcells_zone_id on gridcells (zone_id); create table zones as select distinct z.* 
from zones as z where z.zone_id in (select distinct zone_id from gridcells union select 
distinct zone_id from gridcell_fractions_in_zones); create index zones_zone_id on zones (zone_id);

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
(select count(*) from households) / (select count(*) from households))
        """ % { 'low_x': low_point.x, 
                'low_y': low_point.y, 
                'high_x': high_point.x, 
                'high_y': high_point.y,
                "output_database_name":output_db_name, 
                "input_database_name":db.database_name, 
                "db_host_name":db.host_name,
                }
            )
         
        commands_to_execute = commands_to_execute.replace('\n', ' ')
        command_list = str.split(commands_to_execute, ';')
        for command in command_list:
            command = command.strip()
            logger.log_status(command)
            db_server.DoQuery(command)
        logger.log_status('\n* %s created successfully! *' % output_db_name)


if __name__=='__main__':
    class MyPoint(object):
        x = 0
        y = 0
        
        def __init__(self, x, y):
            self.x = x
            self.y = y
            
        def __str__(self):
            return '(%s,%s)' % (self.x,self.y)    
    
    def check_coord(option, opt, value):
        try:
            values = value.split(',')
            
            if len(values) != 2:
                raise ValueError
            
            return MyPoint(int(values[0]), int(values[1]))
            
        except:
            raise OptionValueError('option %s: invalid coordinate value: %r'
                % (opt, value))
    
    class MyOption(Option):
        TYPES = Option.TYPES + ('coord',)
        TYPE_CHECKER = copy(Option.TYPE_CHECKER)
        TYPE_CHECKER['coord'] = check_coord
    
    
    parser = OptionParser(option_class=MyOption)
    
    parser.add_option('-i', '--input_database', dest='input_db_name', 
        type='string', help='The name of the input database (required)')
    parser.add_option('-o', '--output_database', dest='output_db_name',
        type='string', help="The name of the output database (default:"
            " the name of the input database plus "
            "'_subset_[given coords]')")
    parser.add_option('-s', '--host', dest='host', type='string',
        help="The mysql host (default: MYSQLHOSTNAME environment variable, then"
            " 'localhost').")
    parser.add_option('-u', '--username', dest='username', type='string',
        help='The mysql connection username (default: MYSQLUSERNAME environment'
            ' variable, then nothing).')
    parser.add_option('-p', '--password', dest='password', type='string',
        help='The mysql connection password (default: MYSQLPASSWORD environment'
            ' variable, then nothing).')
    
    parser.add_option('-1', '--point1', dest='point1', type='coord',
        help='The X and Y components of the first point. Comma delimited, with'
            ' no spaces (e.g. --point1=0,0) (required)')
    parser.add_option('-2', '--point2', dest='point2', type='coord',
        help='The X and Y components of the second point. Comma delimited, with'
            ' no spaces (e.g. --point2=100,100) (required)')
    
    (options, args) = parser.parse_args()
    
    if (options.input_db_name is None or
            options.point1 is None or
            options.point2 is None):
        parser.print_help()
        sys.exit(1)

    low_point = MyPoint(
        min(options.point1.x, options.point2.x), 
        min(options.point1.y, options.point2.y))
    high_point = MyPoint(
        max(options.point1.x, options.point2.x), 
        max(options.point1.y, options.point2.y))

    input_db_name = options.input_db_name
    
    output_db_name = options.output_db_name
    if output_db_name is None:
        output_db_name = ('%s_subset_%s_%s_to_%s_%s' 
            % ( input_db_name, 
                low_point.x, 
                low_point.y, 
                high_point.x, 
                high_point.y
                )
            )
       
    from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
    from opus_core.database_management.flatten_scenario_database_chain import FlattenScenarioDatabaseChain
    from opus_core.database_management.database_server import DatabaseServer
    
    hostname = options.host
    username = options.username
    password = options.password
    
    db_server_config = DatabaseServerConfiguration(
        host_name = hostname,
        user_name = username,
        password = password                                        
    )
    db_server = DatabaseServer(db_server_config)
    flatten_db_config = {
        'db_server_config_from':db_server_config,
        'from_database_name':input_db_name,
        'db_server_config_to':db_server_config,
        'to_database_name':'temporary_flattened_scenario_database',
        }
    
    FlattenScenarioDatabaseChain().copy_scenario_database(**flatten_db_config)

    db = db_server.get_database('temporary_flattened_scenario_database')

    GenerateDBSubsetByCoords().make_database_subset(db_server, db, output_db_name, low_point, high_point)
    
    db.close()
    db_server.drop_database('temporary_flattened_scenario_database')
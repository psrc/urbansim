
        
        
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

from opus_core.logger import logger
import os
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.services.run_server.run_manager import RunManager
from opus_core.database_management.database_server import DatabaseServer

def add_runs_to_services_db_from_disk(projects = None):
        
    server_config = GenericOptionGroup().parser.parse_args()[0]
    
    if server_config.protocol == 'sqlite':
        

        
        # set 'datapath' to the path to the opus_data directory.  This is found in the environment variable
        # OPUS_DATA_PATH, or if that environment variable doesn't exist, as the contents of the environment 
        # variable OPUS_HOME followed by 'data'
        datapath = os.environ.get('OPUS_DATA_PATH')
        if datapath is None:
            datapath = os.path.join(os.environ.get('OPUS_HOME'), 'data')
        
            
        for project_name in os.listdir(datapath):
            if projects is not None and project_name not in projects: continue
            
            if not os.path.isdir(os.path.join(datapath, project_name)): continue
            os.environ['OPUSPROJECTNAME'] = project_name
            server = DatabaseServer(server_config)
            server.drop_database(database_name = 'run_activity')
            server.close()
            
            run_manager = RunManager(server_config)
            
            baseyear_directory = os.path.join(datapath, project_name, 'base_year_data')
            
            years = []
            if os.path.exists(baseyear_directory):
                for dir in os.listdir(baseyear_directory):
                    if len(dir) == 4 and dir.isdigit():
                        years.append(int(dir))
                start_year = min(years)
                end_year = max(years)
                run_name = 'base_year_data'
                run_id = run_manager._get_new_run_id()
                resources = {
                     'cache_directory': baseyear_directory,
                     'description': 'base year data',
                     'years': (start_year, end_year)
                }
                logger.log_status('Adding run %s of project %s to run_activity table'%(run_name, project_name))
                run_manager.add_row_to_history(run_id = run_id, 
                                               resources = resources, 
                                               status = 'done', 
                                               run_name = run_name)

            data_directory = os.path.join(datapath, project_name, 'runs')
            if not os.path.exists(data_directory): continue
            
            for run_name in os.listdir(data_directory):
                try:
                    cache_directory = os.path.join(data_directory,run_name)
                    years = []
                    if not os.path.isdir(cache_directory): continue
                    
                    for dir in os.listdir(cache_directory):
                        if len(dir) == 4 and dir.isdigit():
                            years.append(int(dir))
                    start_year = min(years)
                    end_year = max(years)
                    run_id = run_manager._get_new_run_id()
                    resources = {
                         'cache_directory': cache_directory,
                         'description': '',
                         'years': (start_year, end_year)
                    }
                    logger.log_status('Adding run %s of project %s to run_activity table'%(run_name, project_name))
                    run_manager.add_row_to_history(run_id = run_id, 
                                                   resources = resources, 
                                                   status = 'done', 
                                                   run_name = run_name)
                except: pass        
    
if __name__ == '__main__':
    add_runs_to_services_db_from_disk()

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

import getpass
import time
import os
from numpy.random import seed, randint
from numpy import array
from opus_core.misc import load_table_from_text_file, write_table_to_text_file
from opus_core.misc import get_config_from_opus_path
from opus_core.logger import logger
from remote_run_controller import RemoteRunOptionGroup
from remote_run_controller import RemoteRun
from opus_core.services.run_server.run_activity import RunActivity
from urbansim.tools.run_manager import RunManager

class RemoteRunSetOptionGroup(RemoteRunOptionGroup):
    def __init__(self):
        RemoteRunOptionGroup.__init__(self, usage="python %prog [options]",
            description="Control set of urbansim and travel model runs to run on different computers.")
        self.parser.add_option("--run-id-file", dest="run_id_file", default=None, 
                               help="File with run_ids of the set. None means new set will be started.")
        self.parser.add_option("--server-file", dest="server_file", default=None, 
                               help="File with hostnames to run the set on.")
        
class RemoteRunSet(RemoteRun):
    default_run_id_file = 'run_ids'
    python_commands = {"faloorum6.csss.washington.edu": "mosrun -h python",
                       "localhost": "python"}
    configuration_update = {
                            "faloorum6.csss.washington.edu": {'cache_directory_root': '/home/hana/urbansim_cache/psrc/parcel/bm',
                                                              'existing_cache_to_copy': '/home/hana/urbansim_cache/psrc/cache_source_parcel'
                                                              },
                            "localhost": {'cache_directory_root': '/Users/hana/urbansim_cache/psrc/parcel/bm',
                                          'existing_cache_to_copy': '/Users/hana/urbansim_cache/psrc/cache_source_parcel'
                                          }
                            }
    
    def __init__(self, server_file, hostname, username, password, *args, **kwargs):
        self.servers_info = {}
        if server_file is not None: # read hostname-file
            host_names_and_paths_array = load_table_from_text_file(server_file, comment='#')[0]
            for i in range(host_names_and_paths_array.shape[0]):
                self.servers_info[host_names_and_paths_array[i,0]] = {
                                                            'username': host_names_and_paths_array[i,1],
                                                            'opus_path': host_names_and_paths_array[i,2],
                                                            'communication_path_root': host_names_and_paths_array[i,3],
                                                            'number_of_processes': int(host_names_and_paths_array[i,4])}
                if (host_names_and_paths_array[i,0] <> 'localhost'):
                    self.servers_info[host_names_and_paths_array[i,0]]['password'] = getpass.getpass('Password for %s@%s: ' % (
                                self.servers_info[host_names_and_paths_array[i,0]]['username'], 
                                host_names_and_paths_array[i,0]))
                else:
                    self.servers_info[host_names_and_paths_array[i,0]]['password'] = None
        else:
            self.servers_info[hostname] = {
                                           'username': username,
                                           'opus_path': self.remote_opus_path,
                                           'communication_path_root': self.remote_communication_path_root,
                                           'number_of_processes': 1
                                           }
        for server in self.servers_info.keys():
            self.servers_info[server]['python_command'] = self.python_commands.get(server, self.python_command)
            self.servers_info[server]['running'] = 0 # 0 processes are running
 
        RemoteRun.__init__(self, hostname, username, password, *args, **kwargs)
        
 
    def prepare_for_run(self, configuration_path, run_id_file=None, **kwargs):
        self.run_ids_dict = {} # dict of run_id and finished year
        if run_id_file is None:
            config = get_config_from_opus_path(configuration_path)
            self.number_of_runs = config.get("number_of_runs", 1)
            root_seed = config.get("seed", 1)
            seed(root_seed)
            # generate different seed for each run (each seed contains 1 number)
            seed_array = randint(1,2**30, self.number_of_runs)

            for irun in range(self.number_of_runs):
                config['seed']= (seed_array[irun],)
                RemoteRun.prepare_for_run(self, config=config, prepare_cache=False)
                self.run_ids_dict[self.run_id] = (0, 'NA')
            self.run_id_file = self.default_run_id_file
        else:
            self.read_run_id_file(run_id_file)
            self.run_id_file = run_id_file
            run_activity = RunActivity(self.services_database)
            self.run_manager = RunManager(run_activity)

        self.date_time_str = time.strftime('%Y_%m_%d_%H_%M', time.localtime())
        logger.log_status("run_id_file: %s" % self.run_id_file)
        self.write_into_run_id_file()
        return None
            
    def run(self, start_year, end_year, configuration_path, run_id_file=None):
        self.prepare_for_run(configuration_path=configuration_path, run_id_file=run_id_file)    
        self._do_run(start_year, end_year)
        
    def read_run_id_file(self, filename):
        # filename is a file with a pair (run_id, year) per row
        content = load_table_from_text_file(filename, convert_to_float=False)[0]
        for run_id, year, server in content:
            self.run_ids_dict[int(run_id)] = (int(year), server)
        
    def write_into_run_id_file(self):
        result = array(map(lambda(x,y): [x,y[0], y[1]], self.run_ids_dict.iteritems()))
        write_table_to_text_file(self.run_id_file, result)
        
    def _do_run(self, start_year, end_year, *args, **kwargs):

        running_ids = []
        for iter in range(len(self.run_ids_dict.keys())): 
            run_id = self.run_ids_dict.keys()[iter]
            finished_year, server = self.run_ids_dict[run_id]
            while True: # wait for available server
                selected_server, restart = self.select_server(server)
                if selected_server is None: # no server available
                    time.sleep(60)
                    runs_by_status = self.run_manager.get_runs_by_status(running_ids)
                    finished_runs = runs_by_status.get('done', [])
                    failed_runs = runs_by_status.get('failed', [])
                    finished_and_failed_runs = finished_runs + failed_runs
                    self.enable_servers(finished_and_failed_runs)
                    if len(failed_runs) > 0:
                        raise
                    for run in finished_runs:
                        running_ids.remove(run)
                else:
                    break
                
            self.set_environment_for_this_run(selected_server, run_id)
            
            config = self.run_manager.get_resources_for_run_id_from_history(services_host_name=self.services_hostname,
                                                                       services_database_name=self.services_dbname,
                                                                       run_id=self.run_id)
            self.prepare_for_this_run(config, self.configuration_update.get(selected_server, {}), restart)
            if start_year is None:
                this_start_year = config['years'][0]
            else:
                this_start_year = start_year
            running_ids.append(run_id)
            RemoteRun._do_run(self, max(this_start_year, finished_year+1), end_year, config, background=True)
            
            
    def prepare_for_this_run(self, config, config_update={}, restart=False):
        if not restart:
            
            config['cache_directory'] =  '%s/run_%s.%s' % (config_update.get('cache_directory_root',
                                                                             config['creating_baseyear_cache_configuration'].cache_directory_root),
                                                                             self.run_id, self.date_time_str)
            config['creating_baseyear_cache_configuration'].baseyear_cache.existing_cache_to_copy = config_update.get('existing_cache_to_copy', 
                                                                config['creating_baseyear_cache_configuration'].baseyear_cache.existing_cache_to_copy)
        self.prepare_cache_and_communication_path(config)
        self.run_manager.run_activity.storage.DoQuery("DELETE FROM run_activity WHERE run_id = %s" % self.run_id)        
        self.run_manager.run_activity.add_row_to_history(self.run_id, config, "started")
        
    def set_environment_for_this_run(self, server, run_id):
        self.run_id = run_id
        self.username = self.servers_info[server]['username']
        self.hostname = server
        self.password = self.servers_info[server]['password']
        self.remote_communication_path_root = self.servers_info[server]['communication_path_root']
        self.remote_opus_path = self.servers_info[server]['opus_path']
        self.python_command = self.servers_info[server]['python_command']
        self.remote_communication_path = '%s/%s' % (self.remote_communication_path_root, self.run_id)
        self.servers_info[server]['running'] += 1
        self.set_local_output_path()
        self.run_ids_dict[run_id] = (self.run_ids_dict[run_id][0], server)
        self.write_into_run_id_file()
        
    def select_server(self, server):
        restart = False
        selected_server = None
        for s, info in self.servers_info.iteritems():
            if ((server == 'NA') or (server == s)) and (info['running'] < info['number_of_processes']):
                selected_server = s
                break
        if selected_server == server:
            restart=True
        return (selected_server, restart)
    
    def enable_servers(self, runs):
        for run_id in runs:
            server = self.run_ids_dict[run_id][1]
            self.servers_info[server]['running'] =-1
            config = self.run_manager.get_resources_for_run_id_from_history(services_host_name=self.services_hostname,
                                                                       services_database_name=self.services_dbname,
                                                                       run_id=run_id)
            self.run_ids_dict[self.run_id] = (self.get_urbansim_last_year(config), server)
            self.write_into_run_id_file()
        
if __name__ == "__main__":
    option_group = RemoteRunSetOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()
    
    hostname=None
    username=None
    password=None
    if options.server_file is None:
        if options.server is None:
            hostname = raw_input('Hostname [%s]: ' % RemoteRunSet.default_hostname)
            if len(hostname) == 0:
                hostname = RemoteRun.default_hostname
        else:
            hostname = options.server
        if options.user is None:
            username = raw_input('Username [%s]: ' % RemoteRunSet.default_username)
            if len(username) == 0:
                username = RemoteRun.default_username
        else:
            username = options.user
        password = getpass.getpass('Password for %s@%s: ' % (username, hostname))

    try: import wingdbstub
    except: pass
    db = option_group.get_services_database(options)
    run = RemoteRunSet(options.server_file, hostname, username, password, options.host_name, options.database_name, db,
                       options.skip_travel_model, options.skip_urbansim)
    run.run(options.start_year, options.end_year, options.configuration_path, options.run_id_file)
        
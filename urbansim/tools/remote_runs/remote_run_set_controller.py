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

class RemoteRunSetOptionGroup(RemoteRunOptionGroup):
    def __init__(self):
        RemoteRunOptionGroup.__init__(self, usage="python %prog [options]",
            description="Control set of urbansim and travel model runs to run on different computers.")
        self.parser.add_option("--run-id-file", dest="run_id_file", default=None, 
                               help="File with run_ids of the set. None means new set will be started.")
        self.parser.add_option("--server-file", dest="server_file", default=None, 
                               help="File with hostnames to run the set on.")
        
class RemoteRunSet(RemoteRun):
    """
        Launches multiple runs, urbansim on given remote hosts (including localhost), travel model on localhost.
        Several urbansim runs on remote hosts can be run in parallel (makes sense mainly if run with the option --skip-travel-model).
        
        If multiple hosts for urbansim are used, they can be defined in a file given by the option --server-file.
        This file has one line per host in the following format:
            hostname username remote_opus_path remote_communication_path_root number_of_runs_in_parallel_on_this_host
        (see the doc string of the parent class)
        
        The script creates a file 'run_ids' in the current directory that contains information about the runs, their run_ids and hostnames.
        For restarting a simulation, pass this file to the option --run-id-file. 
    """
    default_run_id_file = 'run_ids'
    python_commands = {"localhost": "python"}
    configuration_update = {
                            "localhost": {#'cache_directory_root': '/Users/hana/urbansim_cache/psrc/parcel/bm/0818',
                                          'cache_directory_root': '/Users/hana/urbansim_cache/psrc/parcel/bm/relocation/0114',
                                          'existing_cache_to_copy': '/Users/hana/urbansim_cache/psrc/cache_source_parcel'
                                          #'existing_cache_to_copy': '/Users/hana/urbansim_cache/psrc/parcel/relocation_models_estimation/cache_source_parcel'
                                          },
                            "128.208.52.233": {'cache_directory_root': '/urbansim_cache/psrc_parcel_hana/runs', #paris
                                               'existing_cache_to_copy': '/urbansim_cache/psrc_parcel_hana/base_year_data'
                                          }
                            }
    for i in range(1,13):
        configuration_update["faloorum%s.csss.washington.edu" % i] = {
                                                            'cache_directory_root': '/homes/scratch/hana/urbansim_cache/psrc/parcel/bm/0818',
                                                            'existing_cache_to_copy': '/homes/scratch/hana/urbansim_cache/psrc/cache_source_parcel'
                                                              }    
    def __init__(self, server_file, hostname, username, password, *args, **kwargs):
        self.servers_info = {}
        if server_file is not None: # read hostname-file
            host_names_and_paths_array = load_table_from_text_file(server_file, comment='#')[0]
            passw = None
            for i in range(host_names_and_paths_array.shape[0]):
                self.servers_info[host_names_and_paths_array[i,0]] = {
                                                            'username': host_names_and_paths_array[i,1],
                                                            'opus_path': host_names_and_paths_array[i,2],
                                                            'communication_path_root': host_names_and_paths_array[i,3],
                                                            'number_of_processes': int(host_names_and_paths_array[i,4])}
                previous_passw = None
                if (host_names_and_paths_array[i,0] <> 'localhost'):
                    default = ''
                    if passw is not None:
                        default = ' [previous password]'
                        previous_passw = passw
                    passw = getpass.getpass('Password for %s@%s%s:' % (
                                self.servers_info[host_names_and_paths_array[i,0]]['username'], 
                                host_names_and_paths_array[i,0], default))
                    if len(passw) == 0:
                        passw = previous_passw
                    self.servers_info[host_names_and_paths_array[i,0]]['password'] = passw
                else:
                    self.servers_info[host_names_and_paths_array[i,0]]['password'] = None

        else:
            self.servers_info[hostname] = {
                                           'username': username,
                                           'opus_path': self.remote_opus_path,
                                           'communication_path_root': self.remote_communication_path_root,
                                           'number_of_processes': 1,
                                           'password': password
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
            self.get_run_manager()

        self.date_time_str = time.strftime('%Y_%m_%d_%H_%M', time.localtime())
        logger.log_status("run_id_file: %s" % self.run_id_file)
        self.write_into_run_id_file()
        return None
            
    def run(self, start_year, end_year, configuration_path, run_id_file=None):
        self.prepare_for_run(configuration_path=configuration_path, run_id_file=run_id_file)    
        self._do_run(start_year, end_year)
        
    def read_run_id_file(self, filename):
        # filename is a file with a tuple (run_id, year, hostname) per row
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
                    runs_by_status = self.get_run_manager().get_runs_by_status(running_ids)
                    finished_runs = runs_by_status.get('done', [])
                    failed_runs = runs_by_status.get('failed', [])
                    finished_and_failed_runs = finished_runs + failed_runs
                    self.enable_servers(finished_runs, failed_runs)
                    if len(failed_runs) > 0:
                        raise
                    for run in finished_and_failed_runs:
                        running_ids.remove(run)
                else:
                    break
                
            self.set_environment_for_this_run(selected_server, run_id)
            
            config = self.get_run_manager().get_resources_for_run_id_from_history(run_id=self.run_id)
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
        run_manager = self.get_run_manager()
#        run_manager.delete_everything_for_this_run(run_id = self.run_id)
        run_manager.add_row_to_history(self.run_id, config, "started")
        self.prepare_cache_and_communication_path(config)
        
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
    
    def enable_servers(self, finished_runs=[], failed_runs=[]):
        for run_id in finished_runs+failed_runs:
            server = self.run_ids_dict[run_id][1]
            self.servers_info[server]['running'] -= 1
            config = self.get_run_manager().get_resources_for_run_id_from_history(run_id=run_id)
            if run_id in finished_runs:
                self.run_ids_dict[run_id] = (config['years'][1], server)
            else:
                try:
                    last_year = self.get_urbansim_last_year(config)
                except:
                    last_year = 0
                self.run_ids_dict[run_id] = (int(last_year), server)
        self.write_into_run_id_file()
        
if __name__ == "__main__":
    from opus_core.services.run_server.run_manager import RunManager

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
        if hostname <> 'localhost':
            if options.user is None:
                username = raw_input('Username [%s]: ' % RemoteRunSet.default_username)
                if len(username) == 0:
                    username = RemoteRun.default_username
                else:
                    username = options.user       
            password = getpass.getpass('Password for %s@%s: ' % (username, hostname))

    #try: import wingdbstub
    #except: pass
    run_manager = RunManager(option_group.get_services_database_configuration(options))
    run = RemoteRunSet(options.server_file, hostname, username, password, options.server, options.database_name,
                       options.skip_travel_model, options.skip_urbansim, run_manager)
    run.run(options.start_year, options.end_year, options.configuration_path, options.run_id_file)


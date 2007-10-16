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

import os, sys
import pickle
import copy
import getpass
from opus_core.misc import get_config_from_opus_path
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.services.run_server.run_activity import RunActivity
from opus_core.configuration import Configuration
from urbansim.tools.run_manager import RunManager
from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed
from opus_core.file_utilities import write_resources_to_file
from opus_core.misc import module_path_from_opus_path
from opus_core.fork_process import ForkProcess
from numpy import arange, where, logical_and
from tempfile import mkdtemp

class OptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [options]",
            description="Control urbansim and travle model to run on different computers, tailored for PSRC runs ")
        self.parser.add_option("-c", "--configuration-path", dest="configuration_path", default=None, 
                               help="Opus path to Python module defining run_configuration.")
        self.parser.add_option("--start-year", dest="start_year", default=2000, type="int",
                               help="start year (inclusive)")
        self.parser.add_option("--end-year", dest="end_year", default=2030, type="int",
                               help="end year (inclusive)")
        self.parser.add_option("--run-id", dest="run_id", default=None, 
                               help="which run_id to run, None to start a new run")
        self.parser.add_option("--server", dest="server", default=None, 
                               help="which server to use to run UrbanSim")
        self.parser.add_option("-u", "--user", dest="user", default=None, 
                               help="Which user to use for logging into the remote server")
        
        
class RemoteRun:
    if sys.platform == 'win32':
        plink = 'D:/plink.exe'  #location to plink program
        pscp = 'D:/pscp.exe'
    else:
        plink = 'plink'
        pscp = 'pscp'
        
    python_command = "mosrun -h python" 
    #local_cache_directory_root = 'U:/psrc_parcel/'
    local_cache_directory_root = '/Users/hana/urbansim_cache/psrc/parcel/'

    #default_hostname = "aalborg"
    default_hostname = "faloorum6.csss.washington.edu"
    default_username = getpass.getuser()
    #remote_cache_directory_root = '/projects/null/urbansim5/urbansim_cache/' #the ending slash is critical    
    remote_cache_directory_root = '/home/hana/urbansim_cache/psrc/parcel/'
    remote_opus_path = "/home/hana/opus"
    remote_tmp_path = '/home/hana/urbansim_tmp'
    script_path = 'inprocess/hana/remote_runs'
    remote_travel_models = ['opus_emme2.models.get_cache_data_into_emme2']
    
    def __init__(self, hostname, username, password, services_hostname, services_dbname, services_database):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.services_hostname = services_hostname
        self.services_database = services_database
        self.services_dbname = services_dbname
        
    def prepare_for_run(self, configuration_path, run_id=None):
        run_activity = RunActivity(self.services_database)
        self.run_manager = RunManager(run_activity)
    
        if run_id is not None:
            self.run_id = run_id
        else:
            opus_path = configuration_path
    
            config = get_config_from_opus_path(opus_path)
            insert_auto_generated_cache_directory_if_needed(config)
    
            self.run_id = self.run_manager.run_activity.get_new_history_id()
            head, tail = os.path.split(config['cache_directory'])
            config['cache_directory'] =  os.path.join(head, 'run_' +str(self.run_id)+'.'+tail)
            config['remote_tmp_path'] = os.path.join(self.remote_tmp_path, str(self.run_id))
            
            #create directory on the remote machine for communication
            self.run_remote_python_process("%s/%s/prepare_communication_directory.py" % (self.remote_opus_path, 
                                                                                         self.script_path),
                                           "-d %s" % config['remote_tmp_path'])
    
            # create the baseyear cache on remote machine
            self.run_remote_python_process("%s/%s/create_baseyear_cache.py" % (self.remote_opus_path, self.script_path),
                                           config=config)

            self.run_manager.run_activity.add_row_to_history(self.run_id, config, "started")
            
            #check that run_id must exist
            results = self.run_manager.run_activity.storage.GetResultsFromQuery(
                                                            "SELECT * from run_activity WHERE run_id = %s " % self.run_id)
            if not len(results) > 1:
                raise StandardError, "run_id %s doesn't exist in run_activity table." % self.run_id
            
    def copy_resources_to_remote_host(self, config):
        pickle_dir = mkdtemp()
        pickle_file_path = os.path.join(pickle_dir, 'resources.pickle')
        write_resources_to_file(pickle_file_path, config)
        # copy configuration as resources.pickle to the remote machine
        os.system("%s -v -l %s -pw %s %s %s:%s" % \
                       (self.pscp, self.username, self.password, pickle_file_path, self.hostname, 
                        config['remote_tmp_path']))
        
    def run_remote_python_process(self, python_script, script_options="", config=None, is_opus_path=False):
        if config is not None:
            self.copy_resources_to_remote_host(config)
            cmd_postfix = "-r %s/resources.pickle" % config['remote_tmp_path']
        else:
            cmd_postfix = ""
        if is_opus_path:
            python_script_full_name = self.remote_opus_path
            parts = python_script.split('.')
            for part in parts:
                python_script_full_name = os.path.join(python_script_full_name, part)
            python_script_full_name = python_script_full_name + '.py'
        else:
            python_script_full_name = python_script
        os.system("%s -v -ssh -l %s -pw %s %s %s %s %s %s" % \
                   (self.plink, self.username, self.password, self.hostname, self.python_command, python_script_full_name, 
                    script_options, cmd_postfix))
            
    def run(self, start_year, end_year):
        urbansim_resources = self.run_manager.get_resources_for_run_id_from_history(services_host_name=self.services_hostname,
                                                                       services_database_name=self.services_dbname,
                                                                       run_id=self.run_id)
        #TODO: is this line necessary?
        #urbansim_resources['flt_directory'] = os.path.join(urbansim_resources['cache_directory'], str(restart_year - 1))
        head, tail = os.path.split(urbansim_resources['cache_directory'])
        #remote_cache_directory = os.path.join(remote_cache_directory_root, tail)
        local_cache_directory = os.path.join(self.local_cache_directory_root, tail)
    
        travel_model_resources = None
        if urbansim_resources.has_key('travel_model_configuration'):
            travel_model_resources = Configuration(urbansim_resources)
        
        #urbansim_resources['cache_directory'] = remote_cache_directory
        travel_model_resources['cache_directory'] = local_cache_directory
    
        #only keep sorted travel model years falls into years range
        travel_model_years = []
        for key in travel_model_resources['travel_model_configuration'].keys():
            if type(key) == int:
                if key >= start_year and key <= end_year:
                    travel_model_years.append(key)
        travel_model_years.sort()
        
        this_start_year = start_year
        for travel_model_year in travel_model_years:
            this_end_year = travel_model_year
            if this_start_year >= this_end_year:
                if this_end_year == end_year:
                    sys.exit(1) #run finished
                else:
                    this_end_year = end_year
            urbansim_resources['years'] = (this_start_year, this_end_year)
                
            self.run_manager.run_activity.storage.DoQuery("DELETE FROM run_activity WHERE run_id = %s" % self.run_id)        
            self.run_manager.run_activity.add_row_to_history(self.run_id, urbansim_resources, "started")
            
            #self.run_remote_python_process("%s/urbansim/tools/restart_run.py" % self.remote_opus_path, 
            #                               "%s %s --skip-cache-cleanup --skip-travel-model" % (self.run_id, this_start_year))                   
                    
            if travel_model_resources is not None:
                # run travel models
                if travel_model_resources['travel_model_configuration'].has_key(this_end_year):
                    for full_model_path in travel_model_resources['travel_model_configuration']['models']:
                        if full_model_path in self.remote_travel_models:
                            # run this model remotely
                            travel_model_resources['cache_directory'] = urbansim_resources['cache_directory']
                            self.run_remote_python_process(full_model_path, 
                                                           '-y %d' % this_end_year,
                                                           config=travel_model_resources,
                                                           is_opus_path=True)
                            travel_model_resources['cache_directory'] = local_cache_directory
                        else:
                            ForkProcess().fork_new_process(full_model_path, 
                                                           travel_model_resources, optional_args='-y %d' % this_end_year)
    
            if not os.path.exists(os.path.join(self.local_cache_directory, str(this_end_year+1))):
                raise StandardError, "travel model didn't create any output for year %s in directory %s; there may be problem with travel model run" % \
                                    (this_end_year+1, self.local_cache_directory)
                
            this_start_year = travel_model_year + 1  #next run starting from the next year of the travel model year
if __name__ == "__main__":
    option_group = OptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()
    
    if options.server is None:
        hostname = raw_input('Hostname [%s]: ' % RemoteRun.default_hostname)
        if len(hostname) == 0:
            hostname = RemoteRun.default_hostname
    else:
        hostname = options.server
    if options.user is None:
        username = raw_input('Username [%s]: ' % RemoteRun.default_username)
        if len(username) == 0:
            username = RemoteRun.default_username
    else:
        username = options.user
    password = getpass.getpass('Password for %s@%s: ' % (username, hostname))

    #try: import wingdbstub
    #except: pass
    db = option_group.get_services_database(options)
    run = RemoteRun(hostname, username, password, options.host_name, options.database_name, db)
    run.prepare_for_run(options.configuration_path, options.run_id)
    run.run(options.start_year, options.end_year)
 
 



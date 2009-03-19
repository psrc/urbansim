# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os, sys
import pickle
import copy
import getpass
import shutil
import socket
import time
from opus_core.misc import get_config_from_opus_path
from opus_core.misc import load_from_text_file, get_host_name
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_core.configuration import Configuration
from urbansim.tools.run_manager import RunManager
from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed
from opus_core.file_utilities import write_resources_to_file
from opus_core.fork_process import ForkProcess
from opus_core.logger import logger
from tempfile import mkdtemp
from opus_emme2.models.abstract_emme2_travel_model import AbstractEmme2TravelModel

class RemoteRunOptionGroup(GenericOptionGroup):
    def __init__(self, **kwargs):
        GenericOptionGroup.__init__(self, usage="python %prog [options]",
            description="Control urbansim and travel model to run on different computers, tailored for PSRC runs ")
        self.parser.add_option("-c", "--configuration-path", dest="configuration_path", default=None, 
                               help="Opus path to Python module defining run_configuration.")
        self.parser.add_option("--start-year", dest="start_year", default=None, type="int",
                               help="start year (inclusive)")
        self.parser.add_option("--end-year", dest="end_year", default=None, type="int",
                               help="end year (inclusive)")
        self.parser.add_option("--run-id", dest="run_id", default=None, type="int",
                               help="which run_id to run, None to start a new run")
        self.parser.add_option("--server", dest="server", default=None, 
                               help="which server to use to run UrbanSim")
        self.parser.add_option("-u", "--user", dest="user", default=None, 
                               help="Which user to use for logging into the remote server")
        self.parser.add_option("--skip-travel-model", dest="skip_travel_model", default=False, action="store_true", 
                               help="Travel model will not be run.")
        self.parser.add_option("--skip-urbansim", dest="skip_urbansim", default=False, action="store_true", 
                               help="Urbansim will not be run.")
        
        
class RemoteRun:
    """ 
        This class runs travel model and urbansim on different computers. A simulation is started from a computer on which 
        the travel model is running. The process launches an urbansim simulation on a remote computer and the travel model on the localhost.
        
        Requirements: - Both computers must have installed: plink, pscp (part of the putty system, http://www.chiark.greenend.org.uk/~sgtatham/putty).
                      - Both computers have working opus installation.
                      - urbansim can be launched using the services database (i.e. one has a connection to mysql server and database 'services' exists).
                      - The remote computer has access to the cache data (defined by existing_cache_to_copy and cache_directory_root in the configuration).
        
        The communication is done via file transfer. There must be a directory set on both computers where the 'communication' files 
        are copied to and from. 
        
        Configuration can be specified only on the localhost. The configuration entries existing_cache_to_copy and cache_directory_root
        specify cache directories on the remote host.
    """
    
    # Modify the following settings in order to match your environment
    ##################################################################
    # how to invoke plink and pscp
    if sys.platform == 'win32':
        plink = 'D:/plink.exe'
        pscp = 'D:/pscp.exe'
    else:
        plink = 'plink'
        pscp = 'pscp'
        
    # how to invoke python on the remote host
    python_command = "python" 
    
    # default name of remote host and the user name (user will be prompted for those and can overwrite the default values) 
    #default_hostname = "aalborg"
    default_hostname = "faloorum5.csss.washington.edu"
    default_username = getpass.getuser()

    # opus python path on the remote host (where opus projects live) 
    #remote_opus_path = "/home/hana/opus"
    remote_opus_path = "/Users/hana/workspace"
    
    # root path for the process communicationon on the remote host (a subdirectory with a run_id will be created in runtime).  
    #remote_communication_path_root = '/home/hana/urbansim_tmp'
    remote_communication_path_root = '/Users/hana/urbansim_tmp'
    
    # root path for the process communicationon on the local host (a subdirectory with a run_id will be created in runtime).  
    #local_output_path_root = 'c:/hana/runs'
    local_output_path_root = '/Users/hana/tmp'
    
    # number of banks of the travel model (e.g. if the TM creates directories bank1, bank2 and bank3, the value is [1, 2, 3])
    #banks = [1, 2, 3] 
    banks = [1] 
    #######################################################################
    
    # do not change the following two settings unless you know what you're doing.
    script_path = 'urbansim/tools/remote_runs'
    remote_travel_models = ['opus_emme2.models.get_cache_data_into_emme2']
    
    def __init__(self, hostname, username, password, services_hostname, services_dbname,
                 skip_travel_model=False, skip_urbansim=False, run_manager=None):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.services_hostname = services_hostname
        self.services_dbname = services_dbname
        self.remote_communication_path = None
        self.skip_travel_model = skip_travel_model
        self.skip_urbansim = skip_urbansim
        self.services_db_config = ServicesDatabaseConfiguration(
                                        host_name = services_hostname, 
                                        user_name = username, 
                                        password = password,
                                        database_name = services_dbname
                                        )
        self._run_manager = None
        if run_manager:
            self._run_manager = run_manager
        
    def prepare_for_run(self, configuration_path=None, config=None, run_id=None, prepare_cache=True, run_name = None):
        """Configuration is given either as an opus path (configuration_path) or as a Configuration object (config)."""
    
        if run_id is not None:
            self.run_id = run_id
            config = self.get_run_manager().get_resources_for_run_id_from_history(run_id=self.run_id)
            self.remote_communication_path = '%s/%s' % (self.remote_communication_path_root, self.run_id)
        else:
            if configuration_path is not None:
                opus_path = configuration_path
                config = get_config_from_opus_path(opus_path)
            else:
                if config is None:
                    raise StandardError, "Either configuration_path, config or run_id must be given."
            insert_auto_generated_cache_directory_if_needed(config)
    
            self.run_id = self.get_run_manager()._get_new_run_id()
            head, tail = os.path.split(config['cache_directory'])
            config['cache_directory'] =  '%s/run_%s.%s' % (head, self.run_id, tail)
            self.remote_communication_path = '%s/%s' % (self.remote_communication_path_root, self.run_id)
            
            if not self.skip_urbansim and prepare_cache:
                self.prepare_cache_and_communication_path(config)

            self.get_run_manager().add_row_to_history(self.run_id, config, "started", run_name = None)
            
            #check that run_id must exist
            results = self.get_run_manager().services_db.GetResultsFromQuery(
                                                            "SELECT * from run_activity WHERE run_id = %s " % self.run_id)
            if not len(results) > 1:
                raise StandardError, "run_id %s doesn't exist in run_activity table." % self.run_id
            
        self.set_local_output_path()
        return config
                    
    def prepare_cache_and_communication_path(self, config):
        #create directory on the remote machine for communication
        self.run_remote_python_process("%s/%s/prepare_communication_directory.py" % (self.remote_opus_path, 
                                                                                 self.script_path),
                                   "-d %s" % self.remote_communication_path)

        # create the baseyear cache on remote machine
        self.run_remote_python_process("%s/%s/create_baseyear_cache.py" % (self.remote_opus_path, self.script_path),
                                   config=config)
        
    def set_local_output_path(self):
        self.local_output_path = os.path.join(self.local_output_path_root, str(self.run_id))
        if not os.path.exists(self.local_output_path):
            os.makedirs('%s' % self.local_output_path)
            
    def is_localhost(self):
        if (self.hostname == 'localhost') or (self.hostname == get_host_name()) or \
            (self.hostname == socket.gethostname()):
            return True
        return False
    
    def copy_resources_to_remote_host(self, config):
        pickle_dir = mkdtemp()
        pickle_file_path = os.path.join(pickle_dir, 'resources.pickle')
        write_resources_to_file(pickle_file_path, config)
        # copy configuration as resources.pickle to the remote machine
        self.copy_file_to_remote_host(pickle_file_path)
        
    def copy_file_from_remote_host_and_get_max_zone(self, file, local_directory):
        self.copy_file_from_remote_host(file, local_directory)
        f = open("%s/%s" % (local_directory, file), 'r')
        file_contents = f.readlines()
        f.close()
        last_line = file_contents[-1]
        elements = last_line.split('   ')
        return int(elements[0])
        
    def copy_file_from_remote_host(self, file, local_directory):
        if not os.path.exists(local_directory):
            os.makedirs('%s' % local_directory)
        full_path = "%s/%s" % (self.remote_communication_path, file)
        logger.log_status("Copy %s:%s to %s" % (self.hostname, 
                        full_path, local_directory))
        if self.is_localhost():
            shutil.copy(full_path, local_directory)
        else:
            os.system("%s -l %s -pw %s %s:%s %s" % \
                       (self.pscp, self.username, self.password, self.hostname, 
                        full_path, local_directory))
        
    def copy_file_to_remote_host(self, file, subdirectory=''):
        full_path = "%s/%s" % (self.remote_communication_path, subdirectory)
        logger.log_status("Copy %s to %s:%s" % (file, self.hostname, full_path))
        if self.is_localhost():
            shutil.copy(file, full_path)
        else:
            os.system("%s -l %s -pw %s %s %s:%s" % \
                       (self.pscp, self.username, self.password, file, self.hostname, full_path))
        
    def run_remote_python_process(self, python_script, script_options="", config=None, is_opus_path=False):
        if config is not None:
            self.copy_resources_to_remote_host(config)
            cmd_postfix = "-r %s/resources.pickle" % self.remote_communication_path
        else:
            cmd_postfix = ""
        if is_opus_path:
            python_script_full_name = self.remote_opus_path
            parts = python_script.split('.')
            for part in parts:
                python_script_full_name = "%s/%s" % (python_script_full_name, part)
            python_script_full_name = python_script_full_name + '.py'
        else:
            python_script_full_name = python_script
        logger.log_status("Running on %s: %s %s %s %s" % (self.hostname, self.python_command, python_script_full_name, 
                    script_options, cmd_postfix))
        if self.is_localhost():
            os.system("%s %s %s %s" % (self.python_command, python_script_full_name, 
                    script_options, cmd_postfix))
        else:
            os.system("%s -ssh -l %s -pw %s %s %s %s %s %s" % \
                   (self.plink, self.username, self.password, self.hostname, self.python_command, python_script_full_name, 
                    script_options, cmd_postfix))
            
    def has_urbansim_finished(self, config):
        last_year = self.get_urbansim_last_year(config)
        if last_year < config['years'][1]:
            logger.log_warning("urbansim finished in year %d" % last_year)
            return False
        return True
    
    def get_urbansim_last_year(self, config):
        self.run_remote_python_process('%s/%s/write_last_urbansim_year.py' % (self.remote_opus_path, self.script_path), 
                                       '-d %s -o %s/last_year.txt' % (config['cache_directory'], self.remote_communication_path))
        self.copy_file_from_remote_host('last_year.txt', self.local_output_path)
        return load_from_text_file('%s/last_year.txt' % self.local_output_path, convert_to_float=True)[0]
        
    def run(self, start_year, end_year, configuration_path, run_id=None):
        config = self.prepare_for_run(configuration_path=configuration_path, run_id=run_id)    
        self._do_run(start_year, end_year, config)
        
    def _do_run(self, start_year, end_year, urbansim_resources, background=False):
        travel_model_resources = Configuration(urbansim_resources)
        if start_year is None:
            start_year = travel_model_resources['years'][0]
        if end_year is None:
            end_year = travel_model_resources['years'][1]
        if end_year < start_year:
            logger.log_warning("In run %s end_year (%s) is smaller than start_year (%s)." % (self.run_id, end_year, start_year))
            sys.exit(1)
        #only keep sorted travel model years falls into years range
        travel_model_years = []
        if not self.skip_travel_model:
            for key in travel_model_resources['travel_model_configuration'].keys():
                if type(key) == int:
                    if key >= start_year and key <= end_year:
                        travel_model_years.append(key)
        if end_year not in travel_model_years:
            travel_model_years.append(end_year)
        travel_model_years.sort()
        this_start_year = start_year
        bg = ''
        if background:
            bg = '&'
        for travel_model_year in travel_model_years:
            this_end_year = travel_model_year
            if this_end_year > end_year:
                sys.exit(1) #run finished

            if this_start_year <= this_end_year:
                urbansim_resources['years'] = (this_start_year, this_end_year)

                run_manager = self.get_run_manager()                
                run_manager.add_row_to_history(run_id=self.run_id, resources=urbansim_resources, status="started")
                
                if not self.skip_urbansim:
                    self.run_remote_python_process("%s/urbansim/tools/restart_run.py" % self.remote_opus_path, 
                                               "%s %s --skip-cache-cleanup --skip-travel-model %s" % (
                                                         self.run_id, this_start_year, bg),
                                                   )
                    if not background:               
                        if not self.has_urbansim_finished(urbansim_resources):
                            raise StandardError, "There was an error in the urbansim run."

            # run travel models
            if not self.skip_travel_model:
                if background: # wait until urbansim finishes; check every 60 seconds
                    while True:
                        time.sleep(60)
                        runs_by_status = self.get_run_manager().get_runs_by_status([self.run_id])
                        if self.run_id in runs_by_status.get('done', []):
                            break
                        if self.run_id in runs_by_status.get('failed', []):
                            raise StandardError, "There was an error in the urbansim run."

                max_zone_id = 0
                if travel_model_resources['travel_model_configuration'].has_key(this_end_year):
                    tm = AbstractEmme2TravelModel(travel_model_resources)
                    for full_model_path in travel_model_resources['travel_model_configuration'][this_end_year].get('models'):
                        if full_model_path in self.remote_travel_models:
                            # run this model remotely
                            self.run_remote_python_process(full_model_path, 
                                                           '-y %d -d %s' % (this_end_year, self.remote_communication_path),
                                                           config=travel_model_resources,
                                                           is_opus_path=True)
                            tripgen_dir = tm.get_emme2_dir(this_end_year, 'tripgen')
                            max_zone_id = self.copy_file_from_remote_host_and_get_max_zone('TAZDATA.MA2', '%s/inputtg' % tripgen_dir)
                        else:
                            optional_args=['-y', this_end_year]
                            if full_model_path == 'opus_emme2.models.get_emme2_data_into_cache':
                                optional_args='%s -m -z %s' % (optional_args, max_zone_id)
                            elif full_model_path == 'opus_emme2.models.run_travel_model':
                                optional_args='%s -o %s' % (optional_args, os.path.join(self.local_output_path,'emme2_%d_log.txt' % this_end_year))
                            elif full_model_path == 'opus_emme2.models.run_export_macros':
                                optional_args='%s -o %s' % (optional_args, os.path.join(self.local_output_path,'emme2_export_macros_%d_log.txt' % this_end_year))
                            ForkProcess().fork_new_process(full_model_path, 
                                                           travel_model_resources, optional_args=optional_args)
                    reports = travel_model_resources['travel_model_configuration'].get('reports_to_copy', [])
                    for x in self.banks:
                        bank_dir = tm.get_emme2_dir(this_end_year, "bank%i" % x)
                        self.copy_file_to_remote_host("%s/*_one_matrix.txt" % bank_dir, subdirectory="bank%i" % x)
                        node_map = travel_model_resources['travel_model_configuration'].get('node_matrix_variable_map', {})
                        node_files = []
                        if "bank%i" % x in node_map.keys():
                            node_files = node_map["bank%i" % x].keys()
                        for report in reports+node_files:
                            report_name = os.path.join(bank_dir, report)
                            if os.path.exists(report_name):
                                self.copy_file_to_remote_host(report_name, subdirectory="bank%i" % x)
                        
                    self.run_remote_python_process('opus_emme2.models.get_emme2_data_into_cache', 
                               '-y %d --matrix_directory=%s' % (this_end_year, self.remote_communication_path),
                               config=travel_model_resources, is_opus_path=True
                                                   )
                    
            this_start_year = travel_model_year + 1  #next run starting from the next year of the travel model year
            
    def get_run_manager(self):
        """in case the connection to services timeout, reconnect
        """
        try:
            self._run_manager.services_db.table_exists('run_activity')
        except:  #connection has gone away, re-create run_manager
            self._run_manager = RunManager( self.services_db_config)
        return self._run_manager
    
if __name__ == "__main__":
    option_group = RemoteRunOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()
    
    if options.server is None:
        hostname = raw_input('Hostname [%s]: ' % RemoteRun.default_hostname)
        if len(hostname) == 0:
            hostname = RemoteRun.default_hostname
    else:
        hostname = options.server
        
    username=None
    password=None
    if hostname <> 'localhost':
        if options.user is None:
            username = raw_input('Username [%s]: ' % RemoteRun.default_username)
            if len(username) == 0:
                username = RemoteRun.default_username
            else:
                username = options.user
        password = getpass.getpass('Password for %s@%s: ' % (username, hostname))

    try: import wingdbstub
    except: pass
    run_manager = option_group.get_run_manager(options)
    run = RemoteRun(hostname, username, password, options.host_name, options.database_name,
                    options.skip_travel_model, options.skip_urbansim, run_manager)
    run.run(options.start_year, options.end_year, options.configuration_path, options.run_id)
 
 



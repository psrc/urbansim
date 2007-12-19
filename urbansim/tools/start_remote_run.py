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

import os 
import sys 
import time 
import copy 
import socket
from opus_core.misc import get_config_from_opus_path
from opus_core.misc import module_path_from_opus_path, get_host_name
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.database_server_configuration import DatabaseServerConfiguration
from opus_core.services.run_server.run_activity import RunActivity
from opus_core.services.run_server.run_manager import RunManager, insert_auto_generated_cache_directory_if_needed
from opus_core.fork_process import ForkProcess
from opus_core.logger import logger
from numpy import arange, where, logical_and
from nturl2path import pathname2url
from opus_core.store.sftp_flt_storage import get_stdout_for_ssh_cmd, exists_remotely, load_key_if_exists, _makedirs
import paramiko

class OptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [options]",
            description="Control urbansim and travle model to run on different computers")
        self.parser.add_option("-c", "--configuration-path", dest="configuration_path", default=None, 
                               help="Opus path to Python module defining run_configuration.")
        self.parser.add_option("--run-id", dest="run_id", default=None, 
                               help="which run_id to run, None to start a new run")
        self.parser.add_option("--urbansim-server", dest="urbansim_server", default=None,
                               help="the server runs UrbanSim")
        self.parser.add_option("--travelmodel-server", dest="travelmodel_server", default=None,
                               help="the server runs travel model, default on localhost")        
        self.parser.add_option("-u", "--runserver-username", dest="runserver_username", default=None, 
                               help="Which user name to use for logging into the urbansim and/or travelmodel server(s)")
        ## mostly for debugging purpose
        self.parser.add_option("--start-year", dest="start_year", default=None,
                               help="start year (inclusive)")
        self.parser.add_option("--end-year", dest="end_year", default=None,
                               help="end year (inclusive)")
#        self.parser.add_option("--skip-travel-model", dest="skip_travel_model", default=False, action="store_true", 
#                               help="Travel model will not be run.")
#        self.parser.add_option("--skip-urbansim", dest="skip_urbansim", default=False, action="store_true", 
#                               help="Urbansim will not be run.")
        

class RemoteRun:
    """ 
        This class runs travel model and urbansim on different computers. 
        The script launches an urbansim simulation on the computer specified by urbansim_server and 
        the travel model on the computer specified by travelmodel_server.  
        Both or either can be specifed by command line arguments or system environment variables URBANSIMHOSTNAME and TRAVELMODELHOSTNAME
        
        Examples:
        1.) python start_remote_run.py -c psrc.configs.baseline_with_travel_model
        starts a urbansim simulation and travel model run on localhost (if URBANSIMHOSTNAME and TRAVELMODELHOSTNAME is unspecified).
        This works similarly as opus_core/tools/start_run.py.
         
        2.) python start_remote_run.py -c psrc.configs.baseline_with_travel_model --urbansim-server=ServerA -u user_on_ServerA
        starts a urbansim simulation on ServerA, using user name user_on_ServerA to log on, and travel model run on localhost (if TRAVELMODELHOSTNAME is unspecified).

        3.) python start_remote_run.py -c psrc.configs.baseline_with_travel_model --travelmodel-server=ServerB -u user_on_ServerB
        starts a urbansim simulation on localhost and travel model run on ServerB, using user name user_on_ServerB to log on (if URBANSIMHOSTNAME is unspecified).

        4.) python start_remote_run.py -c psrc.configs.baseline_with_travel_model --urbansim-server=ServerA --travelmodel-server=ServerB -u user_on_ServerA_and_ServerB
        starts a urbansim simulation on ServerA and travel model run on ServerB, both using user name user_on_ServerA_and_ServerB to log on
        
        alternatively, one can specify URBANSIMHOSTNAME, URBANSIMUSERNAME, and URBANSIMPASSWORD, then
        5.) python start_remote_run.py -c psrc.configs.baseline_with_travel_model
        is the same as example 2.
        
        Or if both URBANSIMHOSTNAME, URBANSIMUSERNAME, URBANSIMPASSWORD, and TRAVELMODELHOSTNAME, TRAVELMODELUSERNAME, TRAVELMODELPASSWORD are specified, then
        6.) python start_remote_run.py -c psrc.configs.baseline_with_travel_model
        is the same as example 4.
        
        Password(s) can be specified in system environment variables, 
        (Refer to http://www.urbansim.org/opus/stable-releases/opus-2006-07-14/userguide/node16.html for more details on defining system variables)
        or stored in an SSH key file (http://linux.byexamples.com/archives/297/how-to-ssh-without-password/)
        
        Requirements: - paramiko python module installed, in addition to python modules required by opus/urbansim 
                      - all computers have working opus installation
                      - remote computers and localhost (if UrbanSim runs on localhost) have SSH server running and can be accessed through SSH
                      - the services database connection (i.e. one has a connection to mysql server and database 'services' exists).
                
        The configuration file on the localhost hard disk drive is used when invoked with a configuration file. All directories in a configuration file 
        (e.g. existing_cache_to_copy and cache_directory_root ) are relative to the computer using the part of configuration.  
    """
    
    def __init__(self, urbansim_server_config, travelmodel_server_config, services_db_config, run_manager=None):
        
        self.urbansim_server_config = urbansim_server_config
        self.travelmodel_server_config = travelmodel_server_config
        self.services_db_config = services_db_config
        
        self.ssh = {}
        if not self.is_localhost(self.urbansim_server_config['hostname']):
            self.ssh['urbansim_server'] = self.get_ssh_client(None, self.urbansim_server_config)
        
        if not self.is_localhost(self.travelmodel_server_config['hostname']):
            self.ssh['travelmodel_server'] = self.get_ssh_client(None, self.travelmodel_server_config)
            
        self.services_db_config = DatabaseServerConfiguration(
                                            host_name=services_db_config['hostname'], 
                                            user_name=services_db_config['username'],
                                            password=services_db_config['password'])
        self.services_db_name = services_db_config['database_name']
        self._run_manager = None
        if run_manager:
            self._run_manager = run_manager

    def __del__(self):
        for key, value in self.ssh.iteritems():
            value.close()
    
    def prepare_for_run(self, configuration_path=None, config=None, run_id=None):
        """Configuration is given either as an opus path (configuration_path) or as a Configuration object (config)."""
    
        if run_id is not None:
            config = self.get_run_manager().get_resources_for_run_id_from_history(services_host_name=self.services_db_config.host_name,
                                                                                  services_database_name=self.services_db_name,
                                                                                  run_id=run_id)
        else:
            if configuration_path is not None:
                config = get_config_from_opus_path(configuration_path)
            elif config is None:
                    raise StandardError, "Either configuration_path, config or run_id must be given."
            insert_auto_generated_cache_directory_if_needed(config)
            self.get_run_manager().setup_new_run(run_name = config['cache_directory'])
            run_id = self.get_run_manager().history_id            
            config['cache_directory'] = pathname2url(self.get_run_manager().get_current_cache_directory())
            ## pathname2url converts '\' or '\\' to '/'; it is necessary when this script is invoked from a nt os
            self.get_run_manager().run_activity.add_row_to_history(run_id, config, "started")
            
            #verify run_id has been added to services db
            results = self.get_run_manager().run_activity.storage.GetResultsFromQuery(
                                                            "SELECT * from run_activity WHERE run_id = %s " % run_id)
            if not len(results) > 1:
                raise StandardError, "run_id %s doesn't exist in run_activity table." % run_id

        return run_id, config

    def run(self, configuration_path, run_id=None, start_year=None, end_year=None):
        run_id, config = self.prepare_for_run(configuration_path, run_id=run_id)
        self._do_run(run_id, config, start_year=start_year, end_year=end_year)
        
    def _do_run(self, run_id, config, start_year=None, end_year=None):
        cache_directory = config['cache_directory']
        if start_year is None:
            start_year = config['years'][0]
        if end_year is None:
            end_year = config['years'][1]

        travel_model_resources = None
        travel_model_years = []
        if config.has_key('travel_model_configuration'):
            travel_model_resources = copy.deepcopy(config)

            if not self.is_localhost(self.urbansim_server_config['hostname']):
                travel_model_resources['cache_directory'] = "sftp://%s@%s%s" % (self.urbansim_server_config['username'], 
                                                                               self.urbansim_server_config['hostname'], 
                                                                               cache_directory)
            elif not self.is_localhost(self.travelmodel_server_config['hostname']):
            ## urbansim runs on localhost, and travel model runs on travelmodel_server
            ## set sftp_flt_storage to the hostname of localhost
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('google.com', 0))
                urbansim_server = s.getsockname()[0]    #this is to replace socket.gethostname(), which won't work in some case
                travel_model_resources['cache_directory'] = "sftp://%s@%s%s" % (self.urbansim_server_config['username'], 
                                                                               urbansim_server, 
                                                                               cache_directory)
            #only keep sorted travel model years falls into years range                
            for key in travel_model_resources['travel_model_configuration'].keys():
                if type(key) == int:
                    if key >= start_year and key <= end_year:
                        travel_model_years.append(key)
        
        if end_year not in travel_model_years:
            travel_model_years.append(end_year)
            ## in the case end_year is not a travel_model year, appending it
            ## so we have 1 more iteration after the last travel_model_year
        travel_model_years.sort()
        
        this_start_year = start_year
        for travel_model_year in travel_model_years:
            if this_start_year > end_year:
                return #run finished, should not be needed
            this_end_year = travel_model_year
                    
            config['years'] = (this_start_year, this_end_year)
            ## since there is no --skip-travel-model switch for restart_run yet
            ## delete travel_model_configuration, so travel model won't run on urbansim_server
            if config.has_key('travel_model_configuration'):
                del config['travel_model_configuration']
            self.update_services_database(self.get_run_manager().run_activity, run_id, config)
            
            if not self.is_localhost(self.urbansim_server_config['hostname']):
                logger.start_block("Start UrbanSim Simulation on %s from %s to %s" % (self.urbansim_server_config['hostname'],
                                                                                      this_start_year, this_end_year) )
                cmd = 'python %(module)s %(run_id)s %(start_year)s --hostname=%(services_hostname)s' % \
                      {'module':self.remote_module_path_from_opus_path(self.get_ssh_client(self.ssh['urbansim_server'], self.urbansim_server_config),
                                                                       'opus_core.tools.restart_run'), 
                       'run_id':run_id, 'start_year':this_start_year,
                       'services_hostname': self.services_db_config.host_name}
                cmd += ' --skip-cache-cleanup --create-baseyear-cache-if-not-exists >> ' + 'urbansim_run_%s.log' % run_id
                ## to avoid stdout overfilling sshclient buffer, redirect stdout to a log file
                ## TODO: better handle the location of the urbansim_remote_run.log
                logger.log_status("Call " + cmd)
                try: 
                    ssh = self.get_ssh_client(self.ssh['urbansim_server'], self.urbansim_server_config)
                    std = ssh.exec_command(cmd)  #std[0] - stdin, std[1] - stdout, std[2] - stderr
                except: 
                    raise RuntimeError, "there is a problem running urbansim remotely"
                self.wait_until_run_done_or_failed(run_id, std=std)
                logger.end_block()
                ##TODO: open_sftp may need to be close()
                if not exists_remotely(self.get_ssh_client(self.ssh['urbansim_server'], self.urbansim_server_config).open_sftp(), 
                                       pathname2url(os.path.join(cache_directory, str(this_end_year))) ):
                    raise StandardError, "cache for year %s doesn't exist in directory %s; there may be problem with urbansim run" % \
                                        (this_end_year, cache_directory)
            else:
                cmd = 'python %(module)s %(run_id)s %(start_year)s --hostname=%(services_hostname)s' % \
                      {'module':module_path_from_opus_path('opus_core.tools.restart_run'), 
                       'run_id':run_id, 'start_year':this_start_year,
                       'services_hostname': self.services_db_config.host_name}
                cmd += ' --skip-cache-cleanup --create-baseyear-cache-if-not-exists'
                logger.log_status("Call " + cmd)
                os.system(cmd)
                if not os.path.exists(os.path.join(cache_directory, str(this_end_year))):
                    raise StandardError, "cache for year %s doesn't exist in directory %s; there may be problem with urbansim run" % \
                                        (this_end_year, cache_directory)
                
            if travel_model_resources is not None:
                if travel_model_resources['travel_model_configuration'].has_key(this_end_year):
                    travel_model_resources['years'] = (this_end_year, this_end_year)
                    self.update_services_database(self.get_run_manager().run_activity, run_id, travel_model_resources)

                    if not self.is_localhost(self.travelmodel_server_config['hostname']):
                        logger.start_block("Start Travel Model on %s from %s to %s" % (self.travelmodel_server_config['hostname'],
                                                                                       this_start_year, this_end_year) )
                        cmd = 'python %(module)s %(run_id)s %(start_year)s --hostname=%(services_hostname)s' % \
                              {'module':self.remote_module_path_from_opus_path(self.get_ssh_client(self.ssh['travelmodel_server'], self.travelmodel_server_config),
                                                                               'opus_core.tools.restart_run'), 
                               'run_id':run_id, 'start_year':this_end_year,
                               'services_hostname': self.services_db_config.host_name}
                        cmd += ' --skip-cache-cleanup --skip-urbansim >> ' + 'travelmodel_run_%s.log' % run_id
                        ## to avoid stdout overfilling sshclient buffer, redirect stdout to a log file                        
                        ## TODO: better handle the location of the travelmodel_remote_run.log
                        logger.log_status("Call " + cmd)
                        try:
                            ssh = self.get_ssh_client(self.ssh['travelmodel_server'], self.travelmodel_server_config)
                            std = ssh.exec_command(cmd)
                        except:
                            raise RuntimeError, "there is a problem running travel model remotely"
                        self.wait_until_run_done_or_failed(run_id, std=std)
                        logger.end_block()
                    else:
                        cmd = 'python %(module)s %(run_id)s %(start_year)s  --hostname=%(services_hostname)s' % \
                              {'module':module_path_from_opus_path('opus_core.tools.restart_run'), 
                               'run_id':run_id, 'start_year':this_end_year,
                               'services_hostname': self.services_db_config.host_name}
                        cmd += ' --skip-cache-cleanup --skip-urbansim'
                        logger.log_status("Call " + cmd)
                        os.system(cmd)
                    
                    flt_directory_for_next_year = os.path.join(cache_directory, str(this_end_year+1))
                    if not self.is_localhost(self.urbansim_server_config['hostname']) and \
                       not exists_remotely(self.get_ssh_client(self.ssh['urbansim_server'], self.urbansim_server_config).open_sftp(), 
                                           pathname2url(flt_directory_for_next_year) ):
                        ##TODO: open_sftp may need to be close()
                        raise StandardError, "travel model didn't create any output for year %s in directory %s on %s; there may be problem with travel model run" % \
                                            (this_end_year+1, cache_directory, self.urbansim_server_config['hostname'])
                    elif not os.path.exists(flt_directory_for_next_year):
                        raise StandardError, "travel model didn't create any output for year %s in directory %s; there may be problem with travel model run" % \
                                            (this_end_year+1, cache_directory)
                
            this_start_year = travel_model_year + 1  #next run starting from the next year of a travel model year

        return

    def wait_until_run_done_or_failed(self, run_id, std=[], msg='\n'):
        while True:
            time.sleep(60)

            #raise if command returns an error in stderr
            if len(std) == 3: 
                line = std[2].readline()
                if line:
                    while line:
                        msg += line
                        line = std[2].readline()
                    for st in std:
                        st.close()
                    raise RuntimeError, "run failed: %s." % msg

            runs_by_status = self.get_run_manager().get_runs_by_status([run_id])            
            if run_id in runs_by_status.get('done', []):
                break
            if run_id in runs_by_status.get('failed', []):
                raise RuntimeError, "run failed: %s." % msg
        
    def update_services_database(self, run_activity, run_id, config):
        run_activity.storage.DoQuery("DELETE FROM run_activity WHERE run_id = %s" % run_id)
        run_activity.add_row_to_history(run_id, config, "started")

    def remote_module_path_from_opus_path(self, ssh, opus_path):
        cmdline = 'python -c "import %s; print %s.__file__"' % (opus_path, opus_path)
        module_path = get_stdout_for_ssh_cmd(ssh, cmdline)
        return module_path

    def is_localhost(self, hostname):
        if (hostname == 'localhost') or (hostname == get_host_name()) or \
            (hostname == socket.gethostname()):
            return True
        return False

    def get_ssh_client(self, ssh_client, ssh_server_config):
        """ return ssh_client if it is active, otherwise,
        if ssh_client passed in is None or is not active, re-create a ssh_client
        from ssh_server_config dict including hostname, username, and password
        """
        if ssh_client is not None and ssh_client._transport.is_active():
            return ssh_client
        
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ssh_server_config['hostname'], 
                       username=ssh_server_config['username'],
                       password=ssh_server_config['password'],
                       pkey=load_key_if_exists())
        #client._transport.set_keepalive(60)
        ssh_client = client
        
        return ssh_client    
    
    def get_run_manager(self):
        """in case the connection to services timeout, reconnect
        """
        try:
            self._run_manager.run_activity.storage.table_exists('run_activity')
        except:  #connection has gone away, re-create run_manager
            db_server = DatabaseServer(self.services_db_config)
            services_db = db_server.get_database(self.services_db_name)
            self._run_manager = RunManager( RunActivity(services_db) )
        return self._run_manager

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    option_group = OptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()

    services_db = option_group.get_services_database(options)
    if not services_db:
        raise RuntimeError, "services database must exist; use --hostname argument to specify the database server containing services database."
    run_manager = option_group.get_run_manager(options)
    
    urbansim_server = options.urbansim_server or os.environ.get('URBANSIMHOSTNAME', 'localhost')
    urbansim_user = options.runserver_username or os.environ.get('URBANSIMUSERNAME', None)
    urbansim_password = os.environ.get('URBANSIMPASSWORD', None)
    
    travelmodel_server = options.travelmodel_server or os.environ.get('TRAVELMODELHOSTNAME', 'localhost')
    travelmodel_user = options.runserver_username or os.environ.get('TRAVELMODELUSERNAME', None)
    travelmodel_password = os.environ.get('TRAVELMODELPASSWORD', None)
    if not (options.configuration_path or options.run_id):
        parser.print_help()
        sys.exit(1)

    run = RemoteRun({'hostname':urbansim_server, 'username':urbansim_user, 'password':urbansim_password}, 
                    {'hostname':travelmodel_server, 'username':travelmodel_user, 'password':travelmodel_password}, 
                    {'hostname':services_db.host_name, 'username':services_db.user_name, 'password':services_db.password, 
                     'database_name':options.database_name},
                    run_manager)
    run.run(configuration_path=options.configuration_path, run_id=options.run_id, 
            start_year=options.start_year, end_year=options.end_year)
    del run

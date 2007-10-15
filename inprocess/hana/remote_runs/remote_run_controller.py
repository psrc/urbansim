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
        self.parser.add_option("--start-year", dest="start_year", default=2001, type="int",
                               help="start year (inclusive)")
        self.parser.add_option("--end-year", dest="end_year", default=2030, type="int",
                               help="end year (inclusive)")
        self.parser.add_option("--run-id", dest="run_id", default=None, 
                               help="which run_id to run, None to start a new run")
        self.parser.add_option("--server", dest="server", default='aalborg', 
                               help="which server to use to run UrbanSim, aalborg or pw")
        
#        self.parser.add_option("--force", dest="force", 
#                               default=False, action="store_true", 
#                               help="force to overwrite pre-existing run_id")

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    option_group = OptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()
#################################################
#required set-up before run
#################################################
    #the same URI mapped to different locations in remote computer (where urbansim runs)
    #and local computer (where this script runs)
    #plink = 'D:/plink.exe'  #location to plink program
    plink = 'plink'
    pscp = 'pscp'
    local_cache_directory_root = 'U:/psrc_parcel/'

    #default_hostname = "aalborg"
    default_hostname = "faloorum6.csss.washington.edu"
    default_username = getpass.getuser()
    #remote_cache_directory_root = '/projects/null/urbansim5/urbansim_cache/' #the ending slash is critical    
    remote_cache_directory_root = '/home/hana/urbansim_cache/psrc/parcel/'
    remote_opus_path = "/home/hana/opus"
    remote_tmp_path = '/home/hana/urbansim_tmp'
    script_path = 'inprocess/hana/remote_runs'

    if options.server == 'pw':
        default_hostname = "128.208.52.233"
        remote_cache_directory_root = '/urbansim_cache/psrc_parcel/' #the ending slash is critical    
    
#################################################
    hostname = raw_input('Hostname [%s]: ' % default_hostname)
    if len(hostname) == 0:
        hostname = default_hostname    
    username = raw_input('Username [%s]: ' % default_username)
    if len(username) == 0:
        username = default_username
    password = getpass.getpass('Password for %s@%s: ' % (username, hostname))

    #this line will be executed in shell and return the absolute path for restart_run.py
    #restart_run_py = r"`python -c \"from opus_core.misc import module_path_from_opus_path; print module_path_from_opus_path('urbansim.tools.restart_run')\"`"
    
    #restart_run_py = "`python -c \"from opus_core.misc import module_path_from_opus_path; print module_path_from_opus_path(\'opus_core.tools.start_run\')\"`"
    #os.system("%s -v -ssh -l %s -pw %s %s python %s/opus_core/tools/start_run.py -c %s" % \
    #                   (plink, username, password, hostname, remote_opus_path, options.configuration_path))

    db = option_group.get_services_database(options)
    if db is None:
        run_manager = RunManager()
    else:
        run_activity = RunActivity(db)
        run_manager = RunManager(run_activity)

    if options.run_id is not None:
        run_id = options.run_id
    else:
        opus_path = options.configuration_path

        config = get_config_from_opus_path(opus_path)

        insert_auto_generated_cache_directory_if_needed(config)

        run_id = run_activity.get_new_history_id()
        head, tail = os.path.split(config['cache_directory'])
        config['cache_directory'] =  os.path.join(head, 'run_' +str(run_id)+'.'+tail)
        config['remote_tmp_path'] = os.path.join(remote_tmp_path, str(run_id))
        pickle_dir = mkdtemp()
        pickle_file_path = os.path.join(pickle_dir, 'resources.pickle')
        write_resources_to_file(pickle_file_path, config)
        
        os.system("%s -v -ssh -l %s -pw %s %s python %s/%s/prepare_communication_directory.py -d %s" % \
                       (plink, username, password, hostname, config['remote_tmp_path']))
        print '%s -v -ssh -l %s -pw %s %s python -c "%s"' % \
                       (plink, username, password, hostname, cmd)
        os.system("%s -v -l %s -pw %s %s %s:%s" % \
                       (pscp, username, password, pickle_file_path, hostname, config['remote_tmp_path']))
        print "%s -v -l %s -pw %s %s %s:%s" % \
                       (pscp, username, password, pickle_file_path, hostname, config['remote_tmp_path'])
        cmd = "python %s/inprocess/hana/remote_runs/create_baseyear_cache.py -r %s/resources.pickle" % (remote_opus_path, 
                                                                                                        config['remote_tmp_path'])
        os.system("%s -v -ssh -l %s -pw %s %s %s" % \
                       (plink, username, password, hostname, cmd))
        print "%s -v -ssh -l %s -pw %s %s %s" % \
                       (plink, username, password, hostname, cmd)


    #check that run_id must exist
    results = run_manager.run_activity.storage.GetResultsFromQuery("SELECT * from run_activity WHERE run_id = %s " % run_id)
    if not len(results) > 1:
        raise StandardError, "run_id %s doesn't exist in run_activity table." % run_id

    urbansim_resources = run_manager.get_resources_for_run_id_from_history(services_host_name=options.host_name,
                                                                           services_database_name=options.database_name,
                                                                           run_id=run_id)
    #TODO: is this line necessary?
    urbansim_resources['flt_directory'] = os.path.join(urbansim_resources['cache_directory'], str(restart_year - 1))
    
    head, tail = os.path.split(urbansim_resources['cache_directory'])
    remote_cache_directory = os.path.join(remote_cache_directory_root, tail)
    local_cache_directory = os.path.join(local_cache_directory_root, tail)

    travel_model_resources = None
    if urbansim_resources.has_key('travel_model_configuration'):
        travel_model_resources = copy.deepcopy(urbansim_resources)
#        del urbansim_resources['travel_model_configuration']
    
    urbansim_resources['cache_directory'] = remote_cache_directory
    travel_model_resources['cache_directory'] = local_cache_directory

    start_year = options.start_year
    end_year = options.end_year
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
            
        run_manager.run_activity.storage.DoQuery("DELETE FROM run_activity WHERE run_id = %s" % run_id)        
        run_manager.run_activity.add_row_to_history(run_id, urbansim_resources, "started")
        
        try:
            os.system("%s -ssh -l %s -pw %s %s python %s %s %s --skip-cache-cleanup --skip-travel-model" % \
                       (plink, username, password, hostname, restart_run_py, run_id, this_start_year))
            
        except:
            raise StandardError, "problem running urbansim remotely"

        if not os.path.exists(os.path.join(local_cache_directory, str(this_end_year))):
            raise StandardError, "cache for year %s doesn't exist in directory %s; there may be problem with urbansim run" % \
                                (this_end_year, local_cache_directory)
        
        if travel_model_resources is not None:
            if travel_model_resources['travel_model_configuration'].has_key(this_end_year):
                for full_model_path in travel_model_resources['travel_model_configuration']['models']:
                    ForkProcess().fork_new_process(full_model_path, 
                        travel_model_resources, optional_args='-y %d' % this_end_year)

        if not os.path.exists(os.path.join(local_cache_directory, str(this_end_year+1))):
            raise StandardError, "travel model didn't create any output for year %s in directory %s; there may be problem with travel model run" % \
                                (this_end_year+1, local_cache_directory)
            
        this_start_year = travel_model_year + 1  #next run starting from the next year of the travel model year

# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys
import pickle
import copy
import getpass
from opus_core.misc import get_config_from_opus_path
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from urbansim.tools.run_manager import RunManager
from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed
from opus_core.fork_process import ForkProcess

class OptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [options]",
            description="Control urbansim and travle model to run on different computers, tailored for PSRC runs ")
        self.parser.add_option("--config", "--configuration-path", dest="configuration_path", default=None, 
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
    plink = 'D:/plink.exe'  #location to plink program
    local_cache_directory_root = 'U:/psrc_parcel/'

    default_hostname = "aalborg"
    default_username = getpass.getuser()
    remote_cache_directory_root = '/projects/null/urbansim5/urbansim_cache/' #the ending slash is critical    

    if options.server == 'pw':
        default_hostname = "128.208.52.233"
        remote_cache_directory_root = '/urbansim_cache/psrc_parcel/' #the ending slash is critical    
    
#################################################
    hostname = input('Hostname [%s]: ' % default_hostname)
    if len(hostname) == 0:
        hostname = default_hostname    
    username = input('Username [%s]: ' % default_username)
    if len(username) == 0:
        username = default_username
    password = getpass.getpass('Password for %s@%s: ' % (username, hostname))

    #this line will be executed in shell and return the absolute path for restart_run.py
    restart_run_py = r"`python -c \"from opus_core.misc import module_path_from_opus_path; print module_path_from_opus_path('urbansim.tools.restart_run')\"`"

    run_manager = RunManager(option_group.get_services_database_configuration(options))

    if options.run_id is not None:
        run_id = options.run_id
    else:
#        if options.pickled_resource_file is not None:
#            f = file(options.pickled_resource_file, 'r')
#            try:
#                config = pickle.load(f)
#            finally:
#                f.close()            
#        elif options.configuration_path is not None:
        opus_path = options.configuration_path
#            try:
        config = get_config_from_opus_path(opus_path)
        config['creating_baseyear_cache_configuration'].cache_directory_root = local_cache_directory_root
#            except ImportError:
#                import_stmt = 'from %s import run_configuration as config' % opus_path
#                exec(import_stmt)
        insert_auto_generated_cache_directory_if_needed(config)
#        else:
#            parser.print_help()
#            sys.exit(1)
        
        run_id = run_manager.prepare_for_run(config)

    #check that run_id must exist
    results = run_manager.storage.GetResultsFromQuery("SELECT * from run_activity WHERE run_id = %s " % run_id)
    if not len(results) > 1:
        raise Exception("run_id %s doesn't exist in run_activity table." % run_id)

    urbansim_resources = run_manager.get_resources_for_run_id_from_history(run_id=run_id)
    #TODO: is this line necessary?
    #urbansim_resources['flt_directory'] = os.path.join(urbansim_resources['cache_directory'], str(restart_year - 1))
    
    head, tail = os.path.split(urbansim_resources['cache_directory'])
    remote_cache_directory = os.path.join(remote_cache_directory_root, tail)
    local_cache_directory = os.path.join(local_cache_directory_root, tail)

    travel_model_resources = None
    if 'travel_model_configuration' in urbansim_resources:
        travel_model_resources = copy.deepcopy(urbansim_resources)
#        del urbansim_resources['travel_model_configuration']
    
    urbansim_resources['cache_directory'] = remote_cache_directory
    travel_model_resources['cache_directory'] = local_cache_directory

    start_year = options.start_year
    end_year = options.end_year
    #only keep sorted travel model years falls into years range
    travel_model_years = []
    for key in list(travel_model_resources['travel_model_configuration'].keys()):
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
    
        run_manager.services_db.execute(
               run_manager.services_db.delete(run_manager.services_db.c.run_id == run_id))
        run_manager.add_row_to_history(run_id, urbansim_resources, "started")
        
        try:
            os.system("%s -ssh -l %s -pw %s %s python %s %s %s --skip-cache-cleanup --skip-travel-model" % \
                       (plink, username, password, hostname, restart_run_py, run_id, this_start_year))
            
        except:
            raise Exception("problem running urbansim remotely")

        if not os.path.exists(os.path.join(local_cache_directory, str(this_end_year))):
            raise Exception("cache for year %s doesn't exist in directory %s; there may be problem with urbansim run" % \
                                (this_end_year, local_cache_directory))
        
        if travel_model_resources is not None:
            if this_end_year in travel_model_resources['travel_model_configuration']:
                for full_model_path in travel_model_resources['travel_model_configuration']['models']:
                    ForkProcess().fork_new_process(full_model_path, 
                        travel_model_resources, optional_args=['-y', this_end_year])

        if not os.path.exists(os.path.join(local_cache_directory, str(this_end_year+1))):
            raise Exception("travel model didn't create any output for year %s in directory %s; there may be problem with travel model run" % \
                                (this_end_year+1, local_cache_directory))
            
        this_start_year = travel_model_year + 1  #next run starting from the next year of the travel model year

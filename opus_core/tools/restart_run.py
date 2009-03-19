# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.services.run_server.run_manager import RunManager

class RestartRunOptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [options] run_id start_year",
               description="Restart run request with given run_id, starting with given start_year")
        self.parser.add_option("--skip-urbansim", dest="skip_urbansim", default=False, 
                                action="store_true", 
                                help="Skip running UrbanSim for the restart year.")
        self.parser.add_option("--create-baseyear-cache-if-not-exists", dest="create_baseyear_cache_if_not_exists", default=False, 
                                action="store_true",
                                help="Create baseyear cache if not already exists")        
        self.parser.add_option("--skip-cache-cleanup", dest="skip_cache_cleanup", 
                                default=False, action="store_true", 
                                help="Skip removing year caches for this and future years.")
                                
if __name__ == "__main__":
    option_group = RestartRunOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()

    run_manager = RunManager(option_group.get_services_database_configuration(options))

    if len(args) < 2:
        parser.print_help()
    else:
        run_id, year = (int(args[0]), int(args[1]))
        run_manager.restart_run(run_id, 
                                year,
                                skip_urbansim=options.skip_urbansim,
                                create_baseyear_cache_if_not_exists=options.create_baseyear_cache_if_not_exists,
                                skip_cache_cleanup=options.skip_cache_cleanup)
                                  

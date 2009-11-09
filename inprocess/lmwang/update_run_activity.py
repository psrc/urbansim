# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import sys
import pickle

from opus_core.misc import get_config_from_opus_path
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.services.run_server.run_manager import RunManager

class OptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [options]",
            description="Update run_activity table in services database with the specified options.")
        self.parser.add_option("-c", "--configuration-path", dest="configuration_path", default=None, 
                               help="Opus path to Python module defining run_configuration.")
        self.parser.add_option("--cache-directory", dest="cache_directory", default=None, 
                               help="cache directory")
        self.parser.add_option("--run-id", dest="run_id", default=None, 
                               help="which run_id to update")
        self.parser.add_option("--force", dest="force", 
                               default=False, action="store_true", 
                               help="force to overwrite pre-existing run_id")
        

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    option_group = OptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()

    run_manager = RunManager(option_group.get_services_database_configuration(options))

    if options.configuration_path is not None:
        opus_path = options.configuration_path
        try:
            config = get_config_from_opus_path(opus_path)
        except ImportError:
            import_stmt = 'from %s import run_configuration as config' % opus_path
            exec(import_stmt)
    config['cache_directory'] = options.cache_directory
    
    results = run_manager.storage.GetResultsFromQuery("SELECT * from run_activity WHERE run_id = %s " % options.run_id)

    if len(results) > 1 and not options.force:
        print "WARNING: run_id %s exists in run_activity. Use --force to override." % options.run_id
        sys.exit()
    elif options.force:
        run_manager.services_db.execute(
               run_manager.services_db.delete(run_manager.services_db.c.run_id == options.run_id))
    run_manager.add_row_to_history(options.run_id, config, "started")
    
    
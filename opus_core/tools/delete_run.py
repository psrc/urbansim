# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.services.run_server.run_manager import RunManager
from opus_core.services.run_server.generic_option_group import GenericOptionGroup

class StartRunOptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [options] configuration",
            description="Delete results of a simulation run.")
        self.parser.add_option("--run-id", dest="run_id", default=None, 
                                action="store", 
                                help="The simulation run to delete.")
        self.parser.add_option("--years-to-delete", dest="years_to_delete", 
                                default=None, action="store", 
                                help="Python expression specifying list of years to delete from the simulation's cache.")

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    option_group = StartRunOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()

    
    run_manager = RunManager(option_group.get_services_database_configuration(options))

    if options.run_id is None:
        parser.print_help()
    elif options.years_to_delete:
        years_to_delete = eval(options.years_to_delete)
        if not isinstance(years_to_delete, list):
            years_to_delete = [years_to_delete]
        run_manager.delete_year_dirs_in_cache(options.run_id, 
                                                 years_to_delete=years_to_delete)
    else:
        run_manager.delete_everything_for_this_run(options.run_id)

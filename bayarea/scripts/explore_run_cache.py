# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from opus_core.paths import get_opus_data_path_path
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.services.run_server.run_manager import RunManager

class OptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [-p project_name -r run_id] [-d run_directory] year",
               description="explore cache. See examples at the end of this script")
        self.parser.add_option("-p", "--project-name", dest="project_name", 
                                default='',help="The project name")
        self.parser.add_option("-r", "--run-id", dest="run_id", 
                                default='',help="run id")
        self.parser.add_option("-o", "--package-order", dest="package_order", 
                               default="['bayarea', 'urbansim_parcel', 'urbansim', 'opus_core']",
                               help="package order")
        self.parser.add_option("-d", "--run-directory", dest="run_directory", 
                                default='',help="run directory, e.g. opus/data/bay_area_parcel/runs/run_xxx.xxxx")
        self.parser.add_option("-y", "--year", dest="year", default=None, 
                                help="year")

if __name__ == "__main__":
    option_group = OptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()

    cache_directory = None
    package_order = None
    if options.run_id:
        run_id = int(options.run_id)
        if not options.project_name:
            print("project_name argument is required when using run_id")
            sys.exit(0)
        else:
            run_manager = RunManager(option_group.get_services_database_configuration(options))
            if options.project_name:
                run_manager.update_environment_variables(run_resources={'project_name':options.project_name}) 
            resources = run_manager.get_resources_for_run_id_from_history(run_id=run_id)
            cache_directory = resources['cache_directory']
            package_order = resources['dataset_pool_configuration'].package_order

    if options.run_directory:
        _cache_directory = options.run_directory
        if cache_directory is not None:
            print("Both run-directory and run-id specified; use run directory %s" % cache_directory)
        else:
            cache_directory = _cache_directory

    try:
        year = int(options.year)
    except IndexError:
        parser.error("year must be provided.")
        parser.print_help()
        sys.exit(1)

    if package_order is None:
        package_order = eval(options.package_order)


    st = SimulationState()
    st.set_current_time(year)
    st.set_cache_directory(cache_directory)
    attribute_cache = AttributeCache()
    dp = SessionConfiguration(new_instance=True,
                              package_order=package_order,
                              in_storage=attribute_cache
                              ).get_dataset_pool()

    
    ## example usage:
    # python -i explore_run_cache.py -p bay_area_parcel -r 105 2025
    # >>> h2025 = dp.get_dataset('household')
    # >>> children_5yr = h2025.compute_variables('household.aggregate(person.age <= 5)')

    # python -d /workspace/opus/data/bay_area_parcel/base_year_data 2010
    # >>> h2010 = dp.get_dataset('household')
    # >>> children_5yr = h2010.compute_variables('household.aggregate(person.age <= 5)')

    # python -d /workspace/opus/data/bay_area_parcel/base_year_data -o ['bayarea','urbansim_parcel','urbansim'] 2010
    # >>> h2010 = dp.get_dataset('household')
    # >>> children_5yr = h2010.compute_variables('household.aggregate(person.age <= 5)')


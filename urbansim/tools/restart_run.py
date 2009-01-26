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

from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from urbansim.tools.run_manager import RunManager

class RestartRunOptionGroup(GenericOptionGroup):
    """same as restart_run in opus_core, but with additional switch --skip-travel-model
    use run_manager in urbansim/tools instead of the one in opus_core/tools"""
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [options] run_id start_year",
               description="Restart run request with given run_id, starting with given start_year")
        self.parser.add_option("--skip-urbansim", dest="skip_urbansim", default=False, 
                                action="store_true", 
                                help="Skip running UrbanSim for the restart year.")
        self.parser.add_option("--skip-travel-model", dest="skip_travel_model", default=False, 
                                action="store_true", 
                                help="Skip running travel model for the any year.")
        self.parser.add_option("--skip-cache-cleanup", dest="skip_cache_cleanup", 
                                default=False, action="store_true", 
                                help="Skip removing year caches for this and future years.")
        self.parser.add_option("--project-name", dest="project_name", 
                                default='misc', action="store_true", 
                                help="The name of the project that the restarted run is part of (e.g. eugene_gridcell)")                                
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
                                project_name = options.project_name,
                                skip_urbansim=options.skip_urbansim,
                                skip_travel_model=options.skip_travel_model,
                                skip_cache_cleanup=options.skip_cache_cleanup)
                                  

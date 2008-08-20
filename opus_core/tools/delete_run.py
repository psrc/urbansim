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

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

import sys
import pickle

from opus_core.misc import get_config_from_opus_path
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.services.run_server.run_manager import insert_auto_generated_cache_directory_if_needed


class StartRunOptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [options]",
            description="Starts running the specified configuration.")
        self.parser.add_option("-r", "--pickled-resource-file", dest="pickled_resource_file", default=None, 
                                help="Opus path to pickled configuration file.")
        self.parser.add_option("-c", "--configuration-path", dest="configuration_path", default=None, 
                                help="Opus path to Python module defining run_configuration.")
        self.parser.add_option("--directory-to-cache", dest="existing_cache_to_copy", default=None, 
                                help="Directory containing data to put in new cache.")
        self.parser.add_option("--years-to-cache", dest="years_to_cache", default=None, 
                                help="List of years of data to take from the directory-to-cache (default is all years).")                   

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    option_group = StartRunOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()

    run_manager = option_group.get_run_manager(options)

    if options.pickled_resource_file is not None:
        f = file(options.pickled_resource_file, 'r')
        try:
            config = pickle.load(f)
        finally:
            f.close()
            
    elif options.configuration_path is not None:
        opus_path = options.configuration_path
        try:
            config = get_config_from_opus_path(opus_path)
        except ImportError:
            # TODO: Once all fully-specified configurations are stored as classes,
            #       get rid of this use.
            import_stmt = 'from %s import run_configuration as config' % opus_path
            exec(import_stmt)
        insert_auto_generated_cache_directory_if_needed(config)
    else:
        parser.print_help()
        sys.exit(1)
        
    if options.existing_cache_to_copy is not None:
        config['creating_baseyear_cache_configuration'].cache_from_mysql = False
        config['creating_baseyear_cache_configuration'].baseyear_cache = BaseyearCacheConfiguration(
            existing_cache_to_copy = options.existing_cache_to_copy,
            )
        if options.years_to_cache is not None:
            config['creating_baseyear_cache_configuration'].baseyear_cache.years_to_cache = eval(options.years_to_cache)

    run_manager.run_run(config)
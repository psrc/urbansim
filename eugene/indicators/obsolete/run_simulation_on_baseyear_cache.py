# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
import sys
import wx

from time import strftime, localtime

from enthought.traits.api import HasTraits, Directory, Str, Event, Int
from opus_core.traits_ui.api import View, Group, Item
# later update the ui import to:   from enthought.traits.ui.api import View, Group, Item
from enthought.traits.ui.menu import Action, NoButtons

from opus_core.fork_process import ForkProcess
from opus_core.misc import create_import_for_camel_case_class
from opus_core.indicator_framework.utilities.gui_utilities import display_message_dialog


class RunSimulationOnCacheConfig(HasTraits):
    filesystem_path_to_baseyear_cache = Directory
    opus_classpath_of_configuration = Str('eugene.configs.baseline')
    output_directory = Directory
    number_of_years_to_run = Int(2)
    
    filesystem_path_to_baseyear_cache_help = (r"The filesystem path to the "
        r"baseyear cache directory that contains the year directories, "
        r"e.g. 'C:\urbansim_cache\eugene_1980_baseyear_cache'.")
    opus_classpath_of_configuration_help = (r"The configuration to be used, "
        r"e.g. 'eugene.configs.baseline'.")
    output_directory_help = (r"The directory in which to create a new cache to "
        r"contain the simulation results, e.g. 'C:\urbansim_cache'. The output "
        r"will be in a directory labeled with a timestamp, e.g. "
        r"'C:\urbansim_cache\%s'. A unique run id may also be prepended to the "
        r"timestamp if the appropriate services database has been set up."
            % strftime('%Y_%m_%d_%H_%M',localtime()))
    
    view = View(
            Group(
                Item('filesystem_path_to_baseyear_cache', label='Get baseyear data from this cache directory', width=400, help=filesystem_path_to_baseyear_cache_help),
                Item('opus_classpath_of_configuration', label='Use this configuration', width=400, help=opus_classpath_of_configuration_help),
                Item('output_directory', label='Create the output cache in this directory', width=400, help=output_directory_help),
                Item('number_of_years_to_run', width=-30),
                ),
            ok=True, apply=False, undo=False, revert=False, help=False,
            title='Run UrbanSim Simulation on Baseyear Cache',
            kind='modal',
        )
    
    
if __name__ == '__main__':
    try: import wingdbstub
    except: pass
    
    args = RunSimulationOnCacheConfig()
    
    ok_button = args.configure_traits()
    
    if not ok_button:
        sys.exit(1)
        
    ### TODO: We depend on subpackages (like string) that die if you use unicode.
    ###         A lot of places in the code, too, use isinstance(x, str) and ignore
    ###         the unicode case.
    cache_dir = str(args.filesystem_path_to_baseyear_cache)
    classpath = str(args.opus_classpath_of_configuration)
    output_dir_container = str(args.output_directory)
    output_dir = os.path.join(output_dir_container, strftime('%Y_%m_%d_%H_%M',localtime()))
    years_to_run = args.number_of_years_to_run
    
    exec(create_import_for_camel_case_class(classpath, 
        import_as='ImportedConfiguration'), globals())
    
    config = ImportedConfiguration()
    
    base_year = config['base_year']
    
    config['creating_baseyear_cache_configuration'].cache_from_database = False
    config['creating_baseyear_cache_configuration'].baseyear_cache.existing_cache_to_copy = cache_dir
    config['cache_directory'] = output_dir
    config['years'] = (base_year+1, base_year+years_to_run)

    if not len(list(range(config['years'][0], config['years'][1]+1))) > 0:
        display_message_dialog('No years to simulate!')
        sys.exit(1)
        
    # sanity check on the cache directory -- make sure it includes a subdirectory whose name is the base year
    base_year_directory = os.path.join(cache_dir, str(base_year))
    if not os.path.exists(base_year_directory):
        msg = 'Invalid cache directory: %s\nThe cache directory should have a subdirectory %d for the base year' % (cache_dir, base_year)
        display_message_dialog(msg)
        sys.exit(1)
    
    # sanity check on the output directory 
    if output_dir_container=='':
        msg = 'Output directory not specified'
        display_message_dialog(msg)
        sys.exit(1)
    
    ForkProcess().fork_new_process('opus_core.tools.start_run', resources=config)
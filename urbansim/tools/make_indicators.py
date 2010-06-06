# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import sys, pickle
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_gui.main.opus_project import OpusProject
from opus_gui.results_manager.results_manager_functions import get_batch_configuration

class MakeIndicatorsOptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [options]",
            description="""Make indicators by processing indicator_batch in the specified configuration.

            Example:
            python urbansim/tools/make_indicators.py -x ../project_configs/seattle_parcel_default.xml -i untitled_indicator_batch -y "(2000,)" -c /workspace/urbansim_cache/seattle_parcel/base_year_data/
            
            python urbansim/tools/make_indicators.py -x ../project_configs/seattle_parcel_default.xml -i untitled_indicator_batch -y "(2000,)" -r base_year_data
            
            python urbansim/tools/make_indicators.py -x ../project_configs/seattle_parcel_default.xml -i untitled_indicator_batch -y "arange(2000,2030,1)" -r baseline_run            
            """)
        self.parser.remove_option('--services_database')
        self.parser.remove_option('--database_configuration')        
        self.parser.add_option("-x", "--xml-configuration", dest="xml_configuration", default=None, 
                                help="File name of xml configuration")
        self.parser.add_option("-i", "--indicator-batch", dest="indicator_batch", default=None, 
                                help="Name of the indicator_batch in the specified xml configuration")
        self.parser.add_option("-c", "--cache-directory", dest="cache_directory", default=None, 
                                help="Directory of UrbanSim cache to make indicators from")
        self.parser.add_option("-r", "--run-name", dest="run_name", default=None, 
                                help="")
        self.parser.add_option("-y", "--years", dest="years", 
                                help="List of years to make indicators for.")
        

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    option_group = MakeIndicatorsOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()
    
    if not (options.xml_configuration and
            options.indicator_batch and
            ( options.cache_directory or 
              options.run_name) and
            options.years
            ):
        parser.print_help()
        sys.exit(0)
    
    from opus_gui.results_manager.run.batch_processor import BatchProcessor
    project = OpusProject()
    project.open(options.xml_configuration)
    bp = BatchProcessor(project)
    visualizations = get_batch_configuration(project = project,
                                             batch_name = options.indicator_batch)
    
    bp.set_data(visualizations=visualizations,
                source_data_name = options.run_name,
                cache_directory = options.cache_directory,
                years = eval(options.years),
                )
    bp.errorCallback = lambda x: x     ## 
    bp.finishedCallback = lambda x: x  ## hack to work around BatchProcessor
    bp.run()

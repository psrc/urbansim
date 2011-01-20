# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# script to produce a number of PSRC indicators -- 
# this illustrates using traits-based configurations programatically

from opus_core.resources import Resources
from opus_core.variables.variable_name import VariableName
from opus_core.simulation_state import SimulationState
from opus_core.dataset_factory import DatasetFactory
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration


class BatchMakeIndicator(object):
    def run(self, resources, year):
        cache_directory = config['cache_directory']
        simulation_state = SimulationState()
        simulation_state.set_cache_directory(cache_directory)
        simulation_state.set_current_time(year)
        attribute_cache = AttributeCache()
        SessionConfiguration(new_instance=True,
                             in_storage=AttributeCache())
                             
        arguments = {'in_storage':attribute_cache}
        gc_set = DatasetFactory().get_dataset('gridcell', package='urbansim', 
                                              arguments=arguments)

        runs = {
        #r'X:\urbansim_cache\run_1713.2007_01_03_11_16':r'(run 1713 - baseline)',
        #r'X:\urbansim_cache\run_1714.2007_01_03_11_20':r'(run 1714 - no ugb)',
        #r'X:\urbansim_cache\run_1731.2007_01_03_11_16':r'(run 1731 - no build)',
        
                r'X:\urbansim_cache\run_1847.2007_01_15_15_23':r'(run 1847 - no UGB 1/17/2007)',
                r'X:\urbansim_cache\run_1848.2007_01_15_15_40':r'(run 1848 - no UGB+1.5xhighway 1/17/2007)',
        #        r'X:\urbansim_cache\run_1849.2007_01_15_16_09':r'(run 1849 - baseline 1/17/2007)',
                r'V:\psrc\run_1850.2007_01_15_17_03':r'(run 1850 - baseline 1/17/2007)',
                r'V:\psrc\run_1851.2007_01_15_17_07':r'(run 1851 - no build 1/17/2007)'
                }
        
        #baseline = r'X:\urbansim_cache\run_1713.2007_01_03_11_16'
        baseline = r'V:\psrc\run_1850.2007_01_15_17_03'
        
        comparison_variables = {'gridcell': ['urbansim.gridcell.population',
                                             'urbansim.gridcell.number_of_jobs'],
                                'faz':['urbansim.faz.population',
                                       'urbansim.faz.number_of_jobs'], 
                                 }
        #datasets_to_preload = {
        #                'gridcell':{ 'nchunks':2},
        #                'household':{},
        #                'job':{},
        #                'zone':{},
        #                'faz':{},
        #                'development_type':{},
        #                'development_event_history':{},
        #                'development_constraint':{},
        #                'job_building_type':{},
        #                'urbansim_constant':{},
        #                }
        
        year = 2025
        
        simulation_state = SimulationState()
        simulation_state.set_current_time(year)
        
        SessionConfiguration(new_instance=True,
                             package_order=['psrc','urbansim','opus_core'],
                             in_storage=AttributeCache())
        
        #cache_storage = AttributeCache().get_flt_storage_for_year(year_for_base_year_cache)
        #datasets = DatasetFactory().create_datasets_from_flt(datasets_to_preload,
        #                                                    "urbansim",
        #                                                    additional_arguments={'in_storage': AttributeCache()})
        
        variable_augment = False
        if variable_augment == True:
            for dataset_name in comparison_variables.keys():
                cache_directory = baseline
                simulation_state.set_cache_directory(cache_directory)
                dataset = DatasetFactory().get_dataset(dataset_name,
                                                        package='urbansim', 
                                                        arguments={'in_storage': AttributeCache()})
            
                variables = comparison_variables[dataset_name]
                dataset.compute_variables(variables, resources=Resources())
                ids = dataset.get_id_attribute()
                for run in runs.keys():
                    cache_directory=run
                    simulation_state.set_cache_directory(cache_directory)
                    run_dataset = DatasetFactory().get_dataset(dataset_name, 
                                                               package='urbansim', 
                                                               arguments={'in_storage': AttributeCache()})
                    match_index = run_dataset.get_id_index(ids)
                    for variable in variables:
                        short_name = VariableName(variable).alias()
                        attribute = dataset.get_attribute(short_name)
                        run_dataset.add_attribute(attribute[match_index],'baseline_'+short_name,metadata=1)
                        run_dataset.flush_attribute('baseline_'+short_name)
                    
                    SessionConfiguration().get_dataset_pool().remove_all_datasets()
        
        #indicators_module = args[0]
        #eval("from %s import config" % indicators_module)
        from make_indicators_openev import config
        from urbansim.indicators.indicator_configuration_handler_batch_mode import generate_indicators
        #from make_indicators_openev import config
        #from inprocess.travis.urbansim.indicators.indicator_configuration_handler_batch_mode import generate_indicators
        for run, descriptin in runs.iteritems():
            config.request_years = [year]
            config.cache_directory = run
            config.run_description = descriptin
            generate_indicators(config)        
    
if __name__ == "__main__":
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file 
    from opus_core.file_utilities import write_resources_to_file
    from opus_core.store.attribute_cache import AttributeCache
    from opus_core.fork_process import ForkProcess
    
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    (options, args) = parser.parse_args()
    
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))
    
    SessionConfiguration(new_instance=True,
                         package_order=resources['dataset_pool_configuration'].package_order,                         
                         in_storage=AttributeCache())

    logger.enable_memory_logging()
    BatchMakeIndicators().run(resources, options.year)
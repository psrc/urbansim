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
from optparse import OptionParser
from opus_core.misc import convert_lower_case_with_underscores_into_camel_case
from inprocess.travis.urbansim.indicators.indicator_configuration_handler_batch_mode import generate_indicators

class Runs(object):
    runs = {
            #r'V:\psrc\zonal_simulation\2007_01_20_16_41_baseline':r'(baseline)',
            #r'V:\psrc\zonal_simulation\2007_01_20_16_41_baseline_discounted_travel_data':r'(discounted_travel_data)',
            #r'V:\psrc\zonal_simulation\2007_01_20_16_41_baseline_inflated_travel_data':r'(inflated_travel_data)',

            r'X:\urbansim_cache\psrc_gridcell\2007_01_21_09_43_baseline':r'(baseline)',
            r'X:\urbansim_cache\psrc_gridcell\2007_01_21_09_43_discounted_travel_data':r'(discounted_travel_data)',
            r'X:\urbansim_cache\psrc_gridcell\2007_01_21_09_43_inflated_travel_data':r'(inflated_travel_data)',

    
#            r'X:\urbansim_cache\run_1847.2007_01_15_15_23':r'(run 1847 - no UGB 1/17/2007)',
#            r'X:\urbansim_cache\run_1848.2007_01_15_15_40':r'(run 1848 - no UGB+1.5xhighway 1/17/2007)',
#    #        r'X:\urbansim_cache\run_1849.2007_01_15_16_09':r'(run 1849 - baseline 1/17/2007)',
#            r'V:\psrc\run_1850.2007_01_15_17_03':r'(run 1850 - baseline 1/17/2007)',
#            r'V:\psrc\run_1851.2007_01_15_17_07':r'(run 1851 - no build 1/17/2007)'


            }
    
#    baseline = r'X:\urbansim_cache\run_1713.2007_01_03_11_16'
    baseline = r'X:\urbansim_cache\psrc_gridcell\2007_01_21_09_43_baseline'


    comparison_variables = {'gridcell': ['urbansim.gridcell.population',
                                         'urbansim.gridcell.number_of_jobs'],
                            'faz':['urbansim.faz.population',
                                   'urbansim.faz.number_of_jobs'], 
                             }

if __name__ == "__main__":    
    parser = OptionParser()
    parser.add_option("-a", "--augment-variables", dest="augment_variables", action="store_true",
                      help="model name")
    parser.add_option("-c", "--indicator-config", dest="indicator_config", action="store", 
                      type="string", help="model name")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="end year")
    (options, args) = parser.parse_args()

    runs = Runs.runs
    comparison_variables = Runs.comparison_variables
    baseline = Runs.baseline
    
    simulation_state = SimulationState()
    simulation_state.set_current_time(options.year)
    
    SessionConfiguration(new_instance=True,
                         package_order=['psrc','urbansim','opus_core'],
                         in_storage=AttributeCache())

    if options.augment_variables == True:
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
    
    if options.indicator_config is not None:
        opus_path = options.indicator_config
        try:
            class_name = opus_path.split('.')[-1]
            class_name = convert_lower_case_with_underscores_into_camel_case(class_name)
            import_stmt = 'from %s import %s as config_class' % (opus_path, class_name)
            exec(import_stmt)
            is_class = True
        except ImportError:
            # TODO: Once all fully-specified configurations are stored as classes,
            #       get rid of this use.
            import_stmt = 'from %s import config' % opus_path
            exec(import_stmt)
            is_class = False
    else:
        parser.print_help()
        sys.exit(1)

    for run, description in Runs.runs.iteritems():
        if is_class:
            args = {"base_year":2000, 
                    "cache_directory":run,
                    "description":description,
                     }
            config = config_class(args, options.year)
        else:
            config.request_years = [options.year]
            config.cache_directory = run
            config.run_description = description
        generate_indicators(config)            
    

#indicators_module = args[0]
#eval("from %s import config" % indicators_module)
#from make_indicators_add import config
#from urbansim.indicators.indicator_configuration_handler_batch_mode import generate_indicators
#from make_indicators_openev import config
#from inprocess.psrc_zone.configs.indicator_config import IndicatorConfig
#config = IndicatorConfig({"base_year":2000, 
#                          "cache_directory":run,
#                          "description":description,
#                         }, year)

#for run, description in runs.iteritems():
#    config.request_years = [year]
#    config.cache_directory = run
#    config.run_description = description
#    generate_indicators(config)
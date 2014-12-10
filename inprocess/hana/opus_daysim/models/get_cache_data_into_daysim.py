# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
from shutil import copy
from numpy import where
from opus_core.session_configuration import SessionConfiguration
from opus_core.resources import Resources
from opus_core.simulation_state import SimulationState
from opus_core.storage_factory import StorageFactory
from opus_core.store.storage import Storage
from opus_core.logger import logger
from opus_core.variables.variable_name import VariableName
from opus_core.store.attribute_cache import AttributeCache
from opus_core.datasets.dataset import DatasetSubset
from inprocess.hana.opus_daysim.models.abstract_daysim_travel_model import AbstractDaysimTravelModel
from opus_core.configurations.xml_configuration import XMLConfiguration
        
class GetCacheDataIntoDaysim(AbstractDaysimTravelModel):
    """Get needed Daysim data from UrbanSim cache into inputs for travel model.
    """

    def run(self, year, cache_directory=None):
        """The class is initialized with the appropriate configuration info from the 
        travel_model_configuration part of this config, and then copies the specified 
        UrbanSim data into files for daysim to read.
        The variables/expressions to export are defined in the node travel_model_configuration/urbansim_to_tm_variable_mapping
        of the configuration file.
        """
        if cache_directory is None:
            cache_directory = self.config['cache_directory']
        simulation_state = SimulationState()
        simulation_state.set_cache_directory(cache_directory)
        simulation_state.set_current_time(year)
        attribute_cache = AttributeCache()
        sc = SessionConfiguration(new_instance=True,
                                  package_order=self.config['dataset_pool_configuration'].package_order,
                                  in_storage=attribute_cache)
        dataset_pool = sc.get_dataset_pool()
        tm_config = self.config['travel_model_configuration']
        data_to_export = tm_config['urbansim_to_tm_variable_mapping']
        
        table_names = data_to_export.keys()
        variable_names = {}
        datasets = {}
        filenames = {}
        in_table_names = {}
        for table_name in table_names:
            filter = data_to_export[table_name].get('__filter__', None)
            if filter is not None:
                del data_to_export[table_name]['__filter__']
            out_table_name = data_to_export[table_name].get('__out_table_name__', None)
            if out_table_name is not None:
                del data_to_export[table_name]['__out_table_name__']
            else:
                out_table_name = table_name
            variables_to_export = map(lambda alias: "%s = %s" % (alias, data_to_export[table_name][alias]), data_to_export[table_name].keys())
            dataset_name = None            
            for var in variables_to_export:
                var_name = VariableName(var)
                if dataset_name is None:
                    dataset_name = var_name.get_dataset_name()
                    ds = dataset_pool.get_dataset(dataset_name)
                    
                    datasets[dataset_name] = ds
                    filenames[dataset_name] = out_table_name
                    in_table_names[dataset_name] = table_name
                    if dataset_name not in variable_names.keys():
                        variable_names[dataset_name] = []
                variable_names[dataset_name].append(var_name.get_alias())                
                ds.compute_variables([var_name], dataset_pool=dataset_pool)
            if filter is not None:
                filter_idx = where(ds.compute_variables(["__filter__ = %s" % filter], dataset_pool=dataset_pool)>0)[0]
                ds = DatasetSubset(ds, index = filter_idx)
                datasets[dataset_name] = ds
                
        return self._call_input_file_writer(year, datasets, in_table_names, filenames, variable_names, dataset_pool)

    def _call_input_file_writer(self, year, datasets, in_table_names, out_table_names, variable_names, dataset_pool):
        current_year_tm_dir = self.get_daysim_dir(year)
        file_config = self.config['travel_model_configuration'].get('daysim_file', {})
        file_format = file_config.get('format', 'tab')
        if(file_format == 'hdf5g'):
            current_year_tm_dir = os.path.join(current_year_tm_dir, file_config.get('name', 'daysim_inputs.hdf5'))
        meta_data = self.config['travel_model_configuration'].get('meta_data', {})
        storage = StorageFactory().get_storage('%s_storage' % file_format, storage_location = current_year_tm_dir)
        kwargs = {}
        mode={file_format: Storage.OVERWRITE}
        if file_format == 'csv' or file_format == 'tab' or file_format == 'tsv':
            kwargs['append_type_info'] = False
        if file_format.startswith('hdf5'):
            kwargs['compression'] = file_config.get('hdf5_compression', None) 
        logger.start_block('Writing Daysim inputs.')
        for dataset_name, dataset in datasets.iteritems():
            ds_meta = meta_data.get(in_table_names[dataset_name], {})
            if file_format.startswith('hdf5'):
                kwargs['column_meta']  = ds_meta
            attr_vals = {}
            for attr in variable_names[dataset_name]:
                attr_vals[attr] = dataset[attr]
            storage.write_table(table_name = out_table_names[dataset_name], table_data = attr_vals, mode = mode[file_format], **kwargs)
            mode['hdf5g'] = Storage.APPEND
        logger.end_block()
        logger.log_status('Daysim inputs written into %s' % current_year_tm_dir)
        return out_table_names.values()
    
if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string", default = None,
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    parser.add_option("-o", "--output", dest="output_directory", action="store", type="string", default=None,
                      help="Copy resulting files into this directory.")
    parser.add_option("-x", "--xml-configuration", dest="xml_configuration", default = None,
                               action="store", help="Full path to an XML configuration file (must also provide a scenario name using -s). Either -x or -r must be given.")
    parser.add_option("-s", "--scenario_name", dest="scenario_name", default=None, 
                                help="Name of the scenario. Must be given if option -x is used.")
    parser.add_option("-d", "--directory", dest="cache_directory", default = None,
                               action="store", help="Cache directory with urbansim output.")
    (options, args) = parser.parse_args()
    if options.year is None:
        raise StandardError, "Year (argument -y) must be given."
    if (options.scenario_name is None) and (options.xml_configuration is not None):
        raise StandardError, "No scenario given (argument -s). Must be specified if option -x is used."
    r = None
    xconfig = None
    if options.resources_file_name is not None:
        r = get_resources_from_file(options.resources_file_name)
        resources = Resources(get_resources_from_file(options.resources_file_name))
    elif options.xml_configuration is not None:
        xconfig = XMLConfiguration(options.xml_configuration)
        resources = xconfig.get_run_configuration(options.scenario_name)
    else:
        raise StandardError, "Either option -r or -x must be used."
        
    files = GetCacheDataIntoDaysim(resources).run(options.year, cache_directory=options.cache_directory)
    if options.output_directory is not None:
        for file in files:
            copy(file, options.output_directory)
        logger.log_status('Files copied into %s' % options.output_directory)
        
# For a test run, use options
# -x opus_daysim/configs/sample_daysim_configuration.xml -s daysim_scenario -d opus_core/data/test_cache -y 1980

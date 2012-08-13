# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
import numpy as np
from numpy import array
from pandas import read_csv
from opus_core.logger import logger, log_block, block
from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset import Dataset
from opus_core.store.attribute_cache import AttributeCache
from opus_core.storage_factory import StorageFactory
import mtc_common

def to_opus_dataset(df, out_store, table_name):
    data_dict = {}
    id_names = df.index.names
    if id_names is None or id_names == [None]:
        id_names = []
    else:
        df = df.reset_index()
    for name in df.columns:
        data_dict[name] = df[name].values
    in_store = StorageFactory().get_storage('dict_storage')
    in_store.write_table(table_name=table_name,
                        table_data=data_dict) 
    opus_ds = Dataset(in_storage=in_store,
                    in_table_name=table_name,
                    id_name=id_names,
                    dataset_name='dataset')
    opus_ds.write_dataset(attributes='*', out_storage=out_store,
                          out_table_name=table_name)
    return opus_ds

@log_block()
def import_travel_model_data(config, year):

    cache_directory = config['cache_directory']
    simulation_state = SimulationState()
    simulation_state.set_current_time(year)
    simulation_state.set_cache_directory(cache_directory)
    out_store = AttributeCache().get_flt_storage_for_year(year+1)
    out_store_loc = out_store.get_storage_location()

    tm_config = config['travel_model_configuration']
    data_to_import = tm_config['tm_to_urbansim_variable_mapping'] 
    base_dir = mtc_common.tm_get_base_dir(config)
    data_dir = tm_config[year]['data_dir']

    for dataset_name, skim_file in data_to_import.iteritems():
        skim_file = os.path.join(base_dir, data_dir, skim_file)
        data = read_csv(skim_file, header=0)
        
        with block("Caching {} to {}".format(dataset_name, out_store_loc)):
            logger.log_status("Source file {}".format(skim_file))
            opus_ds = to_opus_dataset(data, out_store, dataset_name)

if __name__ == '__main__':
    from optparse import OptionParser
    from opus_core.resources import Resources
    from opus_core.file_utilities import get_resources_from_file
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", 
                      action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    (options, args) = parser.parse_args()
    resources = Resources(get_resources_from_file(options.resources_file_name))

    import_travel_model_data(resources, options.year)    

# Opus/UrbanSim urban simulation software.
# Copyright (C) 2012 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os, glob, shutil
from opus_core.logger import logger, block, log_block
from opus_core.session_configuration import SessionConfiguration
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.store.csv_storage import csv_storage
from opus_core.variables.variable_name import VariableName
import mtc_common

flip_urbansim_to_tm_variable_mappling = True

@log_block()
def export_opus_data(config, year):
    """ 
    # This script prepares the TazData, PopSynHousehold, PopSynPerson, and
    # WalkAccessBuffers from opus bay area land use model output.
    #
    # The MTC travel model input specifications can be found here:
    # http://mtcgis.mtc.ca.gov/foswiki/Main/DataDictionary

    """

    cache_directory = config['cache_directory']
    simulation_state = SimulationState()
    simulation_state.set_cache_directory(cache_directory)
    simulation_state.set_current_time(year)
    attribute_cache = AttributeCache()
    package_order=config['dataset_pool_configuration'].package_order
    dataset_pool = SessionConfiguration(new_instance=True,
                                        package_order=package_order,
                                        in_storage=attribute_cache
                                       ).get_dataset_pool()

    out_dir = os.path.join(cache_directory, "mtc_data")
    tm_config = config['travel_model_configuration']
    data_to_export = tm_config['urbansim_to_tm_variable_mapping'] 
    out_storage = csv_storage(storage_location=out_dir)
    for data_fname, variable_mapping in data_to_export.iteritems():
        if not flip_urbansim_to_tm_variable_mappling:
            col_names = variable_mapping.values()
            variables_aliases = ["=".join(mapping[::-1]) for mapping in \
                                 variable_mapping.iteritems()]
        else:
            col_names = variable_mapping.keys()
            variables_aliases = ["=".join(mapping) for mapping in \
                                 variable_mapping.iteritems()]

        dataset_name = VariableName(variables_aliases[0]).get_dataset_name()
        dataset = dataset_pool.get_dataset(dataset_name)
        dataset.compute_variables(variables_aliases)
        #data = {} 
        #data_file = os.path.join(out_dir, data_fname)
        #for col_name, variable in zip(col_names, variables):
            #    data[col_name] = dataset[variable]

        org_fname = os.path.join(out_dir, "%s.computed.csv" % data_fname)
        new_fname = os.path.join(out_dir, "%s%s.csv" % (year,data_fname))
        block_msg = "Writing {} for travel model to {}".format(data_fname,
                                                               new_fname)
        with block(block_msg):
            dataset.write_dataset(attributes=col_names,
                                out_storage=out_storage,
                                out_table_name=data_fname)
            #rename & process header
            shutil.move(org_fname, new_fname)
            os.system("sed 's/:[a-z][0-9]//g' -i %s" % new_fname)

if __name__ == "__main__":
    try:import wingdbstub
    except:pass
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

    export_opus_data(resources, options.year)    


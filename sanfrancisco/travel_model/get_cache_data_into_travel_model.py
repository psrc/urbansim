# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os
from opus_core.logger import logger
from numpy import logical_or, logical_and, array, where, zeros
from opus_core.variables.variable_name import VariableName
from opus_core.resources import Resources
from travel_model.models.get_cache_data_into_travel_model import GetCacheDataIntoTravelModel
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.attribute_cache import AttributeCache

class GetCacheDataIntoTravelModel(GetCacheDataIntoTravelModel):
    """Write urbansim simulation information into a (file) format 
    that travel model uses to update its tazdata. """
        
    def create_travel_model_input_file(self,
                                       config,
                                       year,
                                       zone_set,
                                       dataset_pool,
                                       delimiter = ','):
        """Writes to file specified by 'urbansim_to_tm_variable_file' 
        to [travel_model_data_directory]/[year_directory], which travel model 
        will use as input.
        """

        tm_config = config['travel_model_configuration']
        variable_mapping = tm_config['urbansim_to_tm_variable_mapping']
        tm_input_file_name = tm_config['urbansim_to_tm_variable_file'] 
        
        variable_list = []
        column_name = []
        for variable_pair in variable_mapping:
            urbansim_var, travel_model_var = variable_pair
            variable_list.append(urbansim_var)
            column_name.append(travel_model_var)

        zone_set.compute_variables(variable_list, dataset_pool=dataset_pool)
        variable_short_name = [VariableName(x).get_alias() for x in variable_list]
        
        tm_input_data_dir = os.path.join(tm_config['directory'], tm_config[year])
        if not os.path.exists(tm_input_data_dir):
            os.makedirs(tm_input_data_dir)

        input_file = os.path.join(tm_input_data_dir, tm_input_file_name)

        logger.log_status('write travel model input file : %s' % input_file)
        rows = zone_set.size()
        cols = len(variable_short_name)
        data = zeros(shape=(rows,cols))
        for i in range(cols):
            this_column=zone_set.get_attribute(variable_short_name[i])
            data[:,i] = this_column
            
        header = column_name
        self._update_travel_model_data_file(tm_config, data, header, input_file, delimiter)
        
    def _update_travel_model_data_file(self, tm_config, data, header, input_file, delimiter):
        self._write_to_txt_file(data, header, input_file, delimiter)
        
    def _write_to_txt_file(self, data, header, input_file, delimiter=','):
        logger.start_block("Writing to travel_model input file")
        newfile = open(input_file, 'w')
        newfile.write(delimiter.join(header) + "\n")
        rows, cols = data.shape
        for n in range(rows):
            newfile.write(delimiter.join([str(x) for x in data[n,]]) + "\n")
                                          
        newfile.close()
        logger.end_block()
            
if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file
    parser = OptionParser()
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

    GetCacheDataIntoTravelModel().run(resources, options.year)

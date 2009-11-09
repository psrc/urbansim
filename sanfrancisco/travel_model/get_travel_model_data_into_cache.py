# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.resources import Resources
from opus_core.logger import logger
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from numpy import array, where, zeros, logical_and
import os, csv
from travel_model.models.get_travel_model_data_into_cache import GetTravelModelDataIntoCache
from opus_core.storage_factory import StorageFactory
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration

class GetTravelModelDataIntoCache(GetTravelModelDataIntoCache):
    """
    A class to access the output of travel models.
    """
   
    def get_travel_data_from_travel_model(self, config, 
                                          year, zone_set, 
                                          tm_output_file="tm_output.txt",
                                          ):
        """
        Returns a new travel data set populated by a travel model
        The columns in the travel data set are those given in header of the tm_output.txt.
        """
        tm_config = config['travel_model_configuration']

        tm_data_dir = os.path.join(tm_config['directory'], tm_config[year])
        tm_output_file = tm_config['tm_to_urbansim_variable_file']
        tm_output_full_name = os.path.join(tm_data_dir, tm_output_file)
        
        table_name = "travel_data"
        data_dict = self._read_output_file(tm_output_full_name)
        
        in_storage = StorageFactory().get_storage('dict_storage')
        in_storage.write_table(
                table_name=table_name,
                table_data=data_dict
            )
                
        travel_data_set = TravelDataDataset(in_storage=in_storage, in_table_name=table_name)
        max_zone_id = zone_set.get_id_attribute().max()
        remove_index = where(logical_or(travel_data_set.get_attribute("from_zone_id")>max_zone_id,
                                        travel_data_set.get_attribute("to_zone_id")>max_zone_id))[0]
        travel_data_set.size()
        travel_data_set.remove_elements(remove_index)
        return travel_data_set

    def _read_output_file(self, filename, MISSING_VALUE=-9999):
        """"""
        
        fd = open(filename, 'r')
        header_line = fd.readline().strip()
        headers = header_line.split(",")
        
        return_dict = {}
        
#        text_file = open(filename, 'r')
        
        for item in headers:
            return_dict[item] = []

        reader = csv.reader(fd)
        for items in reader:
            for col_index in range(0, len(items)):
                value = items[col_index]
                if value == '':  #missing value
                    value = MISSING_VALUE
                try: #if it's a number, convert it to a float
                    return_dict[headers[col_index]].append(float(value))
                except ValueError: #otherwise, leave it as a string
                    return_dict[headers[col_index]].append(value)
            
        fd.close()
        
        for item, value in return_dict.iteritems():
            try:
                return_dict[item] = array(value)
            except:
                ##TODO: add handling for string array
                pass
        
        return return_dict

    
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

#    logger.enable_memory_logging()
    GetTravelModelDataIntoCache().run(resources, options.year)

# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os, csv
from opus_core.resources import Resources
from opus_core.logger import logger
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from numpy import array, where, zeros, logical_and
from wfrc.cube.get_travel_model_data_into_cache import GetTravelModelDataIntoCache
#from run_transcad_macro import run_transcad_macro, run_get_file_location_macro
from opus_core.storage_factory import StorageFactory
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
#from set_project_ini_file import set_project_ini_file

class GetTranscadDataIntoCache(GetTravelModelDataIntoCache):
    """
    A class to access the output of transcad travel models.
    """
   
    def get_travel_data_from_travel_model(self, config, 
                                          year, zone_set, 
                                          tm_output_file="tm_output.txt",
                                          ):

        table_name = "travel_data"
        tm_config = config['travel_model_configuration']
        base_dir = tm_config['travel_model_base_directory']
        year_dir = tm_config[year]['year_dir']
        xchange_dir = base_dir + '/' + year_dir
        filename = xchange_dir + '/travel_data.csv'
        data_dict = self._read_macro_output_file(filename)
        #data_dict = self._seq_taz_to_zone_conversion(zone_set, data_dict)

        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(
            table_name=table_name,
            table_data=data_dict
            )
        travel_data_set = TravelDataDataset(in_storage=storage, 
                                            in_table_name=table_name)
        travel_data_set.size()
        return travel_data_set

    def prepare_for_run(self, config, year):
        n = 1

    def _read_macro_output_file(self, filename, MISSING_VALUE=-9999):
        """this function is tailored to read the output file from semcog export macro"""
        
        # root, ext = os.path.splitext(filename)
        # header_filename = root + ".DCC"
        # header_fd = open(header_filename, 'r')
        # headers = []

        # for line in header_fd.readlines():
            # line=line.replace('"','')
            # item_list = line.split(",")
            # if len(item_list) < 2:
                # continue
            # if item_list[0] == "ZoneID" and "from_zone_id" not in headers:
                # headers.append("from_zone_id")  # the first RCIndex is from_zone_id?
            # elif item_list[0] == "ZoneID":
                # headers.append("to_zone_id")    # the second RCIndex is to_zone_id?
            # else:
                # headers.append(item_list[0].lower())
        # header_fd.close()
        
        return_dict = {}
        
        text_file = open(filename, 'r')
        
        headers = ['i','j','auto','transit']
        
        for item in headers:
            return_dict[item] = []

        reader = csv.reader(text_file)
        for items in reader:
            if items[0] == 'i':
                1
            else:
                for col_index in range(0, len(items)):
                    value = items[col_index]
                    if value == '':  #missing value
                        value = MISSING_VALUE
                    try: 
                        v = int(value) #integer
                    except ValueError:  #not an integer
                        try:
                            v = float(value) #float
                        except ValueError:
                            v = value  #string
                    return_dict[headers[col_index]].append(v)
        text_file.close()
        
        for item, value in return_dict.iteritems():
            try:
                return_dict[item] = array(value)
            except:
                ##TODO: add handling for string array
                pass
        renamed_dict = {}
        renamed_dict['from_zone_id'] = return_dict['i']
        renamed_dict['to_zone_id'] = return_dict['j']
        renamed_dict['travel_time'] = return_dict['auto']
        renamed_dict['travel_time_transit'] = return_dict['transit']
        return renamed_dict

    def _seq_taz_to_zone_conversion(self, zone_set, data_dict):
        #convert from seq_taz_id to zone_id for both from_zone_id and to_zone_id fields
        seq_taz = zone_set.get_attribute("seq_taz")
        zone_ids = zone_set.get_id_attribute()
        
        #refactored from commented lines below, supposed to be faster
        is_valid_from_zone_id = zeros(data_dict["from_zone_id"].size)
        is_valid_to_zone_id = zeros(data_dict["to_zone_id"].size)

        for id in seq_taz:
            is_valid_from_zone_id += data_dict["from_zone_id"] == id
            is_valid_to_zone_id += data_dict["to_zone_id"] == id
        
        keep_indices = where(logical_and(is_valid_from_zone_id, is_valid_to_zone_id))
        for name, values in data_dict.iteritems():
            data_dict[name] = values[keep_indices]
        
        #convert from seq_taz to zone_id
        for i in range(keep_indices[0].size):
            data_dict['from_zone_id'][i] = zone_ids[where(seq_taz==data_dict['from_zone_id'][i])][0]
            data_dict['to_zone_id'][i] = zone_ids[where(seq_taz==data_dict['to_zone_id'][i])][0]


        return data_dict
    
        #keep_indices = []
        #o_zone_ids = []
        #d_zone_ids = []
        #for index in range(data_dict["from_zone_id"].size):
            #o = data_dict["from_zone_id"][index]
            #d = data_dict["to_zone_id"][index]
            #has_o = (seq_taz==o)
            #has_d = (seq_taz==d)
            
            #if has_o.sum() == 1 and has_d.sum() == 1: #both o and d zones appear in zone_set's seq_taz field once
                #keep_indices.append(index)
                #o_zone_ids.append(zone_ids[where(has_o)][0])
                #d_zone_ids.append(zone_ids[where(has_d)][0])
            #elif has_o.sum() > 1 or has_d.sum() > 1:
                #logger.log_warning("o-d zone pair (%s, %s) has mulitple matches in zones and is dropped from travel data" % (o, d))
        
        #for name, values in data_dict.iteritems():
            #if name == "from_zone_id":
                #data_dict[name] = array(o_zone_ids)
            #elif name == "to_zone_id":
                #data_dict[name] = array(d_zone_ids)
            #else:
                #data_dict[name] = values[keep_indices]
    
    
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

    logger.enable_memory_logging()
    GetTranscadDataIntoCache().run(resources, options.year)

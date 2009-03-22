# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os, csv
from opus_core.resources import Resources
from opus_core.logger import logger
from urbansim.datasets.travel_data_dataset import TravelDataDataset
from numpy import array, where, zeros, logical_and
from travel_model.models.get_travel_model_data_into_cache import GetTravelModelDataIntoCache
from run_transcad_macro import run_transcad_macro, run_get_file_location_macro
from opus_core.storage_factory import StorageFactory
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from washtenaw.transcad.set_project_ini_file import set_project_ini_file

class GetTranscadDataIntoCache(GetTravelModelDataIntoCache):
    """
    A class to access the output of transcad travel models.
    """
   
    def get_travel_data_from_travel_model(self, config, 
                                          year, zone_set, 
                                          tm_output_file="tm_output.txt",
                                          ):
        """
        
        Returns a new travel data set from a given set of transcad matrices 
        populated by a specified transcad macro.  
        The columns in the travel data set are those given in matrix_variable_map in travel_model_configuration.
        """
        tm_config = config['travel_model_configuration']

        tm_data_dir = os.path.join(tm_config['directory'], tm_config[year])
        tm_output_full_name = os.path.join(tm_data_dir, tm_output_file)
        matrix_attribute_name_map = tm_config['tm_to_urbansim_variable_mapping']
        
        transcad_file_location = run_get_file_location_macro(tm_config)
        for matrix in matrix_attribute_name_map:
            matrix[0] = transcad_file_location[matrix[0]]  #replace internal matrix name with absolute file name

        macro_args =[ ("ExportTo", tm_output_full_name) ]
        macro_args.append(("Matrix", matrix_attribute_name_map))
        #for macroname, ui_db_file in tm_config['macro']['get_transcad_data_into_cache'].iteritems():
            #ui_db_file = os.path.join(tm_config['directory'], ui_db_file)
        macroname, ui_db_file = tm_config['macro']['get_transcad_data_into_cache']
        run_transcad_macro(macroname, ui_db_file, macro_args)

        table_name = "travel_data"
        data_dict = self._read_macro_output_file(tm_output_full_name)
        data_dict = self._seq_taz_to_zone_conversion(zone_set, data_dict)

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
        set_project_ini_file(config, year)

    def _read_macro_output_file(self, filename, MISSING_VALUE=-9999):
        """this function is tailored to read the output file from semcog export macro"""
        
        root, ext = os.path.splitext(filename)
        header_filename = root + ".DCC"
        header_fd = open(header_filename, 'r')
        headers = []

        for line in header_fd.readlines():
            line=line.replace('"','')
            item_list = line.split(",")
            if len(item_list) < 2:
                continue
            if item_list[0] == "ZoneID" and "from_zone_id" not in headers:
                headers.append("from_zone_id")  # the first RCIndex is from_zone_id?
            elif item_list[0] == "ZoneID":
                headers.append("to_zone_id")    # the second RCIndex is to_zone_id?
            else:
                headers.append(item_list[0].lower())
        header_fd.close()
        
        return_dict = {}
        
        text_file = open(filename, 'r')
        
        for item in headers:
            return_dict[item] = []

        reader = csv.reader(text_file)
        for items in reader:
            for col_index in range(0, len(items)):
                value = items[col_index]
                if value == '':  #missing value
                    value = MISSING_VALUE
                try: #if it's a number, convert it to a float
                    return_dict[headers[col_index]].append(float(value))
                except ValueError: #otherwise, leave it as a string
                    return_dict[headers[col_index]].append(value)
            
        text_file.close()
        
        for item, value in return_dict.iteritems():
            try:
                return_dict[item] = array(value)
            except:
                ##TODO: add handling for string array
                pass
        
        return return_dict

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

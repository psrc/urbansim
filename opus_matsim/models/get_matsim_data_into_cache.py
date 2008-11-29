#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 

import os

#from opus_core.session_configuration import SessionConfiguration
#from opus_core.resources import Resources
from opus_core.logger import logger
from travel_model.models.get_travel_model_data_into_cache import GetTravelModelDataIntoCache
#from matsim_functions import load_version_file
#from opus_core.variables.variable_name import VariableName
#from opus_core.storage_factory import StorageFactory
#from urbansim.datasets.travel_data_dataset import TravelDataDataset
#from numpy import ravel, ones, array, repeat, newaxis
from opus_core.export_storage import ExportStorage
from opus_core.store.flt_storage import flt_storage
from opus_core.store.csv_storage import csv_storage


class GetMatsimDataIntoCache(GetTravelModelDataIntoCache):
    """Class to copy travel model results into the UrbanSim cache.
       Essentially a variant of do_export_csv_to_cache.py.
    """

    def get_travel_data_from_travel_model(self, config, year, zone_set):
        """
        """
        logger.start_block('Starting GetMatsimDataIntoCache.get_travel_data...')
        
        cache_path = config['cache_directory'] + '/' + year.__str__()
        logger.log_status( " cache_path: " + cache_path ) ;
        
        input_directory = os.environ['OPUS_HOME'].__str__() + "/matsim/tmp"
        logger.log_status(" input_directory: " + input_directory )
        
        cache_storage = flt_storage(storage_location = cache_path)
        in_storage = csv_storage(storage_location = input_directory)

        
        try:
            ExportStorage().export_dataset(
                dataset_name = 'travel_data',
                in_storage = in_storage, 
                out_storage = cache_storage,
            )
        finally:
            logger.end_block()
            
                    
        raise NotImplementedError, "data path from matsim to urbansim not implemented"

#        tm_config = config['travel_model_configuration']
#
#        data_dict = {}
#        table_name = "travel_data"
#        storage = StorageFactory().get_storage('dict_storage')
#        travel_data_set = None
#        
#        #Get config params
#        visum_dir, fileName = tm_config[year]['version']
#        visum_version_number = tm_config['visum_version_number']
#        
#        #Startup Visum
#        Visum = load_version_file(visum_dir, fileName, visum_version_number)
#        
#        matrices = tm_config["tm_to_urbansim_variables"]
#        #Get matrices
#        #Note that matrix objects must be defined in version file before getting or setting
#        try:
#            #Get demand matrices
#            if matrices.has_key('od'):
#                for od_mat_num, od_mat_name in matrices["od"].iteritems():
#                    mat = h.GetODMatrix(Visum, od_mat_num) #returns a 2d numarray object
#                    data_dict[od_mat_name] = ravel(mat)    #flatten to 1d and convert to numpy
#                    #mat.tofile(visum_dir + "/od" + str(od_mat_num) + ".mtx") #temp hack to save it
#                
#            #Get skim matrices    
#            if matrices.has_key('skim'):
#                for skim_mat_num,skim_mat_name in matrices["skim"].iteritems():
#                    mat = h.GetSkimMatrix(Visum, skim_mat_num) #returns a 2d numarray object
#                    data_dict[skim_mat_name] = ravel(mat)      #flatten to 1d and convert to numpy
#                #mat.tofile(visum_dir + "/skim" + str(skim_mat_num) + ".mtx") #temp hack to save it
#        except Exception, e:
#            error_msg = "Getting matrices failed: %s " % e
#            raise StandardError(error_msg)
#
#        ## hack to add keys to the matrix values
#        zoneNumbers = h.GetMulti(Visum.Net.Zones, "NO")
#        zoneNumbers = array(zoneNumbers)[newaxis, :]
#        from_zone_id = ravel(zoneNumbers.repeat(zoneNumbers.size, axis=1))
#        to_zone_id = ravel(zoneNumbers.repeat(zoneNumbers.size, axis=0))
#        
#        data_dict['from_zone_id'] = from_zone_id
#        data_dict['to_zone_id'] = to_zone_id
#        
#        storage.write_table( table_name=table_name, table_data=data_dict )
#        travel_data_set = TravelDataDataset( in_storage=storage, in_table_name=table_name )
#
#        travel_data_set.size()
#        return travel_data_set

# this is needed since it is called from opus via "main":        
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
    resources = Resources(get_resources_from_file(options.resources_file_name))

    logger.enable_memory_logging()
    GetVisumDataIntoCache().run(resources, options.year)

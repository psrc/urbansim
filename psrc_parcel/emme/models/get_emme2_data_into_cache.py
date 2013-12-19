# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.session_configuration import SessionConfiguration
from opus_core.resources import Resources
from numpy import array, float32, ones
import os, shutil
from opus_core.logger import logger
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_emme2.models.get_emme2_data_into_cache import GetEmme2DataIntoCache as ParentGetEmme2DataIntoCache

class GetEmme2DataIntoCache(ParentGetEmme2DataIntoCache):
    """Class to copy skims stored in hdf5 format into the UrbanSim cache. 
    """
    
    def run(self, year):
        """Like its parent, but skims are stored locally in matrix_directory in hdf5 format.
        It is one file per year, called xxxx-travelmodel.h5, where xxxx is the year. 
        Each file has one group per bank, e.g. Bank1, which contains the matrices.
        Zones are assumed to have no gaps.
        """
        cache_directory = self.config['cache_directory']
        simulation_state = SimulationState()
        simulation_state.set_current_time(year)
        simulation_state.set_cache_directory(cache_directory)
        
        year_config = self.config['travel_model_configuration'][year]
        matrix_directory = self.config['travel_model_configuration'].get('matrix_h5_directory', None)
        if matrix_directory is None:
            raise AttributeError, "matrix_directory must be given."
        
        bank_year = self.config['travel_model_configuration'][year]['bank']
        bank_file = os.path.join(matrix_directory, "%s-travelmodel.h5" % bank_year)
        for x in 1,2,3:
            if "bank%i" % x in year_config['matrix_variable_map']:
                self.get_needed_matrices_from_emme2(year, 
                                                year_config['cache_directory'],
                                                bank_file, x,
                                                year_config['matrix_variable_map']["bank%i" % x])
                
    def get_needed_matrices_from_emme2(self, year, cache_directory, bank_file, bank, matrix_variable_map):
        """Copies the specified emme/2 matrices into the specified travel_data variable names.
        """
        logger.start_block('Getting matricies from emme2')
        try:    
            zone_set = SessionConfiguration().get_dataset_from_pool('zone')
            zone_set.load_dataset()
            travel_data_set = self.get_travel_data_from_emme2(zone_set, bank_file, bank, matrix_variable_map)
        finally:
            logger.end_block()
        
        logger.start_block('Writing data to cache')
        try:
            next_year = year + 1
            out_storage = AttributeCache().get_flt_storage_for_year(next_year)
            travel_data_set.write_dataset(attributes='*', 
                                          out_storage=out_storage, 
                                          out_table_name='travel_data')
        finally:
            logger.end_block()
                  
    def get_travel_data_from_emme2(self, zone_set, bank_file, bank, matrix_variable_map, **kwargs):
        """Create a new travel_data from the emme2 output.
        Include the matrices listed in matrix_variable_map, which is a dictionary
        mapping the emme2 matrix name, e.g. au1tim, to the Opus variable
        name, e.g. single_vehicle_to_work_travel_time, as in:
        {"au1tim":"single_vehicle_to_work_travel_time"}
        """
        from psrc_parcel.emme.travel_model_output import TravelModelOutput
        tm_output = TravelModelOutput(self.emme_cmd)
        return tm_output.get_travel_data_set(zone_set, matrix_variable_map, bank_file, bank, **kwargs)
    

        
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

    GetEmme2DataIntoCache(resources).run(options.year)    



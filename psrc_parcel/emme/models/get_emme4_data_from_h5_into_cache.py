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
from opus_core.storage_factory import StorageFactory
from psrc_parcel.emme.models.get_emme4_data_into_cache import GetEmme4DataIntoCache as ParentGetEmme4DataIntoCache

class GetEmme4DataFromH5IntoCache(ParentGetEmme4DataIntoCache):
    """Class to copy skims stored in hdf5 format into the UrbanSim cache. 
    """
    
    def run(self, year):
        """Like its parent, but skims are stored locally in matrix_directory in hdf5 format.
        It is one file per year, called xxxx-travelmodel.h5, where xxxx is the year. 
        Each file has one group per directory name in matrix_variable_map, e.g. 'skims.auto.am', 
        which contains the matrices.
        Zones are assumed to have no gaps.
        """
        cache_directory = self.config['cache_directory']
        simulation_state = SimulationState()
        simulation_state.set_current_time(year)
        simulation_state.set_cache_directory(cache_directory)
        
        tmconfig = self.config['travel_model_configuration']
        year_config = tmconfig[year]
        matrix_directory = tmconfig.get('matrix_h5_directory', self.get_emme2_base_dir())        
        bank_year = tmconfig[year]['bank'][0]
        bank_file = os.path.join(matrix_directory, "%s-travelmodel.h5" % bank_year)
        for path, variable_dict in year_config['matrix_variable_map'].iteritems():
            self.get_needed_matrices_from_emme4(year, 
                                                year_config['cache_directory'],
                                                path, variable_dict, bank_file=bank_file)
                     
    def get_travel_data_from_emme4(self, zone_set, path, matrix_variable_map, bank_file=None, **kwargs):
        """Create a new travel_data from the emme4 output.
        Include the matrices listed in matrix_variable_map, which is a dictionary
        mapping the emme4 matrix name, e.g. au1tim, to the Opus variable
        name, e.g. single_vehicle_to_work_travel_time, as in:
        {"au1tim":"single_vehicle_to_work_travel_time"}
        """
        from psrc_parcel.emme.travel_model_output import TravelModelOutput
        tm_output = TravelModelOutput(self.emme_cmd)
        h5storage = StorageFactory().get_storage('hdf5g_storage', 
                                                 storage_location=bank_file)
        return tm_output.get_travel_data_set(zone_set, matrix_variable_map,
                                             table_name=path, in_storage=h5storage, **kwargs)
    

        
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

    GetEmme4DataFromH5IntoCache(resources).run(options.year)    



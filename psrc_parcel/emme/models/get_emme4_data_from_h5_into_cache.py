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
from psrc_parcel.emme.models.abstract_emme4_travel_model import AbstractEmme4TravelModel

class GetEmme4DataFromH5IntoCache(ParentGetEmme4DataIntoCache, AbstractEmme4TravelModel):
    
    """Copy skims stored in hdf5 format into the UrbanSim cache."""
    
    def run(self, year):
        """
        Copy skims stored in hdf5 format into the UrbanSim cache.
        
        Should run after psrc_parcel.emme.models.run_export_skims which creates the skims hdf5 file.
        It creates a travel_model dataset with each skim being an attribute of it. 
        Zones are assumed to have no gaps.
        
        Arguments:
        year -- year of the urbansim run. Used to extract the TM year from the bank configuration.
        
        Configuration entries (in travel_model_configuration) used:
        matrix_variable_map -- dictionary of bank names and corresponding skim names.
                Bank names are the path where (back-)slashes are replaced by dots, e.g. skims.auto.am.
                A value for each of such bank name is a dictionary with keys being skim names and 
                values being the desired urbansim attribute name. E.g.
                {'skims.nonmotorized.am':
                      {'abketm': 'am_bike_to_work_travel_time',
                       'awlktm': 'am_walk_time_in_minutes'
                      }
                }
        matrix_h5_directory -- path to the hdf5 file called xxxx-travelmodel.h5  
                where xxxx is replaced by the TM year (default is the Emme base directory), 
                which contains the skims as n x n matrices.
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
        """Return a dataset travel_data with set of attributes from one bank.
        
        Creates an hdf5g storage with data corresponding to one bank in 
        matrix_variable_map. It calls the method get_travel_data_set from 
        psrc_parcel.emme.travel_model_output which is expected to return a travel_data 
        dataset with the set of attributes stored in the hdf5g storage.

        Arguments:
        zone_set -- dataset of zones
        path -- group name in the hdf5 file (i.e. the bank name, e.g. skims.auto.am)
        matrix_variable_map -- dictionary of skim names and corresponding attribute names
        bank_file -- full name of the hdf5 file        
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



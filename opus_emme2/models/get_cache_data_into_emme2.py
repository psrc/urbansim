#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.session_configuration import SessionConfiguration
from opus_emme2.sql_value_reader import SqlValueReader
from opus_core.store.scenario_database import ScenarioDatabase
from opus_core.resources import Resources
from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset_factory import DatasetFactory
from psrc.travel_model_input_file_writer import TravelModelInputFileWriter
from opus_core.logger import logger
from opus_core.store.attribute_cache import AttributeCache
from opus_emme2.models.abstract_emme2_travel_model import AbstractEmme2TravelModel
        
class GetCacheDataIntoEmme2(AbstractEmme2TravelModel):
    """Get needed emme/2 data from UrbanSim cache into inputs for travel model.
    """

    def run(self, config, year):
        """This is the main entry point.  It gets the appropriate configuration info from the 
        travel_model_configuration part of this config, and then copies the specified 
        UrbanSim data into files for emme/2 to read.  
        """
        cache_directory = config['cache_directory']
        simulation_state = SimulationState()
        simulation_state.set_cache_directory(cache_directory)
        simulation_state.set_current_time(year)
        attribute_cache = AttributeCache()
        SessionConfiguration(new_instance=True,
                             in_storage=AttributeCache())
                             
        arguments = {'in_storage':attribute_cache}
        gc_set = DatasetFactory().get_dataset('gridcell', package='urbansim', 
                                              arguments=arguments)
        hh_set = DatasetFactory().get_dataset('household', package='urbansim', 
                                              arguments=arguments)
        zone_set = DatasetFactory().get_dataset('zone', package='urbansim', 
                                                arguments=arguments)
        job_set = DatasetFactory().get_dataset('job', package='urbansim', 
                                               arguments=arguments)
        self._call_input_file_writer(config, year, gc_set, job_set, zone_set, hh_set)

    def _call_input_file_writer(self, config, year, gc_set, job_set, zone_set, hh_set):
        scenario_db = ScenarioDatabase(config['input_configuration'].host_name,
                                       config['input_configuration'].user_name, 
                                       config['input_configuration'].password,
                                       config['input_configuration'].database_name)
        constant_taz_reader = SqlValueReader(scenario_db, 'constant_taz_columns')
        gc_set.load_dataset(attributes=['grid_id', 'zone_id'])
        job_set.load_dataset(attributes=['job_id', 'sector_id', 'grid_id'])
        hh_set.load_dataset(attributes=['household_id', 'income', 'grid_id'])
        zone_set.load_dataset()
        
        tm_file_writer = TravelModelInputFileWriter()
        tripgen_dir = self.get_emme2_dir(config, year, 'tripgen')
        logger.log_status('tripgen dir: %s' % tripgen_dir)
        tm_file_writer.create_tripgen_travel_model_input_file(gc_set, job_set, hh_set,
                                                              constant_taz_reader,
                                                              tripgen_dir,
                                                              year)
    
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
                         package_order_exceptions=resources['dataset_pool_configuration'].package_order_exceptions,                              
                         in_storage=AttributeCache())

#    logger.enable_memory_logging()
    GetCacheDataIntoEmme2().run(resources, options.year)
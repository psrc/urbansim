# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from shutil import copy
from opus_core.session_configuration import SessionConfiguration
from opus_core.resources import Resources
from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.class_factory import ClassFactory
from opus_core.logger import logger
from opus_core.store.attribute_cache import AttributeCache
from opus_emme2.models.abstract_emme2_travel_model import AbstractEmme2TravelModel
from opus_core.misc import get_camel_case_class_name_from_opus_path
        
class GetCacheDataIntoEmme2(AbstractEmme2TravelModel):
    """Get needed emme/2 data from UrbanSim cache into inputs for travel model.
    """

    def run(self, year):
        """This is the main entry point.  The class is initialized with the appropriate configuration info from the 
        travel_model_configuration part of this config, and then copies the specified 
        UrbanSim data into files for emme/2 to read.  
        If households and jobs do not have a primary attribute zone_id, the entry 'locations_to_disaggregate'
        in the travel_model_configuration should be a list of dataset names over which the zone_id 
        will be dissaggregated, ordered from higher to lower aggregation level, e.g. ['parcel', 'building']
        """
        cache_directory = self.config['cache_directory']
        simulation_state = SimulationState()
        simulation_state.set_cache_directory(cache_directory)
        simulation_state.set_current_time(year)
        attribute_cache = AttributeCache()
        sc = SessionConfiguration(new_instance=True,
                                  package_order=self.config['dataset_pool_configuration'].package_order,
                                  in_storage=attribute_cache)
        dataset_pool = sc.get_dataset_pool()

        hh_set = dataset_pool.get_dataset('household')
        zone_set = dataset_pool.get_dataset('zone')
        job_set = dataset_pool.get_dataset('job')
        locations_to_disaggregate = self.config['travel_model_configuration']['locations_to_disaggregate']
        len_locations_to_disaggregate = len(locations_to_disaggregate)
        if len_locations_to_disaggregate > 0:
            primary_location = locations_to_disaggregate[0]
            if len_locations_to_disaggregate > 1:
                intermediates_string = ", intermediates=["
                for i in range(1, len_locations_to_disaggregate):
                    intermediates_string = "%s%s, " % (intermediates_string, locations_to_disaggregate[i])
                intermediates_string = "%s]" % intermediates_string
            else:
                intermediates_string = ""
            hh_set.compute_variables(['%s = household.disaggregate(%s.%s %s)' % (zone_set.get_id_name()[0],
                                                                                 primary_location, zone_set.get_id_name()[0],
                                                                                 intermediates_string)], 
                                      dataset_pool=dataset_pool)
            job_set.compute_variables(['%s = job.disaggregate(%s.%s %s)' % (zone_set.get_id_name()[0],
                                                                            primary_location, zone_set.get_id_name()[0],
                                                                            intermediates_string)], 
                                       dataset_pool=dataset_pool)
        
        return self._call_input_file_writer(year, dataset_pool)

    def _call_input_file_writer(self, year, dataset_pool):
        writer_module = self.config['travel_model_configuration'].get('travel_model_input_file_writer')
        writer_class = get_camel_case_class_name_from_opus_path(writer_module)
        file_writer = ClassFactory().get_class( writer_module, class_name=writer_class )
        current_year_emme2_dir = self.get_emme2_dir(year)
        filename = file_writer.run(current_year_emme2_dir, year, dataset_pool, config=self.config)
        if isinstance(filename, list):
            return filename
        return [filename]
    
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
    parser.add_option("-d", "--dest", dest="destination_directory", action="store", type="string", default=None,
                      help="Copy resulting files into this directory.")
    (options, args) = parser.parse_args()
    
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))

#    logger.enable_memory_logging()
    files = GetCacheDataIntoEmme2(resources).run(options.year)
    if options.destination_directory is not None:
        for file in files:
            copy(file, options.destination_directory)
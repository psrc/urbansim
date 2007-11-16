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

from shutil import copy
from opus_core.session_configuration import SessionConfiguration
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
        If households and jobs do not have a primary attribute zone_id, the entry 'locations_to_disaggregate'
        in the travel_model_configuration should be a list of dataset names over which the zone_id 
        will be dissaggregated, ordered from higher to lower aggregation level, e.g. ['parcel', 'building']
        """
        cache_directory = config['cache_directory']
        simulation_state = SimulationState()
        simulation_state.set_cache_directory(cache_directory)
        simulation_state.set_current_time(year)
        attribute_cache = AttributeCache()
        sc = SessionConfiguration(new_instance=True,
                                  package_order=config['dataset_pool_configuration'].package_order,
                                  package_order_exceptions=config['dataset_pool_configuration'].package_order_exceptions, 
                                  in_storage=attribute_cache)
        dataset_pool = sc.get_dataset_pool()

        hh_set = dataset_pool.get_dataset('household')
        zone_set = dataset_pool.get_dataset('zone')
        job_set = dataset_pool.get_dataset('job')
        taz_col_set = dataset_pool.get_dataset('constant_taz_column')
        locations_to_disaggregate = config['travel_model_configuration']['locations_to_disaggregate']
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
        
        return self._call_input_file_writer(config, year, job_set, zone_set, hh_set, taz_col_set)

    def _call_input_file_writer(self, config, year, job_set, zone_set, hh_set, taz_col_set):
        max_zone_id = zone_set.get_id_attribute().max()
        tm_file_writer = TravelModelInputFileWriter()
        tripgen_dir = self.get_emme2_dir(config, year, 'tripgen')
        logger.log_status('tripgen dir: %s' % tripgen_dir)
        resulting_files = []
        filename = tm_file_writer.create_tripgen_travel_model_input_file(job_set, hh_set,
                                                              taz_col_set, max_zone_id,
                                                              tripgen_dir,
                                                              year)
        resulting_files.append(filename)
        return resulting_files
    
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
    files = GetCacheDataIntoEmme2().run(resources, options.year)
    if options.destination_directory is not None:
        for file in files:
            copy(file, options.destination_directory)
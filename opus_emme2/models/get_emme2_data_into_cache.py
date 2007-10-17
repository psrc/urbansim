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
from opus_core.store.flt_storage import flt_storage
from opus_core.resources import Resources
from numpy import array, float32, ones
import os
from opus_core.logger import logger
from opus_emme2.models.abstract_emme2_travel_model import AbstractEmme2TravelModel
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache

class GetEmme2DataIntoCache(AbstractEmme2TravelModel):
    """Class to copy travel model results into the UrbanSim cache.
    """

    def run(self, config, year, matrix_directory=None):
        """This is the main entry point.  It gets the appropriate values from the 
        travel_model_configuration part of this config, and then copies the specified 
        emme/2 matrices into the specified travel_data variable names.  Results in
        a new travel_data cache for year+1.
        If matrix_directory is not None, it is assumed the matrices files are already created 
        in the given directory.
        """
        cache_directory = config['cache_directory']
        simulation_state = SimulationState()
        simulation_state.set_current_time(year)
        simulation_state.set_cache_directory(cache_directory)
        
        year_config = config['travel_model_configuration'][year]
        matrices_created = False
        if matrix_directory is not None:
            matrices_created = True
            
        for x in 1,2,3:
            if matrix_directory is None:
                bank_dir = self.get_emme2_dir(config, year, "bank%i" % x)
            else:
                bank_dir = os.path.join(matrix_directory, "bank%i" % x)
            self.get_needed_matrices_from_emme2(year, 
                                            year_config['cache_directory'],
                                            bank_dir,
                                            year_config['matrix_variable_map']["bank%i" % x],
                                                matrices_created)

    def create_output_matrix_files(self, config, year, max_zone_id):
        """Create data files with emme2 matrices."""
        from opus_emme2.travel_model_output import TravelModelOutput
        tm_output = TravelModelOutput()
        year_config = config['travel_model_configuration'][year]
        for x in 1,2,3:
            bank_dir = self.get_emme2_dir(config, year, "bank%i" % x)
            for matrix_name in year_config['matrix_variable_map']["bank%i" % x].keys():
                tm_output._get_matrix_into_data_file(matrix_name, max_zone_id, bank_dir, "%s_one_matrix.txt" % matrix_name)
            
    def get_needed_matrices_from_emme2(self, year, cache_directory, bank_dir, matrix_variable_map, matrices_created=False):
        """Copies the specified emme/2 matrices into the specified travel_data variable names.
        """
        logger.start_block('Getting matricies from emme2')
        try:
            next_year = year + 1
            flt_dir_for_next_year = os.path.join(cache_directory, str(next_year))
            if not os.path.exists(flt_dir_for_next_year):
                os.mkdir(flt_dir_for_next_year)
    
            zone_set = SessionConfiguration().get_dataset_from_pool('zone')
            
            zone_set.load_dataset()
            travel_data_set = self.get_travel_data_from_emme2(zone_set, bank_dir, matrix_variable_map, matrices_created)
        finally:
            logger.end_block()
        
        logger.start_block('Writing data to cache')
        try:
            out_storage = flt_storage(storage_location=flt_dir_for_next_year)
            travel_data_set.write_dataset(attributes='*', 
                                          out_storage=out_storage, 
                                          out_table_name='travel_data')
        finally:
            logger.end_block()
              
    def get_travel_data_from_emme2(self, zone_set, bank_dir, matrix_variable_map, matrices_created=False):
        """Create a new travel_data from the emme2 output.
        Include the matrices listed in matrix_variable_map, which is a dictionary
        mapping the emme2 matrix name, e.g. au1tim, to the Opus variable
        name, e.g. single_vehicle_to_work_travel_time, as in:
        {"au1tim":"single_vehicle_to_work_travel_time"}
        """
        from opus_emme2.travel_model_output import TravelModelOutput
        tm_output = TravelModelOutput()
        return tm_output.get_travel_data_set(zone_set, matrix_variable_map, bank_dir, matrices_created = matrices_created)
        
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
    parser.add_option("-m", "--matrices-only", dest="matrices_only", default=False, action="store_true",
                      help="Only emme2 matrices will be created.")
    parser.add_option("-z", "--max_zone_id", dest="max_zone_id", default=0, type="int",
                      help="Maximum zone id must be given if the option -m is used.")
    parser.add_option("--matrix_directory", dest="matrix_directory", default=None, 
                      help="This option assumes that the matrix files were previously created (e.g. from a previous run with the -m option) \nand are stored in this directory.")
    (options, args) = parser.parse_args()
   
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))
    
    SessionConfiguration(new_instance=True,
                         package_order=resources['dataset_pool_configuration'].package_order,
                         package_order_exceptions=resources['dataset_pool_configuration'].package_order_exceptions,                              
                         in_storage=AttributeCache())
        
#    logger.enable_memory_logging()
    if options.matrices_only:
        GetEmme2DataIntoCache().create_output_matrix_files(resources, options.year, options.max_zone_id)
    else:
        GetEmme2DataIntoCache().run(resources, options.year, options.matrix_directory)    
    #from opus_core.configuration import Configuration
    #config = Configuration({
        #'cache_directory':r'D:\urbansim_cache\test_data',
        #'travel_model_configuration':{
            #'matrix_variable_map':{
                ##"au1tim":"single_vehicle_to_work_travel_time",
                ##"biketm":"bike_to_work_travel_time",
                ##"walktm":"am_walk_time_in_minutes",
                ##"atrtwa":"am_total_transit_time_walk",
                ##"avehda":"am_pk_period_drive_alone_vehicle_trips",
                ##"ambike":"am_biking_person_trips",
                ##"amwalk":"am_walking_person_trips",
                ##"atrnst":"am_transit_person_trip_table",
                #"au1cos":"single_vehicle_to_work_travel_cost",
                #},
            #2005:{
                #'bank':[
                    #'baseline_travel_model(cra-10-8)',
                    #'2000_05',
                    #'bank1',
                    #],
                #},
            #2010:{
                #'bank':[
                    #'baseline_travel_model(cra-10-8)',
                    #'2000_10',
                    #'bank1',
                    #],
                #},
            #},
        #})

    #GetEmme2DataIntoCache().run(config, 2005)
    #GetEmme2DataIntoCache().run(config, 2010)


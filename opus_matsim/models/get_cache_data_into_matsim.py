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

from opus_core.export_storage import ExportStorage
from opus_core.store.flt_storage import flt_storage
from opus_core.store.tab_storage import tab_storage

from opus_core.logger import logger
from opus_core.resources import Resources
from travel_model.models.get_cache_data_into_travel_model import GetCacheDataIntoTravelModel
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework.core.source_data import SourceData
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.logger import logger
from numpy import zeros, arange
from opus_core.session_configuration import SessionConfiguration
from opus_core.variables.attribute_type import AttributeType
from opus_core.indicator_framework.image_types.dataset_table import DatasetTable
from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory
import os
import shutil
import sys


class GetCacheDataIntoMatsim(GetCacheDataIntoTravelModel):
    """Get needed data from UrbanSim cache into inputs for travel model.
       Essentially a variant of opus_core/tools/do_export_cache_to_tab_delimited_files.py
    """

    #def run(self, config, year):

    def create_travel_model_input_file(self, config, year, *args, **kwargs):
        """"""
        logger.start_block('Starting GetCacheDataIntoMatsim.run(...)')

        #GetCacheDataIntoTravelModel.run(self, config, year)
        
        persons = SessionConfiguration().get_dataset_from_pool('person')
        if not 'matsim_flag' in persons.get_known_attribute_names():
            ## add matsim_flag for persons proportion to the sampling rate
            persons_size = persons.size()
            sampling_rate = config['travel_model_configuration']['sampling_rate']
            matsim_flag = zeros(persons_size, dtype='int32')
            sampled_person_index = sample_noreplace( arange(persons_size), 
                                                     int(sampling_rate * persons_size), 
                                                     return_indices=True )
            matsim_flag[sampled_person_index] = 1
            persons.add_attribute(matsim_flag, 'matsim_flag', metadata=AttributeType.PRIMARY)
            persons.flush_attribute('matsim_flag')
        
        source_data = SourceData(
            cache_directory = config['cache_directory'],
            years = [year],
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['psrc_parcel','urbansim_parcel','psrc', 'urbansim','opus_core'],
                ),
        )            
        
        output_directory = os.environ['OPUS_HOME'].__str__() + "/opus_matsim/tmp"
        
        export_indicators = [
            DatasetTable(
                attributes = [
                    'resid_x_coord = person.disaggregate(parcel.x_coord_sp, intermediates=[building, household])',
                    'resid_y_coord = person.disaggregate(parcel.y_coord_sp, intermediates=[building, household])',
                    'workp_x_coord = person.disaggregate(parcel.x_coord_sp, intermediates=[building, job])',
                    'workp_y_coord = person.disaggregate(parcel.y_coord_sp, intermediates=[building, job])',
                    'person.employment_status',
                    'person.matsim_flag',
                    ],
                dataset_name = 'person',
                exclude_condition = 'person.matsim_flag==0',
                storage_location = output_directory,
                source_data = source_data,
                output_type = 'tab',
                name = 'exported_indicators',
                )
        ]
        
        
        
        IndicatorFactory().create_indicators(
             indicators = export_indicators,
             display_error_box = False, 
             show_results = False)
                
        logger.end_block()        
        
# the following is needed, since it is called as "main" from the framework ...  
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
    GetCacheDataIntoMatsim().run(resources, options.year)

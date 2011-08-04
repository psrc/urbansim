# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from numpy import zeros, arange
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.export_storage import ExportStorage
from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory
from opus_core.indicator_framework.core.source_data import SourceData
from opus_core.indicator_framework.image_types.dataset_table import DatasetTable
from opus_core.logger import logger
from opus_core.resources import Resources
from opus_core.sampling_toolbox import sample_noreplace
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.flt_storage import flt_storage
from opus_core.store.tab_storage import tab_storage
from opus_core.tests import opus_unittest
from opus_core.variables.attribute_type import AttributeType
from travel_model.models.get_cache_data_into_travel_model import GetCacheDataIntoTravelModel
import os
import shutil
import sys



class GetCacheDataIntoMatsim(GetCacheDataIntoTravelModel):
    """Get needed data from UrbanSim cache into inputs for travel model.
       Essentially a variant of opus_core/tools/do_export_cache_to_tab_delimited_files.py
    """

    def create_travel_model_input_file(self, config, year, *args, **kwargs):
        """"""
        logger.start_block('Starting GetCacheDataIntoMatsim.run(...)')
        
        
#        # When this is called for the first time, the 'matsim_flag' is not there.  Will be constructed here:  
#        if not 'matsim_flag' in persons.get_known_attribute_names():
#            persons = SessionConfiguration().get_dataset_from_pool('person')
#            persons_size = persons.size()
#            sampling_rate = config['travel_model_configuration']['sampling_rate']
#            matsim_flag = zeros(persons_size, dtype='int32')
#            sampled_person_index = sample_noreplace( arange(persons_size), 
#                                                     int(sampling_rate * persons_size), 
#                                                     return_index=True )
#            matsim_flag[sampled_person_index] = 1
#            persons.add_attribute(matsim_flag, 'matsim_flag', metadata=AttributeType.PRIMARY)
#            persons.flush_attribute('matsim_flag')
        
        # I guess this is access to the full urbansim cache data.
        source_data = SourceData(
            cache_directory = config['cache_directory'],
            years = [year],
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['psrc_parcel','urbansim_parcel','psrc', 'urbansim','opus_core'],
                ),
        )            
        
        output_root = os.path.join( os.environ['OPUS_HOME'],"opus_matsim" ) 
        try: os.mkdir( output_root )
        except: pass
        
        output_directory = os.path.join( os.environ['OPUS_HOME'], "opus_matsim", "tmp" )
        try: os.mkdir(output_directory)
        except: pass
        
        ### PERSONS
        export_indicators = [
            DatasetTable(
                attributes = [
                    'parcel_id_home = person.disaggregate(parcel.parcel_id, intermediates=[building,household])',
                    'parcel_id_work = person.disaggregate(parcel.parcel_id, intermediates=[building,job])',
                    ],
                dataset_name = 'person',
#                exclude_condition = 'person.matsim_flag==0',
                storage_location = output_directory,
                source_data = source_data,
                output_type = 'tab',
                name = 'exported_indicators',
                )
        ]
        # This is (I assume) executing the export
        IndicatorFactory().create_indicators(
             indicators = export_indicators,
             display_error_box = False, 
             show_results = False)
        
        ### "FACILITIES"
        # yyyy There is a problem here (and at other places) if the table headers do not exist under exactly the same name.  
        # For the _id, this is probably not a problem, since these are fairly strongly typed in the table definitions.  The other
        # headers are, however, free form, and it could be, for example, "x_coord" or "xx" or "x100" or whatever.  There should
        # be, minimally, something that checks that fields exist under these names.  kai, sep'10
        export_indicators = [
            DatasetTable(
                attributes = [
                    'parcel.x_coord_sp',
                    'parcel.y_coord_sp',
                    'parcel.zone_id',
                    ],
                dataset_name = 'parcel',
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
    

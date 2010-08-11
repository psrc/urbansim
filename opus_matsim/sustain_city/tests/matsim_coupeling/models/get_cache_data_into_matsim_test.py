# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory
from opus_core.indicator_framework.core.source_data import SourceData
from opus_core.indicator_framework.image_types.dataset_table import DatasetTable
from opus_core.logger import logger
from opus_core.resources import Resources
from travel_model.models.get_cache_data_into_travel_model import GetCacheDataIntoTravelModel
import os



class GetCacheDataIntoMatsimTest(GetCacheDataIntoTravelModel):
    """Get needed data from UrbanSim cache into inputs for travel model.
       Essentially a variant of opus_core/tools/do_export_cache_to_tab_delimited_files.py
    """

    def create_travel_model_input_file(self, config, year, *args, **kwargs):
        """"""

        logger.start_block('Starting GetCacheDataIntoMatsimTest.run(...)')

        source_data = SourceData(
            cache_directory = config['cache_directory'],
            years = [year],
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['psrc_parcel','urbansim_parcel','psrc', 'urbansim','opus_core'],
                ),
        )            
        
        output_root = config['root']
        if not os.path.exists( output_root ):
            try: os.mkdir( output_root )
            except: pass
        
        output_root_extended = os.path.join( config['root'], 'opus_matsim')
        if not os.path.exists( output_root_extended ):
            try: os.mkdir( output_root_extended )
            except: pass
        
        output_directory = os.path.join( output_root_extended, 'tmp' )
        if not os.path.exists( output_directory ):
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
    GetCacheDataIntoMatsimTest().run(resources, options.year)
    

# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory
from opus_core.indicator_framework.core.source_data import SourceData
from opus_core.indicator_framework.image_types.dataset_table import DatasetTable
from opus_core.logger import logger
from opus_core.resources import Resources
from travel_model.models.get_cache_data_into_travel_model import GetCacheDataIntoTravelModel
import os



class GetCacheDataIntoMatsim(GetCacheDataIntoTravelModel):
    """Get needed data from UrbanSim cache into inputs for travel model.
       Essentially a variant of opus_core/tools/do_export_cache_to_tab_delimited_files.py
    """

    def create_travel_model_input_file(self, config, year, *args, **kwargs):
        """Constructs and writes a persons and jobs table. 
        Both are associated with a parcels table (also constructed here) storing locations (x and y coordinates) of each person and job .
        """

        logger.start_block('Starting GetCacheDataIntoMatsim.run(...)')
        
        # tnicolai :for debugging
        #try:
        #    import pydevd
        #    pydevd.settrace()
        #except: pass
        
        # I guess this is access to the full UrbanSim cache data.
        source_data = SourceData(
            cache_directory = config['cache_directory'],
            years = [year],
            dataset_pool_configuration = DatasetPoolConfiguration(
                package_order=['psrc_parcel','urbansim_parcel','psrc', 'urbansim','opus_core'],
                ),
        )            
        
        output_root = os.path.join( os.environ['OPUS_HOME'],"opus_matsim" ) 
        if not os.path.exists( output_root ):
            try: os.mkdir( output_root )
            except: pass
        
        self.output_directory = os.path.join( output_root, "tmp" )
        if not os.path.exists( self.output_directory ):
            try: os.mkdir(self.output_directory)
            except: pass
                
        ### Jobs ###############################
        
        self.dataset_table_jobs = DatasetTable(
                attributes = [
                    'parcel_id_work = job.disaggregate(parcel.parcel_id, intermediates=[building])',
                    'zone_id_work = job.disaggregate(zone.zone_id, intermediates=[parcel,building])'
                    ],
                dataset_name = 'job',
                # exclude_condition = 'person.matsim_flag==0',
                storage_location = self.output_directory,
                source_data = source_data,
                output_type = 'tab',
                name = 'exported_indicators',
                )
        
        export_indicators_jobs = [ self.dataset_table_jobs ]
        
        # executing the export jobs
        IndicatorFactory().create_indicators(
             indicators = export_indicators_jobs,
             display_error_box = False, 
             show_results = False)
        
        ### PERSONS ###############################
        
        self.dataset_table_persons = DatasetTable(
                attributes = [ # TODO: ADD HOME XY-COORDINATES AND WORK XY_COORDINATES
                    'parcel_id_home = person.disaggregate(parcel.parcel_id, intermediates=[building,household])',
                    'parcel_id_work = person.disaggregate(parcel.parcel_id, intermediates=[building,job])',
                    ],
                dataset_name = 'person',
                # exclude_condition = 'person.matsim_flag==0',
                storage_location = self.output_directory,
                source_data = source_data,
                output_type = 'tab',
                name = 'exported_indicators',
                )
        
        export_indicators_persons = [ self.dataset_table_persons ]
        
        # executing the export persons
        IndicatorFactory().create_indicators(
             indicators = export_indicators_persons,
             display_error_box = False, 
             show_results = False)
        
        ### FACILITIES ###############################
        
        self.dataset_table_parcels = DatasetTable(
                attributes = [
                    'parcel.x_coord_sp',
                    'parcel.y_coord_sp',
                    'parcel.zone_id',
                    ],
                dataset_name = 'parcel',
                storage_location = self.output_directory,
                source_data = source_data,
                output_type = 'tab',
                name = 'exported_indicators',
                )
        
        export_indicators_parcels = [ self.dataset_table_parcels ]
        
        # executing the export parcels
        IndicatorFactory().create_indicators(
             indicators = export_indicators_parcels,
             display_error_box = False, 
             show_results = False)
                
        logger.end_block()        
        


# called from opus via main! 
if __name__ == "__main__":
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
    

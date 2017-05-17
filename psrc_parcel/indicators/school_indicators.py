# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# script to produce a number of PSRC indicators -- 
# this illustrates using traits-based configurations programatically


from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework.core.source_data import SourceData

from opus_core.indicator_framework.image_types.mapnik_map import Map
from opus_core.indicator_framework.image_types.matplotlib_chart import Chart
from opus_core.indicator_framework.image_types.table import Table
from opus_core.indicator_framework.image_types.geotiff_map import GeotiffMap
from opus_core.indicator_framework.image_types.dataset_table import DatasetTable
from opus_core.indicator_framework.image_types.matplotlib_lorenzcurve import LorenzCurve
from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration

from opus_core.simulation_state import SimulationState
SimulationState().set_start_time(2014)

run_description = ''
cache_directory = r'/Volumes/e$/opusgit/urbansim_data/data/psrc_parcel/runs/run_74.run_2016_06_16_15_40'
cache_directory = r'/Volumes/d$/opusgit/urbansim_data/data/psrc_parcel/runs/run_64R.schools_distance_enrollment'

from opus_core.database_management.configurations.indicators_database_configuration import IndicatorsDatabaseConfiguration
from opus_core.database_management.database_server import DatabaseServer
  
#db_config = IndicatorsDatabaseConfiguration()
#db_server = DatabaseServer(db_config)
#database = db_server.get_database('hana_test')


source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2026, 2041],
    #years = [2041],
    #years = range(2014, 2041),
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['psrc_parcel','urbansim_parcel','psrc', 'urbansim','opus_core'],
        ),
    base_year=2014
)


indicators=[
   DatasetTable(
      source_data = source_data,
      dataset_name = 'school',
      name = 'number_of_students',
      attributes = ["name = school.sname",
                    "city = school.scity",
                    "parcel_id = school.parcel_id",
                    "category = school.category",
                    'number_of_students = school.aggregate(school.number_of_agents(person))',
                    'enrollment2014 = school.student_count2014 + school.fte2014',
                    "public = school.public"
                    ],
       output_type = 'csv',
          ),
       
]
from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory

IndicatorFactory().create_indicators(
     indicators = indicators,
     display_error_box = False, 
     show_results = False)    

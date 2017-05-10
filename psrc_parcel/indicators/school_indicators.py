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
#cache_directory = r'/urbansim_cache/psrc_parcel/run_5900.2008_04_02_12_40'
#cache_directory = r'/Users/hana/workspace/data/psrc_parcel/runs/run_35.2010_10_18_17_55'
#cache_directory = r'/Volumes/temp/2010 Nov/PeterC/UrbanSim/runs/run_40.2010_10_26_16_54'
#cache_directory = r'/Volumes/temp/2010 Nov/PeterC/UrbanSim/runs/run_41.2010_10_26_17_13'
#run_description = '(no build 11/26/2007)'
#cache_directory = r'D:\urbansim_cache\run_4169.2007_11_21_00_12'
#cache_directory = r'/Volumes/tmod3/urbansim_cache(Do not remove)/psrc_parcel/runs/copies/run_1.run_2010_11_10_16_24'
#cache_directory = r'/Users/hana/workspace/data/psrc_parcel/runs/run_refFinalDupNZ219'
#cache_directory = r'/Users/hana/workspace/data/psrc_parcel/base_year_estimation'
#cache_directory = r'/Users/hana/workspace/data/psrc_parcel/runs/run_75.2014_10_28_impr_base_scenario_fullTMtoll'
#cache_directory = r'/Users/hana/workspace/data/psrc_parcel/runs/run_81.2015_01_12_fullTMtoll'
#cache_directory = r'/Users/hana/workspace/data/psrc_parcel/runs/run_82.2015_01_12_noTM'
cache_directory = r'/Users/hana/workspace/data/psrc_parcel/runs/run_84.2015_02_24_luv_2010ELCMweights'
cache_directory = r'/Users/hana/workspace/data/psrc_parcel/runs/run_84_refined'
cache_directory = r'/Users/hana/workspace/data/psrc_parcel/runs/run_117'
#cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_114.run_2015_03_10_12_43'
cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_113.run_2015_03_09_18_08'
#cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_115.run_2015_03_10_17_32'
#cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_116.run_2015_03_16_18_15'
#cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_117.run_2015_03_27_17_36'
#cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_120.run_2015_03_31_23_00'
cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_121.run_2015_03_31_23_01'
#cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_122.run_2015_04_07_18_42'
cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_125.run_2015_04_13_17_38'
cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_126.run_2015_04_16_00_23'
#cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_129.run_2015_04_22_16_01'
cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_130.run_2015_05_01_21_07'
cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_131.run_2015_05_01_21_10'
cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_133.run_2015_05_08_10_27'
cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_138.run_2015_05_28_14_57'
#cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_81.run_2015_01_12_13_17_fullTMtoll'
#cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_139.run_2015_05_28_14_58'
cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/runs/run_142.run_2015_07_15_13_39'
#cache_directory = r'/Volumes/e$/opusgit/urbansim_data/data/psrc_parcel/runs/run_170.run_2015_09_15_16_02'
#cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/2040LUVrefinements/runs/run_173.run_2015_09_21_10_57'
#cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/2010refinements/runs/run_176.run_2015_09_30_10_41'
#cache_directory = r'/Volumes/e$/opus/data/psrc_parcel/2010refinements/runs/run_177.run_2015_10_06_17_08'
#cache_directory = r'/Volumes/DataTeam/Projects/UrbanSim/NEW_DIRECTORY/urbansim_cache/psrc_parcel/MR1_Apr14/refinements/run_245_w_faz_city_sfmf_flips_Final_MR1' # final MR1
#cache_directory = r'/Users/hana/workspace/data/psrc_parcel/runs/run_113'
#cache_directory = r'/Users/hana/workspace/data/psrc_parcel/runs/run_70.2014_10_20_frozen_skims_2026'
#cache_directory = r'/Users/hana/workspace/data/psrc_parcel/runs/run_67.2014_10_14_no_toll'
#cache_directory = r'/Users/hana/workspace/data/psrc_parcel/2010refinements/runs/run_5.off_run_178'
#cache_directory = r'/Users/hana/workspace/data/psrc_parcel/2010refinements/runs/run_473.2012_11_20_18_05'
#cache_directory = r'/Users/hana/workspace/data/psrc_parcel/2010refinements/base_year_data'
cache_directory = r'/Volumes/e$/opusgit/urbansim_data/data/psrc_parcel/runs/run_64.run_2016_05_04_15_02'
#cache_directory = r'/Volumes/e$/opusgit/urbansim_data/data/psrc_parcel/runs/run_66.run_2016_05_10_18_22'
cache_directory = r'/Volumes/e$/opusgit/urbansim_data/data/psrc_parcel/runs/run_68.run_2016_05_16_14_27'
cache_directory = r'/Volumes/e$/opusgit/urbansim_data/data/psrc_parcel/runs/run_69.run_2016_05_17_17_54'
cache_directory = r'/Volumes/e$/opusgit/urbansim_data/data/psrc_parcel/runs/run_71.run_2016_05_26_12_41'
cache_directory = r'/Volumes/e$/opusgit/urbansim_data/data/psrc_parcel/runs/run_73.run_2016_06_13_16_56'
cache_directory = r'/Volumes/e$/opusgit/urbansim_data/data/psrc_parcel/runs/run_72.run_2016_06_13_16_55'
cache_directory = r'/Volumes/e$/opusgit/urbansim_data/data/psrc_parcel/runs/run_74.run_2016_06_16_15_40'
cache_directory = r'/Volumes/d$/opusgit/urbansim_data/data/psrc_parcel/runs/run_64R.schools'

from opus_core.database_management.configurations.indicators_database_configuration import IndicatorsDatabaseConfiguration
from opus_core.database_management.database_server import DatabaseServer
  
#db_config = IndicatorsDatabaseConfiguration()
#db_server = DatabaseServer(db_config)
#database = db_server.get_database('hana_test')


source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2026, 2041],
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

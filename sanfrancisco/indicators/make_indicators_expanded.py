# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 



# script to produce a number of PSRC indicators --
# this illustrates using traits-based configurations programatically

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework.core.source_data import SourceData
from numpy import arange
from opus_core.indicator_framework.image_types.matplotlib_map import Map
from opus_core.indicator_framework.image_types.matplotlib_chart import Chart
from opus_core.indicator_framework.image_types.table import Table
from opus_core.indicator_framework.image_types.geotiff_map import GeotiffMap
from opus_core.indicator_framework.image_types.dataset_table import DatasetTable
from opus_core.indicator_framework.image_types.matplotlib_lorenzcurve import LorenzCurve
import os
run_description = '(baseline 11/02/2008)'
cache_directory = r'C:\opus\data\sanfrancisco\runs\run_18.run_2010_03_12_16_01'

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2001,2030],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['sanfrancisco','urbansim','opus_core'],
        ),
)
single_year_requests = [

       DatasetTable(
       source_data = source_data,
       dataset_name = 'tract',
       name = 'Tract Indicators',
       output_type='csv',
       attributes = [
                     'hholds_0_wrk=tract.aggregate(sanfrancisco.building.number_of_households_with_0_workers, intermediates=[parcel])',
                     'hholds_1_wrk =tract.aggregate(sanfrancisco.building.number_of_households_with_1_workers, intermediates=[parcel])',
                     'hholds_2_wrk=tract.aggregate(sanfrancisco.building.number_of_households_with_2_workers, intermediates=[parcel])',
                     'hholds_3_wrk=tract.aggregate(sanfrancisco.building.number_of_households_with_3_workers, intermediates=[parcel])',
                     'hholds_4_wrk=tract.aggregate(sanfrancisco.building.number_of_households_with_4_workers, intermediates=[parcel])',
                     'hoolds_5_wrk=tract.aggregate(sanfrancisco.building.number_of_households_with_5_workers, intermediates=[parcel])',
                     'hholds_6_wrk=tract.aggregate(sanfrancisco.building.number_of_households_with_6_workers, intermediates=[parcel])',
                     'hholds_7_wrk=tract.aggregate(sanfrancisco.building.number_of_households_with_7_workers, intermediates=[parcel])',
                     'res_units=tract.aggregate(sanfrancisco.building.residential_units, intermediates=[parcel])',
                     'res_sqft=tract.aggregate(sanfrancisco.building.residential_sqft, intermediates=[parcel])',
                     'avg_unit_price=tract.aggregate(sanfrancisco.building.unit_price, function=mean, intermediates=[parcel])',
                     'households=tract.aggregate(sanfrancisco.building.number_of_households, intermediates=[parcel])',
                     'population=tract.aggregate(sanfrancisco.building.population, intermediates=[parcel])',
                     'avg_hhsize=safe_array_divide(tract.aggregate(sanfrancisco.building.population, intermediates=[parcel]),tract.aggregate(sanfrancisco.building.number_of_households, intermediates=[parcel]))',
                     'sector_1_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_1, intermediates=[parcel])',
                     'sector_2_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_2, intermediates=[parcel])',
                     'sector_3_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_3, intermediates=[parcel])',
                     'sector_4_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_4, intermediates=[parcel])',
                     'sector_5_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_5, intermediates=[parcel])',
                     'sector_6_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_6, intermediates=[parcel])',
                    r"sector_CIE_emp=tract.aggregate(where(sanfrancisco.business.sector=='CIE',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_RET_emp=tract.aggregate(where(sanfrancisco.business.sector=='RETAIL/ENT',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_PDR_emp=tract.aggregate(where(sanfrancisco.business.sector=='PDR',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_MIPS_emp=tract.aggregate(where(sanfrancisco.business.sector=='MIPS',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_MED_emp=tract.aggregate(where(sanfrancisco.business.sector=='MED',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_VIS_emp=tract.aggregate(where(sanfrancisco.business.sector=='VISITOR',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                     'employment=tract.aggregate(sanfrancisco.building.employment, intermediates=[parcel])',
                     'sector_1_bus=tract.aggregate(business.sector_id == 1, intermediates=[building, parcel])',
                     'sector_2_bus=tract.aggregate(business.sector_id == 2, intermediates=[building, parcel])',
                     'sector_3_bus=tract.aggregate(business.sector_id == 3, intermediates=[building, parcel])',
                     'sector_4_bus=tract.aggregate(business.sector_id == 4, intermediates=[building, parcel])',
                     'sector_5_bus=tract.aggregate(business.sector_id == 5, intermediates=[building, parcel])',
                     'sector_6_bus=tract.aggregate(business.sector_id == 6, intermediates=[building, parcel])',
                     'businesses=tract.aggregate(sanfrancisco.building.number_of_businesses, intermediates=[parcel])',
                     'sqft_cie=tract.aggregate(where(sanfrancisco.building.building_use_id==7,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_retail=tract.aggregate(where(sanfrancisco.building.building_use_id==14,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_pdr=tract.aggregate(where(sanfrancisco.building.building_use_id==13,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_mips=tract.aggregate(where(sanfrancisco.building.building_use_id==8,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_visitor=tract.aggregate(where(sanfrancisco.building.building_use_id==17,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_nonres=tract.aggregate(sanfrancisco.building.non_residential_sqft, intermediates=[parcel])',
                     'empl_cie=tract.aggregate(where(sanfrancisco.building.building_use_id==7,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_retail=tract.aggregate(where(sanfrancisco.building.building_use_id==14,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_pdr=tract.aggregate(where(sanfrancisco.building.building_use_id==13,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_mips=tract.aggregate(where(sanfrancisco.building.building_use_id==8,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_visitor=tract.aggregate(where(sanfrancisco.building.building_use_id==17,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_med=tract.aggregate(where(sanfrancisco.building.building_use_id==18,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_mixres=tract.aggregate(where(sanfrancisco.building.building_use_id==9,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_mixed=tract.aggregate(where(sanfrancisco.building.building_use_id==10,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_nonres=tract.aggregate(sanfrancisco.building.employment, intermediates=[parcel])',
       ],
       #exclude_condition = '==0' #exclude_condition now accepts opus expressions
       ),
       DatasetTable(
       source_data = source_data,
       dataset_name = 'planning_district',
       name = 'planning_district_indicators',
       output_type='csv',
       attributes = [
                     'hholds_0_wrk=planning_district.aggregate(sanfrancisco.building.number_of_households_with_0_workers, intermediates=[parcel])',
                     'hholds_1_wrk =planning_district.aggregate(sanfrancisco.building.number_of_households_with_1_workers, intermediates=[parcel])',
                     'hholds_2_wrk=planning_district.aggregate(sanfrancisco.building.number_of_households_with_2_workers, intermediates=[parcel])',
                     'hholds_3_wrk=planning_district.aggregate(sanfrancisco.building.number_of_households_with_3_workers, intermediates=[parcel])',
                     'hholds_4_wrk=planning_district.aggregate(sanfrancisco.building.number_of_households_with_4_workers, intermediates=[parcel])',
                     'hoolds_5_wrk=planning_district.aggregate(sanfrancisco.building.number_of_households_with_5_workers, intermediates=[parcel])',
                     'hholds_6_wrk=planning_district.aggregate(sanfrancisco.building.number_of_households_with_6_workers, intermediates=[parcel])',
                     'hholds_7_wrk=planning_district.aggregate(sanfrancisco.building.number_of_households_with_7_workers, intermediates=[parcel])',
                     'res_units=planning_district.aggregate(sanfrancisco.building.residential_units, intermediates=[parcel])',
                     'res_sqft=planning_district.aggregate(sanfrancisco.building.residential_sqft, intermediates=[parcel])',
                     'avg_unit_price=planning_district.aggregate(where(sanfrancisco.building.residential_units>0,sanfrancisco.building.unit_price,0), function=mean, intermediates=[parcel])',
                     'stdev_unit_price=planning_district.aggregate(sanfrancisco.building.unit_price, function=standard_deviation, intermediates=[parcel])',
                     'stdev_unit_price2=planning_district.aggregate(where(sanfrancisco.building.residential_units>0,sanfrancisco.building.unit_price,0), function=standard_deviation, intermediates=[parcel])',
                     'households=planning_district.aggregate(sanfrancisco.building.number_of_households, intermediates=[parcel])',
                     'population=planning_district.aggregate(sanfrancisco.building.population, intermediates=[parcel])',
                     'avg_hhsize=safe_array_divide(planning_district.aggregate(sanfrancisco.building.population, intermediates=[parcel]),planning_district.aggregate(sanfrancisco.building.number_of_households, intermediates=[parcel]))',
                     'price_per_person=planning_district.aggregate(safe_array_divide(sanfrancisco.building.unit_price, sanfrancisco.building.population), function=mean, intermediates=[parcel])',
                     'sector_1_emp=planning_district.aggregate(sanfrancisco.building.employment_of_sector_1, intermediates=[parcel])',
                     'sector_2_emp=planning_district.aggregate(sanfrancisco.building.employment_of_sector_2, intermediates=[parcel])',
                     'sector_3_emp=planning_district.aggregate(sanfrancisco.building.employment_of_sector_3, intermediates=[parcel])',
                     'sector_4_emp=planning_district.aggregate(sanfrancisco.building.employment_of_sector_4, intermediates=[parcel])',
                     'sector_5_emp=planning_district.aggregate(sanfrancisco.building.employment_of_sector_5, intermediates=[parcel])',
                     'sector_6_emp=planning_district.aggregate(sanfrancisco.building.employment_of_sector_6, intermediates=[parcel])',
                    r"sector_CIE_emp=planning_district.aggregate(where(sanfrancisco.business.sector=='CIE',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_RET_emp=planning_district.aggregate(where(sanfrancisco.business.sector=='RETAIL/ENT',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_PDR_emp=planning_district.aggregate(where(sanfrancisco.business.sector=='PDR',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_MIPS_emp=planning_district.aggregate(where(sanfrancisco.business.sector=='MIPS',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_MED_emp=planning_district.aggregate(where(sanfrancisco.business.sector=='MED',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_VIS_emp=planning_district.aggregate(where(sanfrancisco.business.sector=='VISITOR',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r'employment=planning_district.aggregate(sanfrancisco.building.employment, intermediates=[parcel])',
                     'sector_1_bus=planning_district.aggregate(business.sector_id == 1, intermediates=[building, parcel])',
                     'sector_2_bus=planning_district.aggregate(business.sector_id == 2, intermediates=[building, parcel])',
                     'sector_3_bus=planning_district.aggregate(business.sector_id == 3, intermediates=[building, parcel])',
                     'sector_4_bus=planning_district.aggregate(business.sector_id == 4, intermediates=[building, parcel])',
                     'sector_5_bus=planning_district.aggregate(business.sector_id == 5, intermediates=[building, parcel])',
                     'sector_6_bus=planning_district.aggregate(business.sector_id == 6, intermediates=[building, parcel])',
                     'businesses=planning_district.aggregate(sanfrancisco.building.number_of_businesses, intermediates=[parcel])',
                     'sqft_cie=planning_district.aggregate(where(sanfrancisco.building.building_use_id==7,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_retail=planning_district.aggregate(where(sanfrancisco.building.building_use_id==14,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_pdr=planning_district.aggregate(where(sanfrancisco.building.building_use_id==13,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_mips=planning_district.aggregate(where(sanfrancisco.building.building_use_id==8,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_visitor=planning_district.aggregate(where(sanfrancisco.building.building_use_id==17,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_nonres=planning_district.aggregate(sanfrancisco.building.non_residential_sqft, intermediates=[parcel])',
                     'empl_cie=planning_district.aggregate(where(sanfrancisco.building.building_use_id==7,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_retail=planning_district.aggregate(where(sanfrancisco.building.building_use_id==14,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_pdr=planning_district.aggregate(where(sanfrancisco.building.building_use_id==13,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_mips=planning_district.aggregate(where(sanfrancisco.building.building_use_id==8,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_visitor=planning_district.aggregate(where(sanfrancisco.building.building_use_id==17,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_med=planning_district.aggregate(where(sanfrancisco.building.building_use_id==18,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_mixres=planning_district.aggregate(where(sanfrancisco.building.building_use_id==9,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_mixed=planning_district.aggregate(where(sanfrancisco.building.building_use_id==10,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_nonres=planning_district.aggregate(sanfrancisco.building.employment, intermediates=[parcel])',
                     'planning_district.district', 
                     
                     #'xxx=123',
                     #'planningdistrict=planning_district.get_data_element(planning_districts.district)'
                    
       ],
       #exclude_condition = '==0' #exclude_condition now accepts opus expressions
       ),
       DatasetTable(
       source_data = source_data,
       dataset_name = 'zone',
       name = 'zone Indicators',
       output_type='csv',
       attributes = [
                     'hholds_0_wrk=zone.aggregate(sanfrancisco.building.number_of_households_with_0_workers, intermediates=[parcel])',
                     'hholds_1_wrk =zone.aggregate(sanfrancisco.building.number_of_households_with_1_workers, intermediates=[parcel])',
                     'hholds_2_wrk=zone.aggregate(sanfrancisco.building.number_of_households_with_2_workers, intermediates=[parcel])',
                     'hholds_3_wrk=zone.aggregate(sanfrancisco.building.number_of_households_with_3_workers, intermediates=[parcel])',
                     'hholds_4_wrk=zone.aggregate(sanfrancisco.building.number_of_households_with_4_workers, intermediates=[parcel])',
                     'hoolds_5_wrk=zone.aggregate(sanfrancisco.building.number_of_households_with_5_workers, intermediates=[parcel])',
                     'hholds_6_wrk=zone.aggregate(sanfrancisco.building.number_of_households_with_6_workers, intermediates=[parcel])',
                     'hholds_7_wrk=zone.aggregate(sanfrancisco.building.number_of_households_with_7_workers, intermediates=[parcel])',
                     'res_units=zone.aggregate(sanfrancisco.building.residential_units, intermediates=[parcel])',
                     'res_sqft=zone.aggregate(sanfrancisco.building.residential_sqft, intermediates=[parcel])',
                     'avg_unit_price=zone.aggregate(sanfrancisco.building.unit_price, function=mean, intermediates=[parcel])','households=zone.aggregate(sanfrancisco.building.number_of_households, intermediates=[parcel])',
                     'population=zone.aggregate(sanfrancisco.building.population, intermediates=[parcel])',
                     'avg_hhsize=safe_array_divide(zone.aggregate(sanfrancisco.building.population, intermediates=[parcel]),zone.aggregate(sanfrancisco.building.number_of_households, intermediates=[parcel]))',
                     'sector_1_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_1, intermediates=[parcel])',
                     'sector_2_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_2, intermediates=[parcel])',
                     'sector_3_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_3, intermediates=[parcel])',
                     'sector_4_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_4, intermediates=[parcel])',
                     'sector_5_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_5, intermediates=[parcel])',
                     'sector_6_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_6, intermediates=[parcel])',
                     r"sector_CIE_emp=zone.aggregate(where(sanfrancisco.business.sector=='CIE',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                     r"sector_RET_emp=zone.aggregate(where(sanfrancisco.business.sector=='RETAIL/ENT',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                     r"sector_PDR_emp=zone.aggregate(where(sanfrancisco.business.sector=='PDR',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                     r"sector_MIPS_emp=zone.aggregate(where(sanfrancisco.business.sector=='MIPS',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                     r"sector_MED_emp=zone.aggregate(where(sanfrancisco.business.sector=='MED',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                     r"sector_VIS_emp=zone.aggregate(where(sanfrancisco.business.sector=='VISITOR',sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                     'employment=zone.aggregate(sanfrancisco.building.employment, intermediates=[parcel])',
                     'sector_1_bus=zone.aggregate(business.sector_id == 1, intermediates=[building, parcel])',
                     'sector_2_bus=zone.aggregate(business.sector_id == 2, intermediates=[building, parcel])',
                     'sector_3_bus=zone.aggregate(business.sector_id == 3, intermediates=[building, parcel])',
                     'sector_4_bus=zone.aggregate(business.sector_id == 4, intermediates=[building, parcel])',
                     'sector_5_bus=zone.aggregate(business.sector_id == 5, intermediates=[building, parcel])',
                     'sector_6_bus=zone.aggregate(business.sector_id == 6, intermediates=[building, parcel])',
                     'businesses=zone.aggregate(sanfrancisco.building.number_of_businesses, intermediates=[parcel])',
                     'sqft_cie=zone.aggregate(where(sanfrancisco.building.building_use_id==7,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_retail=zone.aggregate(where(sanfrancisco.building.building_use_id==14,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_pdr=zone.aggregate(where(sanfrancisco.building.building_use_id==13,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_mips=zone.aggregate(where(sanfrancisco.building.building_use_id==8,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_visitor=zone.aggregate(where(sanfrancisco.building.building_use_id==17,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_nonres=zone.aggregate(sanfrancisco.building.non_residential_sqft, intermediates=[parcel])',
                     'empl_cie=zone.aggregate(where(sanfrancisco.building.building_use_id==7,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_retail=zone.aggregate(where(sanfrancisco.building.building_use_id==14,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_pdr=zone.aggregate(where(sanfrancisco.building.building_use_id==13,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_mips=zone.aggregate(where(sanfrancisco.building.building_use_id==8,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_visitor=zone.aggregate(where(sanfrancisco.building.building_use_id==17,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_med=zone.aggregate(where(sanfrancisco.building.building_use_id==18,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_mixres=zone.aggregate(where(sanfrancisco.building.building_use_id==9,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_mixed=zone.aggregate(where(sanfrancisco.building.building_use_id==10,sanfrancisco.building.employment,0), intermediates=[parcel])',
                     'empl_nonres=zone.aggregate(sanfrancisco.building.employment, intermediates=[parcel])',
                     #'empl_nonres=zone.aggregate(sanfrancisco.business.employment, intermediates=[parcel])',
       ],       #exclude_condition = '==0' #exclude_condition now accepts opus expressions
),

    ]

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [2001,2030],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['sanfrancisco','urbansim','opus_core'],
        ),
)

multi_year_requests = [
    #Chart(
        #attribute = 'bus_ = alldata.aggregate_all(business.sector_id == 1)',
        #dataset_name = 'alldata',
        #source_data = source_data,
        #years=arange(2001,2026),
        #),

    Table(
    source_data = source_data,
    dataset_name = 'alldata',
    name = 'Business Counts 1',
    output_type='csv',
    attribute = 'bus_1 = alldata.aggregate_all(business.sector_id == 1)',
    years = [2001, 2002],
    ),

    Table(
    source_data = source_data,
    dataset_name = 'alldata',
    name = 'Business Counts 2',
    output_type='csv',
    attribute = 'bus_2 = alldata.aggregate_all(business.sector_id == 2)',
    years = [2001, 2002],
    ),

    Table(
    source_data = source_data,
    dataset_name = 'alldata',
    name = 'Business Counts 3',
    output_type='csv',
    attribute = 'bus_3 = alldata.aggregate_all(business.sector_id == 3)',
    years = [2001, 2002],
    ),

    Table(
    source_data = source_data,
    dataset_name = 'alldata',
    name = 'Business Counts 4',
    output_type='csv',
    attribute = 'bus_4 = alldata.aggregate_all(business.sector_id == 4)',
    years = [2001, 2002],
    ),

    Table(
    source_data = source_data,
    dataset_name = 'alldata',
    name = 'Business Counts 5',
    output_type='csv',
    attribute = 'bus_5 = alldata.aggregate_all(business.sector_id == 5)',
    years = [2001, 2002],
    ),

    Table(
    source_data = source_data,
    dataset_name = 'alldata',
    name = 'Business Counts 6',
    output_type='csv',
    attribute = 'bus_6 = alldata.aggregate_all(business.sector_id == 6)',
    years = [2001, 2002],
    ),
]

if __name__ == '__main__':
    from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory

    IndicatorFactory().create_indicators(
        indicators = single_year_requests,
        display_error_box = False,
        show_results = True)
    #IndicatorFactory().create_indicators(
        #indicators = multi_year_requests,
        #display_error_box = False,
        #show_results = True)
 
   
#===============================================================================
#    for root, dirs, files in os.walk(cache_directory):
#        for name in files:
#            try:
#                filename = os.path.join(root, name)
#                if 'tract__dataset_table__' in filename:
#                    newfilename=os.path.join(root, 'census_'+name)
#                    os.rename(filename, newfilename)
#                    print newfilename
#            except:
#                pass
#===============================================================================

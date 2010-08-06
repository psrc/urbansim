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
cache_directory = r'C:\opus\data\sanfrancisco\runs\run_183.SFBaseyr2009_2010Jul02Fri_1257_Sim2010to2035'
yearstart=2010
yearend=2035
source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [yearstart,yearend],
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
                     'avg_total_price=tract.aggregate(sanfrancisco.building.total_price, function=mean, intermediates=[parcel])',
                     'households=tract.aggregate(sanfrancisco.building.number_of_households, intermediates=[parcel])',
                     'population=tract.aggregate(sanfrancisco.building.population, intermediates=[parcel])',
                     'avg_hhsize=safe_array_divide(tract.aggregate(sanfrancisco.building.population, intermediates=[parcel]),tract.aggregate(sanfrancisco.building.number_of_households, intermediates=[parcel]))',
                     'sector_1_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_1, intermediates=[parcel])',
                     'sector_2_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_2, intermediates=[parcel])',
                     'sector_3_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_3, intermediates=[parcel])',
                     'sector_4_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_4, intermediates=[parcel])',
                     'sector_5_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_5, intermediates=[parcel])',
                     'sector_6_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_6, intermediates=[parcel])',
                     'sector_7_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_7, intermediates=[parcel])',
                     'sector_8_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_8, intermediates=[parcel])',
                     'sector_9_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_9, intermediates=[parcel])',
                     'sector_10_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_10, intermediates=[parcel])',
                     'sector_11_emp=tract.aggregate(sanfrancisco.building.employment_of_sector_11, intermediates=[parcel])',
                    r"sector_CIE_emp=tract.aggregate(where(sanfrancisco.business.activity_id==1,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_RET_emp=tract.aggregate(where(sanfrancisco.business.activity_id==5,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_PDR_emp=tract.aggregate(where(sanfrancisco.business.activity_id==4,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_MIPS_emp=tract.aggregate(where(sanfrancisco.business.activity_id==3,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_MED_emp=tract.aggregate(where(sanfrancisco.business.activity_id==2,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_VIS_emp=tract.aggregate(where(sanfrancisco.business.activity_id==6,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                     'employment=tract.aggregate(sanfrancisco.building.employment, intermediates=[parcel])',
                     'sector_1_bus=tract.aggregate(business.sector_id == 1, intermediates=[building, parcel])',
                     'sector_2_bus=tract.aggregate(business.sector_id == 2, intermediates=[building, parcel])',
                     'sector_3_bus=tract.aggregate(business.sector_id == 3, intermediates=[building, parcel])',
                     'sector_4_bus=tract.aggregate(business.sector_id == 4, intermediates=[building, parcel])',
                     'sector_5_bus=tract.aggregate(business.sector_id == 5, intermediates=[building, parcel])',
                     'sector_6_bus=tract.aggregate(business.sector_id == 6, intermediates=[building, parcel])',
                     'sector_7_bus=tract.aggregate(business.sector_id == 7, intermediates=[building, parcel])',
                     'sector_8_bus=tract.aggregate(business.sector_id == 8, intermediates=[building, parcel])',
                     'sector_9_bus=tract.aggregate(business.sector_id == 9, intermediates=[building, parcel])',
                     'sector_10_bus=tract.aggregate(business.sector_id == 10, intermediates=[building, parcel])',
                     'sector_11_bus=tract.aggregate(business.sector_id == 11, intermediates=[building, parcel])',
                     'businesses=tract.aggregate(sanfrancisco.building.number_of_businesses, intermediates=[parcel])',
                     'sqft_cie=tract.aggregate(where(sanfrancisco.building.building_use_id==7,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_retail=tract.aggregate(where(sanfrancisco.building.building_use_id==14,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_pdr=tract.aggregate(where(sanfrancisco.building.building_use_id==13,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_mips=tract.aggregate(where(sanfrancisco.building.building_use_id==8,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_visitor=tract.aggregate(where(sanfrancisco.building.building_use_id==17,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel])',
                     'sqft_nonres=tract.aggregate(sanfrancisco.building.non_residential_sqft, intermediates=[parcel])',
       ],
       #exclude_condition = '==0' #exclude_condition now accepts opus expressions
       ),
       DatasetTable(
       source_data = source_data,
       dataset_name = 'pdist',
       name = 'pdist_indicators',
       output_type='csv',
       attributes = ['pdist.district',
                     'hholds_0_wrk=pdist.aggregate(sanfrancisco.building.number_of_households_with_0_workers, intermediates=[parcel])',
                     'hholds_1_wrk =pdist.aggregate(sanfrancisco.building.number_of_households_with_1_workers, intermediates=[parcel])',
                     'hholds_2_wrk=pdist.aggregate(sanfrancisco.building.number_of_households_with_2_workers, intermediates=[parcel])',
                     'hholds_3_wrk=pdist.aggregate(sanfrancisco.building.number_of_households_with_3_workers, intermediates=[parcel])',
                     'hholds_4_wrk=pdist.aggregate(sanfrancisco.building.number_of_households_with_4_workers, intermediates=[parcel])',
                     'hholds_5_wrk=pdist.aggregate(sanfrancisco.building.number_of_households_with_5_workers, intermediates=[parcel])',
                     'hholds_6_wrk=pdist.aggregate(sanfrancisco.building.number_of_households_with_6_workers, intermediates=[parcel])',
                     'hholds_7_wrk=pdist.aggregate(sanfrancisco.building.number_of_households_with_7_workers, intermediates=[parcel])',
                     'res_units=pdist.aggregate(sanfrancisco.building.residential_units, intermediates=[parcel])',
                     'res_sqft=pdist.aggregate(sanfrancisco.building.residential_sqft, intermediates=[parcel])',
                     'avg_total_price=pdist.aggregate(where(sanfrancisco.building.residential_units>0,sanfrancisco.building.total_price,0), function=mean, intermediates=[parcel])',
                     'stdev_total_price=pdist.aggregate(sanfrancisco.building.total_price, function=standard_deviation, intermediates=[parcel])',
                     'stdev_total_price2=pdist.aggregate(where(sanfrancisco.building.residential_units>0,sanfrancisco.building.total_price,0), function=standard_deviation, intermediates=[parcel])',
                     'households=pdist.aggregate(sanfrancisco.building.number_of_households, intermediates=[parcel])',
                     'population=pdist.aggregate(sanfrancisco.building.population, intermediates=[parcel])',
                     'avg_hhsize=safe_array_divide(pdist.aggregate(sanfrancisco.building.population, intermediates=[parcel]),pdist.aggregate(sanfrancisco.building.number_of_households, intermediates=[parcel]))',
                     'price_per_person=pdist.aggregate(safe_array_divide(sanfrancisco.building.total_price, sanfrancisco.building.population), function=mean, intermediates=[parcel])',
                     'ag_natural_resources_emp=pdist.aggregate(sanfrancisco.building.employment_of_sector_1, intermediates=[parcel])',
                     'construction_emp=pdist.aggregate(sanfrancisco.building.employment_of_sector_2, intermediates=[parcel])',
                     'manufacturing_wholesale_emp=pdist.aggregate(sanfrancisco.building.employment_of_sector_3, intermediates=[parcel])',
                     'retail_emp=pdist.aggregate(sanfrancisco.building.employment_of_sector_4, intermediates=[parcel])',
                     'transportation_utilities_emp=pdist.aggregate(sanfrancisco.building.employment_of_sector_5, intermediates=[parcel])',
                     'information_emp=pdist.aggregate(sanfrancisco.building.employment_of_sector_6, intermediates=[parcel])',
                     'financial_leasing_emp=pdist.aggregate(sanfrancisco.building.employment_of_sector_7, intermediates=[parcel])',
                     'prof_managerial_services_emp=pdist.aggregate(sanfrancisco.building.employment_of_sector_8, intermediates=[parcel])',
                     'health_educ_services_emp=pdist.aggregate(sanfrancisco.building.employment_of_sector_9, intermediates=[parcel])',
                     'arts_rec_other_services_emp=pdist.aggregate(sanfrancisco.building.employment_of_sector_10, intermediates=[parcel])',
                     'government_emp=pdist.aggregate(sanfrancisco.building.employment_of_sector_11, intermediates=[parcel])',
                    r"sector_CIE_emp=pdist.aggregate(where(sanfrancisco.business.activity_id==1,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_RET_emp=pdist.aggregate(where(sanfrancisco.business.activity_id==5,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_PDR_emp=pdist.aggregate(where(sanfrancisco.business.activity_id==4,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_MIPS_emp=pdist.aggregate(where(sanfrancisco.business.activity_id==3,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_MED_emp=pdist.aggregate(where(sanfrancisco.business.activity_id==2,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r"sector_VIS_emp=pdist.aggregate(where(sanfrancisco.business.activity_id==6,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                    r'employment=pdist.aggregate(sanfrancisco.building.employment, intermediates=[parcel])',
                     'ag_natural_resources_bus=pdist.aggregate(business.sector_id == 1, intermediates=[building, parcel])',
                     'construction_bus=pdist.aggregate(business.sector_id == 2, intermediates=[building, parcel])',
                     'manufacturing_wholesale_bus=pdist.aggregate(business.sector_id == 3, intermediates=[building, parcel])',
                     'retail_bus=pdist.aggregate(business.sector_id == 4, intermediates=[building, parcel])',
                     'transportation_utilities_bus=pdist.aggregate(business.sector_id == 5, intermediates=[building, parcel])',
                     'information_bus=pdist.aggregate(business.sector_id == 6, intermediates=[building, parcel])',
                     'financial_leasing_bus=pdist.aggregate(business.sector_id == 7, intermediates=[building, parcel])',
                     'prof_managerial_services_bus=pdist.aggregate(business.sector_id == 8, intermediates=[building, parcel])',
                     'health_educ_services_bus=pdist.aggregate(business.sector_id == 9, intermediates=[building, parcel])',
                     'arts_rec_other_services_bus=pdist.aggregate(business.sector_id == 10, intermediates=[building, parcel])',
                     'government_bus=pdist.aggregate(business.sector_id == 11, intermediates=[building, parcel])',
                     'businesses=pdist.aggregate(sanfrancisco.building.number_of_businesses, intermediates=[parcel])',
                     'office_sqft=pdist.aggregate(where(sanfrancisco.building.building_type_id==10,sanfrancisco.building.building_sqft,0), intermediates=[parcel])',
                     'office_occ=safe_array_divide(pdist.aggregate(where(sanfrancisco.business.activity_id==3,sanfrancisco.business.sqft,0), intermediates=[building, parcel]),pdist.aggregate(where(sanfrancisco.building.building_type_id==10,sanfrancisco.building.non_residential_sqft,0), intermediates=[parcel]))'


                     #'xxx=123',
                     #'planningdistrict=pdist.get_data_element(pdists.district)'

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
                     'avg_total_price=zone.aggregate(sanfrancisco.building.total_price, function=mean, intermediates=[parcel])','households=zone.aggregate(sanfrancisco.building.number_of_households, intermediates=[parcel])',
                     'population=zone.aggregate(sanfrancisco.building.population, intermediates=[parcel])',
                     'avg_hhsize=safe_array_divide(zone.aggregate(sanfrancisco.building.population, intermediates=[parcel]),zone.aggregate(sanfrancisco.building.number_of_households, intermediates=[parcel]))',
                     'sector_1_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_1, intermediates=[parcel])',
                     'sector_2_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_2, intermediates=[parcel])',
                     'sector_3_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_3, intermediates=[parcel])',
                     'sector_4_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_4, intermediates=[parcel])',
                     'sector_5_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_5, intermediates=[parcel])',
                     'sector_6_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_6, intermediates=[parcel])',
                     'sector_7_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_7, intermediates=[parcel])',
                     'sector_8_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_8, intermediates=[parcel])',
                     'sector_9_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_9, intermediates=[parcel])',
                     'sector_10_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_10, intermediates=[parcel])',
                     'sector_11_emp=zone.aggregate(sanfrancisco.building.employment_of_sector_11, intermediates=[parcel])',
                     r"sector_CIE_emp=zone.aggregate(where(sanfrancisco.business.activity_id==1,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                     r"sector_RET_emp=zone.aggregate(where(sanfrancisco.business.activity_id==5,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                     r"sector_PDR_emp=zone.aggregate(where(sanfrancisco.business.activity_id==4,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                     r"sector_MIPS_emp=zone.aggregate(where(sanfrancisco.business.activity_id==3,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                     r"sector_MED_emp=zone.aggregate(where(sanfrancisco.business.activity_id==2,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                     r"sector_VIS_emp=zone.aggregate(where(sanfrancisco.business.activity_id==6,sanfrancisco.business.employment,0), intermediates=[building, parcel])",
                     'employment=zone.aggregate(sanfrancisco.building.employment, intermediates=[parcel])',
                     'sector_1_bus=zone.aggregate(business.sector_id == 1, intermediates=[building, parcel])',
                     'sector_2_bus=zone.aggregate(business.sector_id == 2, intermediates=[building, parcel])',
                     'sector_3_bus=zone.aggregate(business.sector_id == 3, intermediates=[building, parcel])',
                     'sector_4_bus=zone.aggregate(business.sector_id == 4, intermediates=[building, parcel])',
                     'sector_5_bus=zone.aggregate(business.sector_id == 5, intermediates=[building, parcel])',
                     'sector_6_bus=zone.aggregate(business.sector_id == 6, intermediates=[building, parcel])',
                     'sector_7_bus=zone.aggregate(business.sector_id == 7, intermediates=[building, parcel])',
                     'sector_8_bus=zone.aggregate(business.sector_id == 8, intermediates=[building, parcel])',
                     'sector_9_bus=zone.aggregate(business.sector_id == 9, intermediates=[building, parcel])',
                     'sector_10_bus=zone.aggregate(business.sector_id == 10, intermediates=[building, parcel])',
                     'sector_11_bus=zone.aggregate(business.sector_id == 11, intermediates=[building, parcel])',
                     'businesses=zone.aggregate(sanfrancisco.building.number_of_businesses, intermediates=[parcel])']
                     #exclude_condition = '==0' #exclude_condition now accepts opus expressions
),

    ]

source_data = SourceData(
    cache_directory = cache_directory,
    run_description = run_description,
    years = [yearstart,yearend],
    dataset_pool_configuration = DatasetPoolConfiguration(
        package_order=['sanfrancisco','urbansim','opus_core'],
        ),
)

multi_year_requests = [
    #Chart(
        #attribute = 'bus_ = alldata.aggregate_all(business.activity_id == 1)',
        #dataset_name = 'alldata',
        #source_data = source_data,
        #years=arange(yearstart, yearend),
        #),



    Table(
    source_data = source_data,
    dataset_name = 'pdist',
    name = 'residential units',
    output_type='csv',
    attribute =  'res_units=pdist.aggregate(sanfrancisco.building.residential_units, intermediates=[parcel])',
    years = [2010,2012,2014,2016,2018,2020,2022,2024,2026,2028,2030],
    ),

]

if __name__ == '__main__':
    from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory

    IndicatorFactory().create_indicators(
        indicators = single_year_requests,
        display_error_box = False,
        show_results = True)
    #===========================================================================
    # IndicatorFactory().create_indicators(
    #    indicators = multi_year_requests,
    #    display_error_box = False,
    #    show_results = True)
    #===========================================================================


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

# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE



# script to produce a number of PSRC indicators --
# this illustrates using traits-based configurations programatically

from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from opus_core.indicator_framework.core.source_data import SourceData
from opus_core.indicator_framework.image_types.table import Table
from opus_core.indicator_framework.image_types.dataset_table import DatasetTable
from opus_core.indicator_framework.core.indicator_factory import IndicatorFactory
from opus_core.logger import logger
from opus_core.configurations.xml_configuration import XMLConfiguration
from time import time,localtime,strftime,sleep
import csv,os,sys

def make_topsheet(cache_directory):
    """ Run the indicators for the LU topsheet
    """
    run_description = '(baseline 11/02/2008)'
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
           attributes = ['hholds_0_wrk=tract.aggregate(sanfrancisco.building.number_of_households_with_0_workers, intermediates=[parcel])',
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

    IndicatorFactory().create_indicators(
        indicators = single_year_requests,
        display_error_box = False,
        show_results = False)

def make_multiyear_workbook(cache_directory, yearstart=2010, yearend=2035):
    """ This spits out the indicators for a multiyear workbook and then combines them 
        into a single file, cache_directory/alldata.csv
        You can then copy this a copy of the MultiyearLU_template.xls and see some basic
          performance/troubleshooting graphs for the various submodels.
    """
    
    multiyear_workbook_source_data = SourceData(
        cache_directory = cache_directory,
        run_description = "Run description is used for what?",
        years = list(range(yearstart,yearend+1)),
        dataset_pool_configuration = DatasetPoolConfiguration(
            package_order=['sanfrancisco','urbansim','opus_core'],
        ),
    )
    
    multiyear_workbook_alldata_attributes = \
    [
        # commercial
        'bldg_count_comm=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==1,1,0))',
        'bldg_occsqft_comm=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==1,sanfrancisco.building.occupied_sqft,0))',
        'bldg_count_totsqft_comm=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==1,sanfrancisco.building.non_residential_sqft,0))',
        'bldg_vacrate_comm=(alldata.aggregate_all(where(sanfrancisco.building.building_group_id==1,sanfrancisco.building.non_residential_sqft,0))-' + 
                           'alldata.aggregate_all(where(sanfrancisco.building.building_group_id==1,sanfrancisco.building.occupied_sqft,0)))/' + 
                           'alldata.aggregate_all(where(sanfrancisco.building.building_group_id==1,sanfrancisco.building.non_residential_sqft,0))',
        'bldg_count_totunit_comm=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==1,sanfrancisco.building.residential_units,0))',

        # institutional
        'bldg_count_inst=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==2,1,0))',
        'bldg_occsqft_inst=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==2,sanfrancisco.building.occupied_sqft,0))',
        'bldg_count_totsqft_inst=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==2,sanfrancisco.building.non_residential_sqft,0))',
        'bldg_vacrate_inst=(alldata.aggregate_all(where(sanfrancisco.building.building_group_id==2,sanfrancisco.building.non_residential_sqft,0))-' + 
                           'alldata.aggregate_all(where(sanfrancisco.building.building_group_id==2,sanfrancisco.building.occupied_sqft,0)))/' + 
                           'alldata.aggregate_all(where(sanfrancisco.building.building_group_id==2,sanfrancisco.building.non_residential_sqft,0))',
        'bldg_count_totunit_inst=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==2,sanfrancisco.building.residential_units,0))',

        # office
        'bldg_count_offc=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==3,1,0))',
        'bldg_occsqft_offc=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==3,sanfrancisco.building.occupied_sqft,0))',
        'bldg_count_totsqft_offc=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==3,sanfrancisco.building.non_residential_sqft,0))',
        'bldg_vacrate_offc=(alldata.aggregate_all(where(sanfrancisco.building.building_group_id==3,sanfrancisco.building.non_residential_sqft,0))-' + 
                           'alldata.aggregate_all(where(sanfrancisco.building.building_group_id==3,sanfrancisco.building.occupied_sqft,0)))/' + 
                           'alldata.aggregate_all(where(sanfrancisco.building.building_group_id==3,sanfrancisco.building.non_residential_sqft,0))',
        'bldg_count_totunit_offc=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==3,sanfrancisco.building.residential_units,0))',

        # residential
        'bldg_count_res=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==4,1,0))',
        'bldg_occunit_res=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==4,sanfrancisco.building.number_of_households,0))',
        'bldg_count_totunit_res=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==4,sanfrancisco.building.residential_units,0))',
        'bldg_vacrate_res=(alldata.aggregate_all(where(sanfrancisco.building.building_group_id==4,sanfrancisco.building.residential_units,0))-' + 
                          'alldata.aggregate_all(where(sanfrancisco.building.building_group_id==4,sanfrancisco.building.number_of_households,0)))/' + 
                          'alldata.aggregate_all(where(sanfrancisco.building.building_group_id==4,sanfrancisco.building.residential_units,0))',
        'bldg_count_totsqft_res=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==4,sanfrancisco.building.non_residential_sqft,0))',

        # res in non-res group buildings
        'bldg_count_reso=alldata.aggregate_all(where(sanfrancisco.building.building_group_id!=4,1,0))',
        'bldg_occunit_reso=alldata.aggregate_all(where(sanfrancisco.building.building_group_id!=4,sanfrancisco.building.number_of_households,0))',
        'bldg_count_totunit_reso=alldata.aggregate_all(where(sanfrancisco.building.building_group_id!=4,sanfrancisco.building.residential_units,0))',
        'bldg_vacrate_reso=(alldata.aggregate_all(where(sanfrancisco.building.building_group_id!=4,sanfrancisco.building.residential_units,0))-' + 
                           'alldata.aggregate_all(where(sanfrancisco.building.building_group_id!=4,sanfrancisco.building.number_of_households,0)))/' + 
                           'alldata.aggregate_all(where(sanfrancisco.building.building_group_id!=4,sanfrancisco.building.residential_units,0))',
        'bldg_count_totsqft_ores=alldata.aggregate_all(where(sanfrancisco.building.building_group_id!=4,sanfrancisco.building.non_residential_sqft,0))',
    
        # visitor
        'bldg_count_vis=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==5,1,0))',
        'bldg_occsqft_vis=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==5,sanfrancisco.building.occupied_sqft,0))',
        'bldg_count_totsqft_vis=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==5,sanfrancisco.building.non_residential_sqft,0))',
        'bldg_vacrate_vis=(alldata.aggregate_all(where(sanfrancisco.building.building_group_id==5,sanfrancisco.building.non_residential_sqft,0))-' + 
                          'alldata.aggregate_all(where(sanfrancisco.building.building_group_id==5,sanfrancisco.building.occupied_sqft,0)))/' + 
                          'alldata.aggregate_all(where(sanfrancisco.building.building_group_id==5,sanfrancisco.building.non_residential_sqft,0))',
        'bldg_count_totunit_vis=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==5,sanfrancisco.building.residential_units,0))',
    
        # mixed
        'bldg_count_mix=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==6,1,0))',
        'bldg_occsqft_mix=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==6,sanfrancisco.building.occupied_sqft,0))',
        'bldg_count_totsqft_mix=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==6,sanfrancisco.building.non_residential_sqft,0))',
        'bldg_vacrate_mix=(alldata.aggregate_all(where(sanfrancisco.building.building_group_id==6,sanfrancisco.building.non_residential_sqft,0))-' + 
                           'alldata.aggregate_all(where(sanfrancisco.building.building_group_id==6,sanfrancisco.building.occupied_sqft,0)))/' + 
                           'alldata.aggregate_all(where(sanfrancisco.building.building_group_id==6,sanfrancisco.building.non_residential_sqft,0))',
        'bldg_count_totunit_mix=alldata.aggregate_all(where(sanfrancisco.building.building_group_id==6,sanfrancisco.building.residential_units,0))',
                           
        # unplaced buildings
        'bldg_count_unplaced=alldata.aggregate_all(where(sanfrancisco.building.parcel_id<0,1,0))',
        'bldg_count_unplaced_BLCMspec=alldata.aggregate_all(where(numpy.logical_and(sanfrancisco.building.parcel_id<0,sanfrancisco.building.is_placed_type>0),1,0))',
        'bldg_count_unplaced_noBLCMspec=alldata.aggregate_all(where(numpy.logical_and(sanfrancisco.building.parcel_id<0,sanfrancisco.building.is_placed_type==0),1,0))',
    
        # household counts
        'hhld_count_sz1=alldata.aggregate_all(where(household.household_size==1,1,0))',
        'hhld_count_sz2=alldata.aggregate_all(where(household.household_size==2,1,0))',
        'hhld_count_sz34=alldata.aggregate_all(where(numpy.logical_or(household.household_size==3,household.household_size==4),1,0))',
        'hhld_count_sz56=alldata.aggregate_all(where(numpy.logical_or(household.household_size==5,household.household_size==6),1,0))',
        'hhld_count_sz7=alldata.aggregate_all(where(household.household_size>=7,1,0))',
        
        # business counts
        'jobs_count_sect1=alldata.aggregate_all(where(business.sector_id==1,business.employment,0))',
        'jobs_count_sect2=alldata.aggregate_all(where(business.sector_id==2,business.employment,0))',
        'jobs_count_sect3=alldata.aggregate_all(where(business.sector_id==3,business.employment,0))',
        'jobs_count_sect4=alldata.aggregate_all(where(business.sector_id==4,business.employment,0))',
        'jobs_count_sect5=alldata.aggregate_all(where(business.sector_id==5,business.employment,0))',
        'jobs_count_sect6=alldata.aggregate_all(where(business.sector_id==6,business.employment,0))',
        'jobs_count_sect7=alldata.aggregate_all(where(business.sector_id==7,business.employment,0))',
        'jobs_count_sect8=alldata.aggregate_all(where(business.sector_id==8,business.employment,0))',
        'jobs_count_sect9=alldata.aggregate_all(where(business.sector_id==9,business.employment,0))',
        'jobs_count_sect10=alldata.aggregate_all(where(business.sector_id==10,business.employment,0))',
        'jobs_count_sect11=alldata.aggregate_all(where(business.sector_id==11,business.employment,0))',
        
        # unplaced businesses, how full are buildings?  overall nonres sqft totals
        'business_count_unplaced=alldata.aggregate_all(where(business.building_id<1,1,0))',
        'bldg_count_overfullbiz=alldata.aggregate_all(where(numpy.logical_and(sanfrancisco.building.occupied_sqft>building.non_residential_sqft,'+
                                          'building.non_residential_sqft>0),1,0))',
        'bldg_count_overfullbiz0=alldata.aggregate_all(where(numpy.logical_and(sanfrancisco.building.occupied_sqft>building.non_residential_sqft,'+
                                          'building.non_residential_sqft==0),1,0))',
        'bldg_count_partialfullbiz=alldata.aggregate_all(where(numpy.logical_and(sanfrancisco.building.occupied_sqft<building.non_residential_sqft,'+
                                                                                'sanfrancisco.building.occupied_sqft>0),1,0))',
        'bldg_count_vacantbiz=alldata.aggregate_all(where(numpy.logical_and(building.non_residential_sqft>0,'+
                                                                           'sanfrancisco.building.occupied_sqft==0),1,0))',
        # these are covered above for building_groups
        'bldg_nonres_sqft_total=alldata.aggregate_all(building.non_residential_sqft)',
        'bldg_nonres_sqft_occ=alldata.aggregate_all(sanfrancisco.building.occupied_sqft)',
        'bldg_nonres_sqft_vacant=alldata.aggregate_all(building.non_residential_sqft)-alldata.aggregate_all(sanfrancisco.building.occupied_sqft)',

        # unplaced households, how full are buildings?  overall hhunit totals
        'hhld_count_unplaced=alldata.aggregate_all(where(household.building_id<1,1,0))',
        'hhld_count_overfullhh=alldata.aggregate_all(where(numpy.logical_and(sanfrancisco.building.number_of_households>building.residential_units,'+
                                                                        'building.residential_units>0),1,0))',
        'hhld_count_overfullhh0=alldata.aggregate_all(where(numpy.logical_and(sanfrancisco.building.number_of_households>building.residential_units,'+
                                                                        'building.residential_units==0),1,0))',
        'hhld_count_partialfullhh=alldata.aggregate_all(where(numpy.logical_and(sanfrancisco.building.number_of_households<building.residential_units,'+
                                                                                'sanfrancisco.building.number_of_households>0),1,0))',
        'hhld_count_vacanthh=alldata.aggregate_all(where(numpy.logical_and(building.residential_units>0,'+
                                                                          'sanfrancisco.building.number_of_households==0),1,0))',
        # these are covered above for building_groups
        'hhld_res_unit_total=alldata.aggregate_all(building.residential_units)',
        'hhld_res_unit_occ=alldata.aggregate_all(sanfrancisco.building.number_of_households)',
        'hhld_res_unit_vacant=alldata.aggregate_all(building.residential_units)-alldata.aggregate_all(sanfrancisco.building.number_of_households)',

    ]

    
    class SFIndicatorDialect(csv.excel):
        lineterminator = '\n'        
    csv.register_dialect("SFIndicatorDialect", SFIndicatorDialect)
    
    onetableWriter = csv.writer(open(os.path.join(cache_directory,"alldata.csv"),'w'),
                                dialect='SFIndicatorDialect')
    headeryears = []
    for year in multiyear_workbook_source_data.years:
        headeryears.append("y"+str(year))
    onetableWriter.writerow(['variable']+headeryears)
    
    for attr in multiyear_workbook_alldata_attributes:
        attr_name = attr.partition('=')[0]
        request = [ Table( source_data = multiyear_workbook_source_data,
                           dataset_name = 'alldata',
                           name = attr_name,
                           attribute = attr
                          ) 
                   ]
        IndicatorFactory().create_indicators(indicators = request,
                                             display_error_box = False,
                                             show_results = False)
        # open this file
        filename = request[0].get_file_path()
        indicatorReader = csv.reader(open(filename,'r'))
        
        # title row
        fields = next(indicatorReader) 
        assert(len(fields)==len(multiyear_workbook_source_data.years)+1) # quick check
        
        # data row
        fields = next(indicatorReader)
        fields[0] = attr_name
        onetableWriter.writerow(fields)
        
        # for *_count_* rows, add *_new_* row
        if attr_name.find("_count_") >= 0:
            attr_new_name = attr_name.replace("_count_","_new_")
            new_fields = [ attr_new_name, 0 ]
            for ind in range(1,len(multiyear_workbook_source_data.years)):
                new_fields.append(float(fields[ind+1])-float(fields[ind]))
            
            onetableWriter.writerow(new_fields)
    

def make_zone_dbfs(cache_directory):
    xmlconfig = XMLConfiguration(filename="sanfrancisco.xml", 
                                 default_directory=r'C:\opus\project_configs',
                                 is_parent=False)
    runconfig = xmlconfig.get_run_configuration("sanfrancisco_baseline2009", merge_controllers=True)
    tm_config = runconfig['travel_model_configuration']
    print(tm_config['urbansim_to_tm_variable_mapping'])

    travel_model_years = []
    for key in tm_config.keys():
        if isinstance(key,int) and 'year_dir' in tm_config[key]:
            travel_model_years.append(key)
    travel_model_years.sort()
    
    zonedbfs_source_data = SourceData(
        cache_directory = cache_directory,
        run_description = "Run description is used for what?",
        years = travel_model_years,
        dataset_pool_configuration = DatasetPoolConfiguration(
            package_order=['sanfrancisco','urbansim','opus_core'],
        ),
    )

    attrs = []
    for key,val in tm_config['urbansim_to_tm_variable_mapping'].items():
        key = key.replace(".", "_")
        attrs.append("%s=%s" % (key,val))
        
    attrs.extend([\
      "pwac_bus=sanfrancisco.zone.bus_travel_time_weighted_access_by_population",
      "pwac_exp=sanfrancisco.zone.exp_travel_time_weighted_access_by_population",
      "pwac_lrt=sanfrancisco.zone.lrt_travel_time_weighted_access_by_population",
      "pwac_bart=sanfrancisco.zone.bart_travel_time_weighted_access_by_population",
      "pwac_hwy=sanfrancisco.zone.hwy_travel_time_weighted_access_by_population",
      "ewac_bus=sanfrancisco.zone.bus_travel_time_weighted_access_to_employment",
      "ewac_exp=sanfrancisco.zone.exp_travel_time_weighted_access_to_employment",
      "ewac_lrt=sanfrancisco.zone.lrt_travel_time_weighted_access_to_employment",
      "ewac_bart=sanfrancisco.zone.bart_travel_time_weighted_access_to_employment",
      "ewac_hwy=sanfrancisco.zone.hwy_travel_time_weighted_access_to_employment",
      "ttpw_bus=sanfrancisco.zone.bus_travel_time_to_751",
      "ttpw_exp=sanfrancisco.zone.exp_travel_time_to_751",
      "ttpw_lrt=sanfrancisco.zone.lrt_travel_time_to_751",
      "ttpw_bart=sanfrancisco.zone.bart_travel_time_to_751",
      "ttpw_hwy=sanfrancisco.zone.hwy_travel_time_to_751",      
      "d2powell=sanfrancisco.zone.dist_travel_time_to_751"
    ])

    zonedbf_indicators = [ DatasetTable(
        source_data = zonedbfs_source_data,
        dataset_name = 'zone',
        name = 'zone Indicators',
        output_type='dbf',
        attributes = attrs
        ) ]
                       
    IndicatorFactory().create_indicators(indicators = zonedbf_indicators,
                                         display_error_box = False,
                                         show_results = False)


if __name__ == '__main__':

    # takes 9.5 mins.  :p
    starttime = time()
    logger.log_note(strftime("%x %X", localtime(starttime)) + ": Starting")
    
    cache_directory=sys.argv[1]

    make_multiyear_workbook(cache_directory=cache_directory,
                             yearstart=2010,
                             yearend=2035)
    make_topsheet(cache_directory)
    make_zone_dbfs(cache_directory)

    endtime = time()
    logger.log_note(strftime("%x %X", localtime(endtime)) + " Completed. Total time: " + str((endtime-starttime)/60.0) + " mins")


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

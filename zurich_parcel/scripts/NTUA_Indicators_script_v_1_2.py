# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2013 National Technical University of Athens, Greece
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

'''
Created on Feb 20, 2013

NTUA SustainCity Project Team:
Constantinos Antoniou, Assistant Professor
Dimitrios Efthymiou, NTUA Phd Canditate
Giorgos Kalampokis, Junior Researcher
'''

import os
import urbansim
import sys

from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from opus_core.datasets.dataset_pool import DatasetPool
from numpy import *
from time import gmtime, strftime

opus_home = os.environ['OPUS_HOME']
opus_data_path = os.environ['OPUS_DATA_PATH']

print 'Indicators Policy Script Started on: %s' % strftime("%a, %d %b %Y %X", gmtime())

# Available policy levels
policy_levels = ['zone', 'parcel', 'gridcell']
# Available case studies
case_studies = ['brussels', 'zurich', 'paris']
# Available export computation levels
computation_levels = ['person', 'zone', 'parcel']

# Set user variables
# Attention!! Use backslash '/' for paths !!
# For Division in python (/) use decimal places on at least one of the inputs !! 

policy_level = policy_levels[1]

case_study = case_studies[1]

base_year_path = opus_data_path + '/zurich_kt_parcel/base_year_data/2000' #'/Network/Servers/kosrae.ethz.ch/Volumes/ivt-home/zoelligc/sustaincity/opushome/data/zurich_parcel/base_year_data/2000'

run_path = opus_data_path + '/runs/run_177.run_2013_02_13_09_36' #'/Network/Servers/kosrae.ethz.ch/Volumes/ivt-home/zoelligc/sustaincity/opushome/data/runs/run_177.run_2013_02_13_09_36'

storage_loc_save = run_path #'/Network/Servers/kosrae.ethz.ch/Volumes/ivt-home/zoelligc/sustaincity/opushome/data/runs/run_177.run_2013_02_13_09_36'

out_table_name_computations_prefix = 'swf_' + case_study + '_' + policy_level + '_computations_'

out_table_name_computations_person_prefix = 'swf_' + case_study + '_person_computations_'

out_table_name_swf_indicators = 'swf_' + case_study + '_' + policy_level + '_indicators'

interest_rate = '0.03'

vot = '1.5'

percentage_of_agents = '20.0'

start_year = 2006

end_year = 2010

year_interval = 1

export_computations_person = True
export_computations_zone = True
export_computations_parcel =True

# Print the variables
print 'Initializing variables set by user...'
print '-------------------------------------'
print 'Case Study: %s' % case_study
print 'Policy Level: %s' % policy_level
print 'Base Year Path: %s' % base_year_path
print 'Simulation Runs Path: %s' % run_path
print 'Output Path: %s' % storage_loc_save
print 'Interest Rate: %s' % interest_rate
print 'Value of Time: %s' % vot
print 'Percentage of Agents (%%): %s' % percentage_of_agents
print 'Year of Implementation: %s' % start_year
print 'Year of Evaluation: %s' % end_year
print 'Year Interval: %s' % year_interval
print '-------------------------------------'

# Detect Case Study

if case_study == 'brussels' and policy_level == 'zone':
    print 'brussels_zone Case Study'
elif case_study == 'zurich' and policy_level == 'parcel':
    print 'zurich_parcel Case Study'
elif case_study == 'paris' and policy_level == 'parcel':
    print 'paris_parcel Case Study'
else:
    print 'Unknown combination'
    sys.exit()

###############################################
# Preparation of years_list

# Create an empty list
years_list = list()
# Append 'base_year' to years list
years_list.append('base_year')
# Years to loop with interval set by user
years_run = range(start_year, end_year, year_interval)
print 'List of Years to loop through:'
# Append years to years list
for year in years_run:
    years_list.append(str(year))
# Retrieve years list
for year in years_list:
    print str(year)

###############################################

# Create storage object for in-memory computations

ram_storage = StorageFactory().get_storage('dict_storage')

# Create a table of swf indicators

ram_storage.write_table(table_name = out_table_name_swf_indicators,
                        table_data = {"swf_id":array([]),
                                      "year":array([]),
                                      "social_welfare":array([])})

# Create in-memory dataset of social welfare indicators

swf_indicators = Dataset(in_storage = ram_storage,
                    in_table_name = out_table_name_swf_indicators,
                    id_name = 'swf_id',
                    dataset_name = 'swf_indicator')

# Loop for storage location path including base year and year runs !

for year in years_list:
    print '-------------------------------------'
    print 'Data processing for year: %s' % year
    if year == 'base_year':
        storage_loc_load = base_year_path
    else:
        storage_loc_load = run_path + '/' + year
    out_table_name_person_computations = out_table_name_computations_person_prefix + year
    out_table_name_computations = out_table_name_computations_prefix + year
    print 'Data Input Path for year %s : %s' % (year, storage_loc_load)
    print 'Creating common datasets for year %s' % year
    # Create storage object for loading the data from
    storage_input = StorageFactory().get_storage('flt_storage', 
                                                 storage_location = storage_loc_load)
    # Create storage object for exporting the output data
    storage_output = StorageFactory().get_storage('tab_storage', 
                                                  storage_location = storage_loc_save)
    # Create household dataset
    households = Dataset(in_storage = storage_input,
                         in_table_name = 'households',
                         id_name = 'household_id',
                         dataset_name = 'household')
    # Create building dataset
    buildings = Dataset(in_storage = storage_input,
                        in_table_name = 'buildings',
                        id_name = 'building_id',
                        dataset_name = 'building')
    # Create building type dataset
    building_types = Dataset(in_storage = storage_input,
                    in_table_name = 'building_types',
                    id_name = 'building_type_id',
                    dataset_name = 'building_type')
    # Create persons dataset
    persons = Dataset(in_storage = storage_input,
                        in_table_name = 'persons',
                        id_name = 'person_id',
                        dataset_name = 'person')
    print 'Common datasets households, buildings, building_types, persons are created successfully!'
    # Create additional datasets according to the case study
    if case_study == 'brussels' and policy_level == 'zone':
        print 'Creating additional datasets for brussels_zone Case Study'
        # Create income_level dataset
        #income_level = Dataset(in_storage = storage_input,
        #             in_table_name = 'income_level',
        #             id_name = 'income_level_id',
        #             dataset_name = 'income_level')
        # Create zones dataset
        zones = Dataset(in_storage = storage_input,
                        in_table_name = 'zones',
                        id_name = 'zone_id',
                        dataset_name = 'zone')
        print 'Additional dataset zones is created successfully!'
    elif case_study == 'zurich' and policy_level == 'parcel':
        print 'Creating additional datasets for zurich_parcel Case Study'
        # Create parcel dataset
        parcels = Dataset(in_storage = storage_input,
                        in_table_name = 'parcels',
                        id_name = 'parcel_id',
                        dataset_name = 'parcel')
        print 'Additional dataset parcels is created successfully!'
    else:
        print 'Unknown combination'
    # Set variables about pool object according to the case study
    if case_study == 'brussels' and policy_level == 'zone':
        package_order = ['urbansim_zone', 'urbansim_parcel', 'urbansim', 'opus_core']
        datasets_dict = {'building': buildings,
                        'zone': zones,
                        'household': households,
                        #'income_level': income_level,
                        'person':persons}
    elif case_study == 'zurich' and policy_level == 'parcel':
        package_order = ['zurich_parcel','urbansim_parcel','urbansim','opus_core']
        datasets_dict = {'building': buildings,
                        'parcel': parcels,
                        'household': households,
                        'person':persons}
    else:
        package_order = []
        datasets_dict = {}
    # Create dataset pool object
    dataset_pool = DatasetPool(package_order = package_order,
                                storage = storage_input,
                                datasets_dict = datasets_dict)
    print '**********************'
    print 'Computing variables...'
    print '**********************'
    # Set expressions according to the case study
    if case_study == 'brussels' and policy_level == 'zone':
        # expressions for brussels zone case study in interactive opus mode
        zones.compute_variables("income_per_zone = \
        zone.aggregate(12 * household.income, \
        intermediates=[building])", dataset_pool = dataset_pool)
        zones.compute_variables("housing_cost_per_zone = \
        zone.aggregate(where(household.disaggregate(building_type.is_residential==1),\
        household.disaggregate(building.average_value_per_unit *" + interest_rate + "), 0)\
        )", dataset_pool = dataset_pool)    
        persons.compute_variables("travel_cost_per_person = \
        where(person.home2work_travel_time_min>=0,\
        (" + vot + "*((person.home2work_travel_time_min+\
        person.work2home_travel_time_min)/60.0)*250*\
        (100/" + percentage_of_agents + ")),0)", dataset_pool = dataset_pool)
        zones.compute_variables("travel_cost_per_zone = \
        zone.aggregate(person.travel_cost_per_person,\
        intermediates=[household, building])", dataset_pool = dataset_pool)
        zones.compute_variables("utility_of_residents_zone = \
        zone.income_per_zone-zone.housing_cost_per_zone-zone.travel_cost_per_zone", dataset_pool = dataset_pool)
    elif case_study == 'zurich' and policy_level == 'parcel':
        # expressions for zurich parcel case study in interactive opus mode
        parcels.compute_variables("income_per_parcel = \
        parcel.aggregate(12 * household.income, \
        intermediates=[building])", dataset_pool = dataset_pool)
        parcels.compute_variables("housing_cost_per_parcel = \
        parcel.aggregate(where(building.disaggregate(building_type.is_residential==1),\
        building.improvement_value*building.residential_units*" + interest_rate + ", 0))", dataset_pool = dataset_pool)    
        persons.compute_variables("travel_cost_per_person = \
        where(person.home2work_travel_time_min>=0,\
        (" + vot + "*((person.home2work_travel_time_min+\
        person.work2home_travel_time_min)/60.0)*250*\
        (100/" + percentage_of_agents + ")),0)", dataset_pool = dataset_pool)
        parcels.compute_variables("travel_cost_per_parcel = \
        parcel.aggregate(person.travel_cost_per_person,\
        intermediates=[household, building])", dataset_pool = dataset_pool)
        parcels.compute_variables("utility_of_residents_parcel = \
        parcel.income_per_parcel-parcel.housing_cost_per_parcel-parcel.travel_cost_per_parcel", dataset_pool = dataset_pool)
    # export output to tab file
    print '*************************'
    print 'Exporting to tab files...'
    print '*************************'
    # export computations to tab file [person level]
    if export_computations_person == True:
        print '[Person Level] Exporting computations to: %s' % out_table_name_person_computations
        persons.write_dataset(attributes = ['person_id', 'home2work_travel_time_min', 'work2home_travel_time_min', 'travel_cost_per_person'], 
                            out_storage = storage_output, 
                            out_table_name = out_table_name_person_computations)
    # Exports according to case study
    if case_study == 'brussels' and policy_level == 'zone':
        # export computations to tab file [zone level]
        if export_computations_zone == True:
            print '[Zone Level] Exporting computations to: %s' % out_table_name_computations
            zones.write_dataset(attributes = ['income_per_zone', 'housing_cost_per_zone', 'travel_cost_per_zone', 'utility_of_residents_zone'], 
                            out_storage = storage_output, 
                            out_table_name = out_table_name_computations)
        # Summarize utility_of_residents_zone attributes
        swf_per_year = zones.attribute_sum('utility_of_residents_zone')
    elif case_study == 'zurich' and policy_level == 'parcel':
        # export computations to tab file [parcel level]
        if export_computations_parcel == True:
            print '[Parcel Level] Exporting computations to: %s' % out_table_name_computations
            parcels.write_dataset(attributes = ['income_per_parcel', 'housing_cost_per_parcel', 'travel_cost_per_parcel', 'utility_of_residents_parcel'], 
                                out_storage = storage_output, 
                                out_table_name = out_table_name_computations)
        # Summarize utility_of_residents_zone attributes
        swf_per_year = parcels.attribute_sum('utility_of_residents_parcel')
    print 'Social Welfare for year %s: %s' % (year, swf_per_year)
    # Place swf idicator value for the running year into a dict storage
    # Add swf as primary attribute for the running year
    swf_indicators.add_elements(data = {"swf_id":array([1]),
                                        "year":array([year]),
                                        "social_welfare":array([swf_per_year])}, require_all_attributes = True, change_ids_if_not_unique = True)

# Summarize social_welfare attributes for all years
swf_summary = swf_indicators.attribute_sum('social_welfare')
print '-------------------------------------'
print 'Total Social Welfare: %s' % swf_summary
# Add swf_summary as primary attribute to table swf_indicators
swf_indicators.add_elements(data = {"swf_id":array([1]),
                                    "year":array(['swf_summary']),
                                    "social_welfare":array([swf_summary])}, require_all_attributes = True, change_ids_if_not_unique = True)
# export social welfare indicators to tab file 
print 'Exporting Table of Social Welfare Indicators to: %s' % out_table_name_swf_indicators
swf_indicators.write_dataset(attributes = ['swf_id', 'year', 'social_welfare'], 
                    out_storage = storage_output, 
                    out_table_name = out_table_name_swf_indicators)
print '-------------------------------------'
print 'Indicators Policy Script Completed on %s !' % strftime("%a, %d %b %Y %X", gmtime())

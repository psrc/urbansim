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
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.services.run_server.run_manager import RunManager

class RestartRunOptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="Navigate in the console to your OPUS_HOME folder. Type: \
                                                    python %prog [options] base_year_bath run_path",
               description="Run the indicator module on a given base year and a given run.")
#        self.parser.add_option("-p", "--project-name", dest="project_name", 
#                                default='',help="The name project name")
        
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

working_dir = os.environ['PWD']
opus_home = os.environ['OPUS_HOME']
opus_data_path = opus_home + 'data/' # os.environ['OPUS_DATA_PATH']

option_group = RestartRunOptionGroup()
parser = option_group.parser
options, args = option_group.parse()
if len(args) < 2:
    parser.print_help()
base_year_path = working_dir + '/' + args[0] #'zurich_kt_parcel/base_year_data_indicator_module_test/2000'

run_path = working_dir + '/' + args[1] #'zurich_kt_parcel/runs/run_indicator_module_test'

storage_loc_save = run_path

out_table_name_computations_prefix = 'swf_' + case_study + '_' + policy_level + '_computations_'

out_table_name_computations_person_prefix = 'swf_' + case_study + '_person_computations_'

out_table_name_swf_indicators = 'swf_' + case_study + '_' + policy_level + '_indicators'

interest_rate = '0.03'

discounting_rate = 0.01

vot = '.4188' # [Currency / min], SN 641 822, for commuting: 31.45 [CHF / h]-> 0.4188 [EUR / min]

percentage_of_agents = '100.0'

transport_cost_per_km = '2.00'

energy_consumption_rate = '1.50'

cost_of_investment = 112000000 # Bruns, F., P. Kern and C. Abegg (2008) Wie weiter mit dem Verkehr, Zürcher Kantonalbank, Zürich. Seite 24.

annual_operation_cost = 55 # Bruns, F., P. Kern and C. Abegg (2008) Wie weiter mit dem Verkehr, Zürcher Kantonalbank, Zürich. Seite 24.

revenue_per_year = 100000

base_year = 2000

start_year = 2015

end_year = 2017

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
print 'Transport Cost per Km (Euro/km): %s' % transport_cost_per_km
print 'Energy Consumption Rate: %s' % energy_consumption_rate
print 'Cost of investment: %s' % cost_of_investment
print 'Revenue per year: %s' % revenue_per_year
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
    print 'Started on: %s' % strftime("%a, %d %b %Y %X", gmtime())
    if year == 'base_year':
        storage_loc_load = base_year_path
    else:
        storage_loc_load = run_path + '/' + year
    out_table_name_person_computations = out_table_name_computations_person_prefix + year
    out_table_name_computations = out_table_name_computations_prefix + year
    print 'Data Input Path for year %s : %s' % (year, storage_loc_load)
    print 'Creating common datasets for year %s' % year
    print 'Started on: %s' % strftime("%a, %d %b %Y %X", gmtime())
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
        fazes = Dataset(in_storage = storage_input,
                        in_table_name = 'fazes',
                        id_name = 'faz_id',
                        dataset_name = 'faz')
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
                        'faz':fazes,
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
    
    
##########        BRUSSELS        ##########

    if case_study == 'brussels' and policy_level == 'zone':
        
        # expressions for brussels zone case study in interactive opus mode
        
        ###        VARIABLES    ###

        zones.compute_variables("income_per_zone = \
        zone.aggregate(12 * household.income, \
        intermediates=[building])", dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        zones.compute_variables("tax_ipp_per_zone = \
        zone.disaggregate(faz.tax_ipp)", dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        zones.compute_variables("local_taxes_on_property_per_zone = \
        0.01 * zone.tax_ipp_per_zone * \
        zone.aggregate(where(building.disaggregate(building_type.is_residential==1),\
        building.average_value_per_unit * building.residential_units, 0))" \
        , dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        zones.compute_variables("housing_cost_per_zone = \
        zone.aggregate(where(household.disaggregate(building_type.is_residential==1),\
        household.disaggregate(building.average_value_per_unit *" + interest_rate + "), 0)\
        )", dataset_pool = dataset_pool)   
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime()) 
        
        persons.compute_variables("travel_cost_per_person = \
        where(person.home2work_travel_time_min>=0,\
        (" + vot + "*((person.home2work_travel_time_min+\
        person.work2home_travel_time_min)/60.0)*250*\
        (100/" + percentage_of_agents + ")),0)", dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        print 'Persons Table Attributes: \n %s' \
#       % persons.get_multiple_attributes(["person_id", "travel_cost_per_person"])
        
        zones.compute_variables("travel_cost_per_zone = \
        zone.aggregate(person.travel_cost_per_person,\
        intermediates=[household, building])", dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        print 'Zone Table Attributes: \n %s' \
#       % zones.get_multiple_attributes(["zone_id", "travel_cost_per_zone"])

        persons.compute_variables("vehkm_per_person = \
        (person.home2work_distance_meter + person.work2home_distance_meter)/1000.0" \
        , dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        persons.compute_variables("transport_cost_per_person = " \
        + transport_cost_per_km + " * person.vehkm_per_person", dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        #zones.compute_variables = ("transport_per_person_per_zone = \
        #zone.aggregate(person.transport_cost_per_person, \
        #intermediates=[household, building])")
        #print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        zones.compute_variables("travel_benefit_car = zone.car_accessibility")
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
       # zones.compute_variables = ("travel_benefit_pt = zone.pt_accessibility")
       # print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        buildings.compute_variables("building_energy_consumption = \
        (building.residential_units * building.sqft_per_unit) * " + energy_consumption_rate, \
        dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        print 'Building Table Attributes: \n %s' \
        % buildings.get_multiple_attributes(["building_id", "building_energy_consumption"])
        
        zones.compute_variables("building_energy_consumption_per_zone = \
        zone.aggregate(building.building_energy_consumption)" \
        , dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        #zones.compute_variables("utility_of_the_rest_of_the_world = \
        #transport_per_person_per_zone + 100" \
        #, dataset_pool = dataset_pool)
        #print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())           
                 
        
        ###        UTILITIES    ###
                 
        zones.compute_variables("utility_of_residents_zone = \
        zone.income_per_zone-zone.housing_cost_per_zone-zone.local_taxes_on_property_per_zone-zone.travel_cost_per_zone" \
        , dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        zones.compute_variables("utility_of_the_rest_of_the_world = \
        building_energy_consumption_per_zone" \
        , dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        zones.compute_variables("utility_of_commuters = \
        zone.utility_of_residents_zone", dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())


##########        ZURICH        ##########
        
    elif case_study == 'zurich' and policy_level == 'parcel':
        # expressions for zurich parcel case study in interactive opus mode
    
        ###        VARIABLES    ###

        parcels.compute_variables("income_per_parcel = \
        parcel.aggregate(12 * household.income, \
        intermediates=[living_unit, building])", dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        parcels.compute_variables("housing_cost_per_parcel = \
        parcel.aggregate(where(building.disaggregate(building_type.is_residential==1),\
        building.aggregate(12 * living_unit.rent_price, function=sum), 0))", dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        persons.compute_variables("travel_cost_per_person = \
        where(person.home2work_travel_time_min>=0,\
        (" + vot + "*((person.home2work_travel_time_min+\
        person.work2home_travel_time_min)/60.0)*250*\
        (100/" + percentage_of_agents + ")),0)", dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        parcels.compute_variables("travel_cost_per_parcel = \
        parcel.aggregate(person.travel_cost_per_person,\
        intermediates=[household, building])", dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        parcels.compute_variables("travel_benefit_car = \
        parcel.car_accessibility")
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        #parcels.compute_variables = ("travel_benefit_pt = \
        #parcel.pt_accessibility")
        #print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        buildings.compute_variables("building_energy_consumption = \
        (building.aggregate(living_unit.area, function=sum)) * " + energy_consumption_rate, \
        dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        print 'Building Table Attributes: \n %s' \
        % buildings.get_multiple_attributes(["building_id", "building_energy_consumption"])
        
        parcels.compute_variables("building_energy_consumption_per_parcel = \
        parcel.aggregate(building.building_energy_consumption)" \
        , dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        

        ###        UTILITIES    ###
        
        parcels.compute_variables("utility_of_the_rest_of_the_world = \
        building_energy_consumption_per_parcel" \
        , dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())        
        
        parcels.compute_variables("utility_of_residents_parcel = \
        parcel.income_per_parcel-parcel.housing_cost_per_parcel-parcel.travel_cost_per_parcel" \
        , dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
        parcels.compute_variables("utility_of_commuters = \
        parcel.utility_of_residents_parcel", dataset_pool = dataset_pool)
        print 'Computed on: %s' % strftime("%a, %d %b %Y %X", gmtime())
        
    # export output to tab file
    print '*************************'
    print 'Exporting to tab files...'
    print '*************************'
    # export computations to tab file [person level]
    if export_computations_person == True:
        print '[Person Level] Exporting computations to: %s' % out_table_name_person_computations
        print 'Time Start: %s' % strftime("%a, %d %b %Y %X", gmtime())
#        persons.write_dataset(attributes = ['person_id', 'home2work_travel_time_min', 'work2home_travel_time_min', 'travel_cost_per_person'], 
#                            out_storage = storage_output, 
#                            out_table_name = out_table_name_person_computations)
        print 'Time End: %s' % strftime("%a, %d %b %Y %X", gmtime())
    # Exports according to case study
    if case_study == 'brussels' and policy_level == 'zone':
        # export computations to tab file [zone level]
        if export_computations_zone == True:
            print '[Zone Level] Exporting computations to: %s' % out_table_name_computations
            print 'Time Start: %s' % strftime("%a, %d %b %Y %X", gmtime())
            zones.write_dataset(attributes = ['income_per_zone', 
                                              'housing_cost_per_zone', 
                                              'travel_cost_per_zone',
                                              'travel_benefit_car', #'travel_benefit_pt',
                                              'utility_of_residents_zone',
                                              'utility_of_commuters',
                                              'utility_of_the_rest_of_the_world'], 
                            out_storage = storage_output, 
                            out_table_name = out_table_name_computations)
            print 'Time End: %s' % strftime("%a, %d %b %Y %X", gmtime())
        # Compute social welfare per year by summarizing attributes
        swf_per_year = zones.attribute_sum('utility_of_residents_zone') \
        + zones.attribute_sum('utility_of_commuters') \
        + zones.attribute_sum('utility_of_the_rest_of_the_world')
    elif case_study == 'zurich' and policy_level == 'parcel':
        # export computations to tab file [parcel level]
        if export_computations_parcel == True:
            print '[Parcel Level] Exporting computations to: %s' % out_table_name_computations
            print 'Time Start: %s' % strftime("%a, %d %b %Y %X", gmtime())
            parcels.write_dataset(attributes = ['income_per_parcel', 
                                                'housing_cost_per_parcel', 
                                                'travel_cost_per_parcel', 
                                                'travel_benefit_car', #'travel_benefit_pt',
                                                'utility_of_residents_parcel',
                                                'utility_of_commuters',
                                                'utility_of_the_rest_of_the_world'], 
                                out_storage = storage_output, 
                                out_table_name = out_table_name_computations)
            print 'Time End: %s' % strftime("%a, %d %b %Y %X", gmtime())
        # Summarize utility_of_residents_zone attributes
        swf_per_year = parcels.attribute_sum('utility_of_residents_parcel') \
        + parcels.attribute_sum('utility_of_commuters') \
        + parcels.attribute_sum('utility_of_the_rest_of_the_world') \
        + revenue_per_year
        
    if type(year) is str:
          swf_per_year_disc = swf_per_year
    else:
        swf_per_year_disc = swf_per_year/((1 + discounting_rate)**(base_year - int(year)))
        
    print 'Social Welfare for year %s: %s' % (year, swf_per_year)
    # Place swf idicator value for the running year into a dict storage
    # Add swf as primary attribute for the running year
    swf_indicators.add_elements(data = {"swf_id":array([1]),
                                        "year":array([year]),
                                        "social_welfare":array([swf_per_year_disc])}, require_all_attributes = True, change_ids_if_not_unique = True)

# Summarize social_welfare attributes for all years
swf_summary = swf_indicators.attribute_sum('social_welfare') - cost_of_investment
print '-------------------------------------'
print 'Total Social Welfare: %s' % swf_summary
# Add swf_summary as primary attribute to table swf_indicators
swf_indicators.add_elements(data = {"swf_id":array([1]),
                                    "year":array(['swf_summary']),
                                    "social_welfare":array([swf_summary])}, require_all_attributes = True, change_ids_if_not_unique = True)
# export social welfare indicators to tab file 
print 'Exporting Table of Social Welfare Indicators to: %s' % out_table_name_swf_indicators
print 'Time Start: %s' % strftime("%a, %d %b %Y %X", gmtime())
swf_indicators.write_dataset(attributes = ['swf_id', 'year', 'social_welfare'], 
                    out_storage = storage_output, 
                    out_table_name = out_table_name_swf_indicators)
print 'Time End: %s' % strftime("%a, %d %b %Y %X", gmtime())
print '-------------------------------------'
print 'Indicators Policy Script Completed on %s !' % strftime("%a, %d %b %Y %X", gmtime())
# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from elixir import *

# Select the database connection by (un)commenting and adapting the following options
######################
metadata.bind = "sqlite:////Users/thomas/sqlite/sample_parcel.db"
#metadata.bind = "postgres://account:password@localhost/sample_parcel"
#metadata.bind = "mysql://account:password@localhost/sample_parcel"
######################

metadata.bind.echo = True

class AnnualEmploymentControlTotal(Entity):
    using_options(tablename='annual_employment_control_totals')
    year = Field(Integer)
    sector = ManyToOne('EmploymentSector', colname='sector_id')
    home_based_status = Field(Integer)
    number_of_jobs = Field(Integer)

class AnnualHouseholdControlTotal(Entity):
    using_options(tablename='annual_household_control_totals')
    year = Field(Integer)
    # optional fields commented out
    #age_of_head = Field(Integer)
    persons = Field(Integer)
    #income = Field(Integer)
    total_number_of_households = Field(Integer)

class AnnualRelocationRatesForHousehold(Entity):
    using_options(tablename='annual_relocation_rates_for_households')
    age_of_head_min = Field(Integer)
    age_of_head_max = Field(Integer)
    income_min = Field(Integer)
    income_max = Field(Integer)
    probability_of_relocating = Field(Float)

class AnnualJobRelocationRates(Entity):
    using_options(tablename='annual_job_relocation_rates')
    sector = ManyToOne('EmploymentSector', colname='sector_id')
    job_relocation_probability = Field(Float)

class Building(Entity):
    using_options(tablename='buildings')
    building_id = Field(Integer, primary_key=True)
    building_quality_id = Field(Integer)
    building_type = ManyToOne('BuildingType', colname='building_type_id')
    improvement_value = Field(Integer)
    land_area = Field(Integer)
    non_residential_sqft = Field(Integer)
    residential_units = Field(Integer)
    sqft_per_unit = Field(Integer)
    year_built = Field(Integer)
    stories = Field(Integer)
    tax_exempt = Field(Integer)
    parcel = ManyToOne('Parcel', colname='parcel_id')

class BuildingSqftPerJob(Entity):
    using_options(tablename='building_sqft_per_job')
    building_type_id = Field(Integer, primary_key=True)
    zone_id = Field(Integer, primary_key=True)
    building_sqft_per_job = Field(Integer)
    
class BuildingType(Entity):
    using_options(tablename='building_types')
    building_type_id = Field(Integer, primary_key=True)
    is_residential = Field(Integer)
    building_type_name = Field(String(20))
    building_type_description = Field(String(20))
    unit_name = Field(String(20))
    generic_building_type_id = Field(Integer)
    generic_building_type_name = Field(String(20))

class City(Entity):
    using_options(tablename='cities')
    city_id = Field(Integer, primary_key=True)
    city_name = Field(String(25))

class County(Entity):
    using_options(tablename='counties')
    county_id = Field(Integer, primary_key=True)
    county_name = Field(String(20))
    county_fips = Field(String(10))

class DemolitionCostPerSqft(Entity):
    using_options(tablename='demolition_cost_per_sqft')
    building_type = ManyToOne('BuildingType', colname='building_type_id')
    #building_type_name = Field(String(20))
    demolition_cost_per_sqft = Field(Integer)

class DevelopmentConstraint(Entity):
    using_options(tablename='development_constraints')
    constraint_id = Field(Integer, primary_key=True)
    generic_land_use_type = ManyToOne('GenericLandUseType', colname='generic_land_use_type_id')
    plan_type = ManyToOne('PlanType', colname='plan_type_id')
    minimum = Field(Integer)
    maximum = Field(Integer)

class DevelopmentEventHistory(Entity):
    using_options(tablename='development_event_history')
    parcel = ManyToOne('Parcel', colname='parcel_id')
    building_type_id = Field(Integer, primary_key=True)
    scheduled_year = Field(Integer)
    residential_units = Field(Integer)
    non_residential_sqft = Field(Integer)
    change_type = Field(String(1))

class DevelopmentProjectProposal(Entity):
    using_options(tablename='development_project_proposals')
    proposal_id = Field(Integer, primary_key=True)
    parcel = ManyToOne('Parcel', colname='parcel_id')
    template = ManyToOne('DevelopmentTemplate', colname='template_id')
    status_id = Field(Integer) 
    #1 (in active development), 2 (proposed for development), 3 (planned and will be developed), 4 (tentative), 5 (not available), 6 (refused)
    start_year = Field(Integer)
    is_redevelopment = Field(Integer) # 1 requires redevelopment, 0 otherwise

class DevelopmentTemplate(Entity):
    using_options(tablename='development_templates')
    template_id = Field(Integer, primary_key=True)
    percent_land_overhead = Field(Integer)
    land_sqft_min = Field(Integer)
    land_sqft_max = Field(Integer)
    density = Field(Float)
    density_type = Field(String(20))
    land_use_type_id = Field(Integer)
    development_type = Field(String(20))
    is_active = Field(Integer)

class DevelopmentTemplateComponents(Entity):
    using_options(tablename='development_template_components')
    component_id = Field(Integer, primary_key=True)
    template_id = Field(Integer)
    building_type = ManyToOne('BuildingType', colname='building_type_id')
    percent_building_sqft = Field(Integer)
    construction_cost_per_unit = Field(Integer)
    building_sqft_per_unit = Field(Integer)

class EmploymentAdHocSectorGroup(Entity):
    using_options(tablename='employment_adhoc_sector_groups')
    group_id = Field(Integer, primary_key=True)
    name = Field(String(20))

class EmploymentAdHocSectorGroupDefinition(Entity):
    using_options(tablename='employment_adhoc_sector_group_definitions')
    sector_id = Field(Integer, primary_key=True)
    group = ManyToOne('EmploymentAdHocSectorGroup', colname='group_id')

class EmploymentSector(Entity):
    using_options(tablename='employment_sectors')
    sector_id = Field(Integer, primary_key=True)
    name = Field(String(20))

class Faz(Entity):
    using_options(tablename='fazes')
    faz_id = Field(Integer, primary_key=True)
    large_area = ManyToOne('LargeArea', colname='large_area_id')

class GenericLandUseType(Entity):
    using_options(tablename='generic_land_use_types')
    generic_land_use_type_id = Field(Integer, primary_key=True)
    generic_description = Field(String(50))

class HomeBasedStatus(Entity):
    using_options(tablename='home_based_status')
    home_based_status = Field(Integer, primary_key=True)
    name = Field(String(20))

class Household(Entity):
    using_options(tablename='households')
    household_id = Field(Integer, primary_key=True)
    building = ManyToOne('Building', colname='building_id')
    persons = Field(Integer)
    income = Field(Integer)
    age_of_head = Field(Integer)
    race = ManyToOne('RaceName', colname='race_id')
    workers = Field(Integer)
    children = Field(Integer)
    cars = Field(Integer)

class HouseholdCharacteristicsForHT(Entity):
    using_options(tablename='household_characteristics_for_ht')
    characteristic = Field(String(20))
    min = Field(Integer)
    max = Field(Integer)

class HouseholdsForEstimation(Entity):
    using_options(tablename='households_for_estimation')
    household_id = Field(Integer, primary_key=True)
    building = ManyToOne('Building', colname='building_id')
    persons = Field(Integer)
    income = Field(Integer)
    age_of_head = Field(Integer)
    race = ManyToOne('RaceName', colname='race_id')
    workers = Field(Integer)
    children = Field(Integer)
    cars = Field(Integer)

class Job(Entity):
    using_options(tablename='jobs')
    job_id = Field(Integer, primary_key = True)
    building = ManyToOne('Building', colname='building_id')
    home_based_status = Field(Integer)
    sector = ManyToOne('EmploymentSector', colname='sector_id')

class JobsForEstimation(Entity):
    using_options(tablename='jobs_for_estimatiion')
    job_id = Field(Integer, primary_key = True)
    building = ManyToOne('Building', colname='building_id')
    home_based_status = Field(Integer)
    sector = ManyToOne('EmploymentSector', colname='sector_id')

class LandUseType(Entity):
    using_options(tablename='land_use_types')
    land_use_type_id = Field(Integer, primary_key = True)
    description = Field(String(40))
    land_use_name = Field(String(25))
    unit_name = Field(String(15))
    generic_land_use_type = ManyToOne('GenericLandUseType', colname='generic_land_use_type_id')

class LargeArea(Entity):
    using_options(tablename='large_areas')
    large_area_id = Field(Integer, primary_key=True)
    large_area_name = Field(String(50))
    county = ManyToOne('County', colname='county_id')
    
class Parcel(Entity):
    using_options(tablename='parcels')
    parcel_id = Field(Integer, primary_key=True)
    parcel_id_local = Field(String(20)) #Store assessors key to merge other data
    land_value = Field(Integer)
    parcel_sqft = Field(Integer)
    plan_type = ManyToOne('PlanType', colname='plan_type_id')
    centroid_x = Field(Integer) #optional
    centroid_y = Field(Integer) #optional
    tax_exempt_flag = Field(Integer)
    city = ManyToOne('City', colname='city_id')
    county = ManyToOne('County', colname='county_id')
    zone = ManyToOne('Zone', colname='zone_id')
    census_block_id = Field(String(20))

class PlanType(Entity): #Needed for zones?
    using_options(tablename='plan_types')
    plan_type_id = Field(Integer, primary_key=True)
    name = Field(String(50))

class RaceName(Entity):
    using_options(tablename='race_names')
    race_id = Field(Integer, primary_key=True)
    minority = Field(Integer)
    name = Field(String(20))

class Refinement(Entity):
    refinement_id = Field(Integer, primary_key=True)
    using_options(tablename='refinements')
    transaction_id = Field(Integer, primary_key=True)
    agent_dataset = Field(String(25))
    agent_expression = Field(String(200))
    amount = Field(Integer)
    location_capacity_attribute= (50)
    location_expression = Field(String(200))
    transaction_id = Field(Integer)
    year = Field(Integer)

class ScheduledDevelopmentEvents(Entity):
    using_options(tablename='scheduled_development_events')
    id = Field(Integer, primary_key=True)
    year = Field(Integer)
    action = Field(String(20))
    attribute = Field(String(25))  #optional, required if action is 'set_value', 'add_value', 'subtract_value', or multiply_value
    amount = Field(Integer)
    #fields to identify buildings(location and building type) for events
    building = ManyToOne('Building', colname='building_id')
    ## alternatively, use primary or computed attributes of buildings
    #zone = ManyToOne('Zone', colname='zone_id')
    #building_type = ManyToOne('Building_type', colname='building_type_id')

class ScheduledEmploymentEvents(Entity):
    using_options(tablename='scheduled_employment_events')
    id = Field(Integer, primary_key=True)
    year = Field(Integer)
    action = Field(String)
    attribute = Field(String)   #optional, required if action is 'set_value', 'add_value', 'subtract_value', or multiply_value
    amount = Field(Integer)
    #fields to identify jobs for events 
    sector = ManyToOne('EmploymentSector', colname='sector_id')
    ##alternatively, use primary or computed attributes of jobs
    # building = ManyToOne('Building', colname='building_id')

class TargetVacancy(Entity):
    using_options(tablename='target_vacancies')
    year = Field(Integer, primary_key=True)
    building_type = ManyToOne('BuildingType', colname='building_type_id')
    target_vacancy_rate = Field(Float)

class TravelData(Entity):
    using_options(tablename='travel_data')
    from_zone_id = Field(Integer, primary_key=True)
    to_zone_id = Field(Integer, primary_key=True)
    am_single_vehicle_to_work_travel_time = Field(Integer)
    #Enter any additional columns needed from travel model skims

class VelocityFunction(Entity):
    using_options(tablename='velocity_functions')
    velocity_function_id = Field(Integer, primary_key=True)
    annual_construction_schedule = Field(String) 
    #A numbered list in brackets of the form, '[p1, p2,...,pn]', indicating with each entry the percentage complete of the 
    #project each year from its start. The last entry must be '100'.
    building_type = ManyToOne('BuildingType', colname='building_type_id')
    minimum_units = Field(Integer)
    maximum_units = Field(Integer)

class Zone(Entity):
    using_options(tablename='zones')
    zone_id = Field(Integer, primary_key=True)
    city = ManyToOne('City', colname='city_id')
    county = ManyToOne('County', colname='county_id')
    faz = ManyToOne('Faz', colname='faz_id')


setup_all()
create_all()

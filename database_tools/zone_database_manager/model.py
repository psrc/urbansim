import camelot.types
from camelot.model import metadata, Entity, Field, ManyToOne, OneToMany, Integer, String, Float, using_options
from camelot.view.controls import delegates
from camelot.view.elixir_admin import EntityAdmin
from camelot.view.forms import *

__metadata__ = metadata

class AnnualEmploymentControlTotal(Entity):
    using_options(tablename='annual_employment_control_totals')
    year = Field(Integer)
    sector = ManyToOne('EmploymentSector', colname='sector_id')
    home_based_status = Field(Integer)
    number_of_jobs = Field(Integer)
    
    class Admin(EntityAdmin):
        verbose_name='Employment Control Total'
        list_display=['year', 'sector_id', 'home_based_status', 'number_of_jobs']
        #list_filter = ['sector_id', 'year']
        field_attributes = dict(year=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1900, maximum=2050),
                                sector_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                home_based_status=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1),
                                number_of_jobs=dict(delegate=delegates.IntegerDelegate, calculator=False)
                                )

class AnnualHouseholdControlTotal(Entity):
    using_options(tablename='annual_household_control_totals')
    id = Field(Integer, primary_key=True)
    year = Field(Integer)
    total_number_of_households = Field(Integer)
    
    class Admin(EntityAdmin):
        verbose_name='Household Control Total'
        list_display=['year', 'total_number_of_households']
        field_attributes = dict(year=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1900, maximum=2050),
                                total_number_of_households=dict(delegate=delegates.IntegerDelegate, calculator=False)
                                )

class AnnualRelocationRatesForHousehold(Entity):
    using_options(tablename='annual_relocation_rates_for_households')
    age_of_head_min = Field(Integer)
    age_of_head_max = Field(Integer)
    income_min = Field(Integer)
    income_max = Field(Integer)
    probability_of_relocating = Field(Float)

    class Admin(EntityAdmin):
        verbose_name='Annual Relocation Rates for Household'
        list_display=['age_of_head_min', 'age_of_head_max', 'income_min', 'income_max', 'probability_of_relocating']
        field_attributes = dict(age_of_head_min=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=100),
                                age_of_head_max=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=100),
                                income_min=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                income_max=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                probability_of_relocating=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1)
                                )

class Building(Entity):
    using_options(tablename='buildings')
    id = Field(Integer, primary_key=True, colname='building_id')
    building_type = ManyToOne('BuildingType', colname='building_type_id')
    land_area = Field(Integer)
    non_residential_sqft = Field(Integer)
    non_residential_sqft_capacity = Field(Integer)
    residential_units = Field(Integer)
    residential_units_capacity = Field(Integer)
    sqft_per_unit = Field(Integer)
    year_built = Field(Integer)
    average_value_per_unit = Field(Integer)
    zone = ManyToOne('Zone', colname='zone_id')

    class Admin(EntityAdmin):
        verbose_name='Building'
        list_display=[
            'building_id',
            'building_type_id',
            'land_area',
            'non_residential_sqft',
            'non_residential_sqft_capacity',
            'residential_units',
            'residential_units_capacity',
            'sqft_per_unit',
            'year_built',
            'average_value_per_unit',
            'zone'
            ]
        field_attributes = dict(building_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                land_area=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                non_residential_sqft=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0),
                                non_residential_sqft_capacity=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0),
                                residential_units=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0),
                                residential_units_capacity=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0),
                                sqft_per_unit=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0),
                                year_built=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1800, maximum=2050),
                                average_value_per_unit=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0),
                                zone_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
            
class BuildingSqftPerJob(Entity):
    using_options(tablename='building_sqft_per_job')
    id = Field(Integer, primary_key=True)
    building_sqft_per_job = Field(Integer)
    building_type_id = Field(Integer)
    zone_id = Field(Integer)
    
    class Admin(EntityAdmin):
        verbose_name='Building Sqft Per Job'
        list_display=['building_sqft_per_job', 'building_type_id', 'zone_id']
        field_attributes = dict(building_sqft_per_job=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0),
                                building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                zone_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )

class BuildingType(Entity):
    using_options(tablename='building_types')
    id = Field(Integer, primary_key=True, colname='building_type_id')
    is_residential = Field(Integer)
    building_type_name = Field(String(20))

    class Admin(EntityAdmin):
        verbose_name='Building Type'
        list_display=[
            'building_type_id',
            'is_residential',
            'building_type_name',
            ]
        field_attributes = dict(building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                is_residential=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1)
                                )
 
class County(Entity):
    using_options(tablename='counties')
    id = Field(Integer, primary_key=True, colname='county_id')
    county_name = Field(String(20))
    county_fips = Field(String(10))
    
    class Admin(EntityAdmin):
        verbose_name='Countie'
        list_display=['county_id', 'county_name', 'county_fips']
        field_attributes = dict(county_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1))

class DevelopmentConstraint(Entity):
    using_options(tablename='development_constraints')
    id = Field(Integer, primary_key=True, colname='development_constraint_id')
    zone_id = Field(Integer)
    building_type_id = Field(Integer)
    residential_units_capacity = Field(Integer)
    non_residential_sqft_capacity = Field(Integer)
    
    class Admin(EntityAdmin):
        verbose_name='Development Constraint'
        list_display=['development_constraint_id', 'zone_id', 'building_type_id', 'residential_units_capacity', 'non_residential_sqft_capacity']
        field_attributes = dict(development_constraint_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                zone_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                residential_units_capacity=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0),
                                non_residential_sqft_capacity=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0)
                                )
                                
class DevelopmentEventHistory(Entity):
    using_options(tablename='development_event_history')
    id = Field(Integer, primary_key=True)
    zone = ManyToOne('Zone', colname='zone_id')
    building_type_id = Field(Integer)
    scheduled_year = Field(Integer)
    residential_units = Field(Integer)
    non_residential_sqft = Field(Integer)
    change_type = Field(String(1))

    class Admin(EntityAdmin):
        verbose_name='Development Event Historie'
        list_display=['zone_id', 'building_type_id', 'scheduled_year', 'residential_units', 'non_residential_sqft', 'change_type']
        field_attributes = dict(zone_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                scheduled_year=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1950, maximum=2050),
                                residential_units=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0),
                                non_residential_sqft=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0)
                                )
                                
class EmploymentAdHocSectorGroupDefinition(Entity):
    using_options(tablename='employment_adhoc_sector_group_definitions')
    id = Field(Integer, primary_key=True)
    sector_id = Field(Integer)
    group = ManyToOne('EmploymentAdHocSectorGroup', colname='group_id')

    class Admin(EntityAdmin):
        verbose_name='Employment Ad Hoc Sector Group Definition'
        list_display=['sector_id', 'group_id']
        field_attributes = dict(sector_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                group_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
                                
class EmploymentAdHocSectorGroup(Entity):
    using_options(tablename='employment_adhoc_sector_groups')
    id = Field(Integer, primary_key=True)
    group_id = Field(Integer)
    name = Field(String(20))

    class Admin(EntityAdmin):
        verbose_name='Employment Ad Hoc Sector Group'
        list_display=['group_id', 'name']
        field_attributes = dict(group_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1))
    
class EmploymentSector(Entity):
    using_options(tablename='employment_sectors')
    id = Field(Integer, primary_key=True, colname='sector_id')
    name = Field(String(20))
    
    class Admin(EntityAdmin):
        verbose_name='Employment Sector'
        list_display=['sector_id', 'name']
        field_attributes = dict(sector_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1))
        
class Faz(Entity):
    using_options(tablename='fazes')
    id = Field(Integer, primary_key=True, colname='faz_id')
    large_area = ManyToOne('LargeArea', colname='large_area_id')
    
    class Admin(EntityAdmin):
        verbose_name='Faz'
        list_display=['faz_id', 'large_area_id']
        field_attributes = dict(faz_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                large_area_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
                                
class HomeBasedStatus(Entity):
    using_options(tablename='home_based_status')
    id = Field(Integer, primary_key=True)
    home_based_status = Field(Integer)
    name = Field(String(20))

    class Admin(EntityAdmin):
        verbose_name='Home Based Statu'
        list_display=['home_based_status', 'name']
        field_attributes = dict(home_based_status=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1))

class Household(Entity):
    using_options(tablename='households')
    id = Field(Integer, primary_key=True, colname='household_id')
    building = ManyToOne('Building', colname='building_id')
    persons = Field(Integer)
    income = Field(Integer)
    age_of_head = Field(Integer)
    race = ManyToOne('RaceName', colname='race_id')
    workers = Field(Integer)
    children = Field(Integer)
    cars = Field(Integer)

    class Admin(EntityAdmin):
        verbose_name='Household'
        list_display=[
            'household_id',
            'building_id',
            'persons',
            'income',
            'age_of_head',
            'race_id',
            'workers',
            'children',
            'cars'
            ]
        field_attributes = dict(household_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                persons=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=15),
                                income=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=1000000),
                                age_of_head=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=100),
                                race_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                workers=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=15),
                                children=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=15),
                                cars=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=15)
                                )
            
class HouseholdCharacteristicsForHT(Entity):
    using_options(tablename='household_characteristics_for_ht')
    id = Field(Integer, primary_key=True)
    characteristic = Field(String(20))
    min = Field(Integer)
    max = Field(Integer)

    class Admin(EntityAdmin):
        verbose_name='Household Characteristics for HT'
        list_display=['characteristic', 'min', 'max']
        field_attributes = dict(min=dict(delegate=delegates.IntegerDelegate, calculator=False),
                                max=dict(delegate=delegates.IntegerDelegate, calculator=False)
                                )

class HouseholdsForEstimation(Entity):
    using_options(tablename='households_for_estimation')
    id = Field(Integer, primary_key=True)
    household_id = Field(Integer)
    building = ManyToOne('Building', colname='building_id')
    persons = Field(Integer)
    income = Field(Integer)
    age_of_head = Field(Integer)
    race = ManyToOne('RaceName', colname='race_id')
    workers = Field(Integer)
    children = Field(Integer)
    cars = Field(Integer)

    class Admin(EntityAdmin):
        verbose_name='Households for Estimation'
        list_display=[
            'household_id',
            'building_id',
            'persons',
            'income',
            'age_of_head',
            'race_id',
            'workers',
            'children',
            'cars'
            ]
        field_attributes = dict(household_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                persons=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=15),
                                income=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=1000000),
                                age_of_head=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=100),
                                race_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                workers=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=15),
                                children=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=15),
                                cars=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=15)
                                )
                                
class Job(Entity):
    using_options(tablename='jobs')
    id = Field(Integer, primary_key=True, colname='job_id')
    building = ManyToOne('Building', colname='building_id')
    home_based_status = Field(Integer)
    sector = ManyToOne('EmploymentSector', colname='sector_id')

    class Admin(EntityAdmin):
        verbose_name='Job'
        list_display=['job_id', 'building_id', 'home_based_status', 'sector_id']
        field_attributes = dict(job_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                home_based_status=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1),
                                sector_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
                                
class JobsForEstimation(Entity):
    using_options(tablename='jobs_for_estimatiion')
    id = Field(Integer, primary_key = True, colname='job_id')
    building = ManyToOne('Building', colname='building_id')
    home_based_status = Field(Integer)
    sector = ManyToOne('EmploymentSector', colname='sector_id')
    
    class Admin(EntityAdmin):
        verbose_name='Jobs for Estimation'
        list_display=['job_id', 'building_id', 'home_based_status', 'sector_id']
        field_attributes = dict(job_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                home_based_status=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1),
                                sector_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
                                
class LargeArea(Entity):
    using_options(tablename='large_areas')
    id = Field(Integer, primary_key=True, colname='large_area_id')
    large_area_name = Field(String(50))
    county = ManyToOne('County', colname='county_id')
    
    class Admin(EntityAdmin):
        verbose_name='Large Area'
        list_display=['large_area_id', 'large_area_name', 'county_id']
        field_attributes = dict(large_area_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                county_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )

class PlanType(Entity): #Needed for zones?
    using_options(tablename='plan_types')
    id = Field(Integer, primary_key=True, colname='plan_type_id')
    plan_type_name = Field(String(50))
    
    class Admin(EntityAdmin):
        verbose_name='Plan Type'
        list_display=['plan_type_id', 'plan_type_name']
        field_attributes = dict(plan_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1))
        
class RaceName(Entity):
    using_options(tablename='race_name')
    id = Field(Integer, primary_key=True, colname='race_id')
    minority = Field(Integer)
    name = Field(String(20))
    
    class Admin(EntityAdmin):
        verbose_name='Race Names'
        list_display=['race_id', 'minority', 'name']
        field_attributes = dict(race_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                minority=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1)
                                )
    
class Refinement(Entity):
    using_options(tablename='refinements')
    id = Field(Integer, primary_key=True, colname='refinement_id')
    transaction_id = Field(Integer)
    agent_dataset = Field(String(25))
    agent_expression = Field(String(200))
    amount = Field(Integer)
    location_capacity_attribute= Field(String(50))
    location_expression = Field(String(200))
    year = Field(Integer)
    
    class Admin(EntityAdmin):
        verbose_name='Refinement'
        list_display=[
            'refinement_id',
            'transaction_id', 
            'agent_dataset',
            'agent_expression',
            'amount',
            'location_capacity_attribute',
            'location_expression',
            'year'
            ]
        field_attributes = dict(refinement_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                transaction_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                amount=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0),
                                year=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1950, maximum=2050)
                                )
            
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
    
    class Admin(EntityAdmin):
        verbose_name='Scheduled Development Event'
        list_display=['year', 'action', 'attribute', 'amount', 'building_id']
        field_attributes = dict(year=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1950, maximum=2050),
                                amount=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0),
                                building_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
                                
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
    
    class Admin(EntityAdmin):
        verbose_name='Scheduled Employment Event'
        list_display=['year,' 'action', 'attribute', 'amount', 'sector_id']
        field_attributes = dict(year=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1950, maximum=2050),
                                amount=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0),
                                sector_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
                                
class TargetVacancy(Entity):
    using_options(tablename='target_vacancies')
    year = Field(Integer, primary_key=True)
    building_type = ManyToOne('BuildingType', colname='building_type_id')
    target_vacancy_rate = Field(Float)
    
    class Admin(EntityAdmin):
        verbose_name='Target Vacancie'
        list_display=['year', 'building_type_id', 'target_vacancy_rate']
        field_attributes = dict(year=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1950, maximum=2050),
                                target_vacancy_rate=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1),
                                building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
    
class TravelData(Entity):
    using_options(tablename='travel_data')
    id = Field(Integer, primary_key=True)
    from_zone_id = Field(Integer)
    to_zone_id = Field(Integer)
    am_single_vehicle_to_work_travel_time = Field(Integer)
    #Enter any additional columns needed from travel model skims
    
    class Admin(EntityAdmin):
        verbose_name='Travel Data'
        list_display=['from_zone_id', 'to_zone_id', 'am_single_vehicle_to_work_travel_time']
        field_attributes = dict(from_zone_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                to_zone_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                am_single_vehicle_to_work_travel_time=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
        
class Zone(Entity):
    using_options(tablename='zones')
    id = Field(Integer, primary_key=True, colname='zone_id')
    county = Field(String(20))
    faz = ManyToOne('Faz', colname='faz_id')
    
    class Admin(EntityAdmin):
        verbose_name='Zone'
        list_display=['zone_id', 'county', 'faz_id']
        field_attributes = dict(zone_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                faz_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
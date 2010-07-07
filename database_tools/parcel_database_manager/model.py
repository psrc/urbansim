# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010 University of California, Berkeley
# See opus_core/LICENSE

import camelot.types
from camelot.model import metadata, Entity, Field, ManyToOne, OneToMany, Integer, String, Float, using_options
from camelot.view.controls import delegates
from camelot.view.elixir_admin import EntityAdmin
from camelot.view.forms import *

__metadata__ = metadata

class AnnualHouseholdControlTotal(Entity):
    using_options(tablename='annual_household_control_totals')
    id = Field(Integer, primary_key=True)
    year = Field(Integer)
    persons = Field(Integer)
    total_number_of_households = Field(Integer)
    
    class Admin(EntityAdmin):
        verbose_name='Household Control Total'
        list_display=['year', 'persons', 'total_number_of_households']
        list_filter = ['persons', 'year']
        field_attributes = dict(year=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1900, maximum=2050),
                                persons=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=15),
                                total_number_of_households=dict(delegate=delegates.IntegerDelegate, calculator=False)
                                )

class AnnualEmploymentControlTotal(Entity):
    using_options(tablename='annual_employment_control_totals')
    id = Field(Integer, primary_key=True)
    year = Field(Integer)
    #sector_id = Field(Integer)
    sector = ManyToOne('EmploymentSector', colname='sector_id')
    home_based_status = Field(Integer)
    number_of_jobs = Field(Integer)

    class Admin(EntityAdmin):
        verbose_name='Employment Control Total'
        list_display=['year', 'sector_id','home_based_status', 'number_of_jobs']
        #list_filter = ['sector_id', 'year']
        field_attributes = dict(year=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1900, maximum=2050),
                                sector_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=100),
                                home_based_status=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1),
                                number_of_jobs=dict(delegate=delegates.IntegerDelegate, calculator=False)
                                )

class AnnualRelocationRatesForHousehold(Entity):
    using_options(tablename='annual_relocation_rates_for_households')
    id = Field(Integer, primary_key=True)
    year = Field(Integer)
    age_of_head_min = Field(Integer)
    age_of_head_max = Field(Integer)
    income_min = Field(Integer)
    income_max = Field(Integer)
    probability_of_relocating = Field(Float(2))
    
    class Admin(EntityAdmin):
        verbose_name='Annual Relocation Rates for Household'
        list_display=['year','age_of_head_min', 'age_of_head_max', 'income_min', 'income_max', 'probability_of_relocating']
        field_attributes = dict(year=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1900, maximum=2050),
                                age_of_head_min=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=100),
                                age_of_head_max=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=100),
                                income_min=dict(delegate=delegates.IntegerDelegate, calculator=False),
                                income_max=dict(delegate=delegates.IntegerDelegate, calculator=False),
                                probability_of_relocating=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1)
                                )
        
class AnnualJobRelocationRates(Entity):
    using_options(tablename='annual_job_relocation_rates')
    id = Field(Integer, primary_key=True)
    sector = ManyToOne('EmploymentSector', colname='sector_id')
    job_relocation_probability = Field(Float(2))

    class Admin(EntityAdmin):
        verbose_name='Annual Job Relocation Rate'
        list_display=['sector_id', 'job_relocation_probability']
        field_attributes = dict(sector_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=100),
                                job_relocation_probability=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1)
                                )
        
class Building(Entity):
    using_options(tablename='buildings')
    id = Field(Integer, primary_key=True, colname='building_id')
    building_quality_id = Field(Integer)
    building_type = ManyToOne('BuildingType', colname='building_type_id')
    improvement_value = Field(Integer)
    land_area = Field(Integer)
    total_building_sqft = Field(Integer)
    non_residential_sqft = Field(Integer)
    residential_units = Field(Integer)
    sqft_per_unit = Field(Integer)
    year_built = Field(Integer)
    stories = Field(Integer)
    tax_exempt = Field(Integer)
    parcel = ManyToOne('Parcel', colname='parcel_id')
    parcel_local = ManyToOne('Parcel', colname='parcel_local_id')
    
    class Admin(EntityAdmin):
        verbose_name='Building'
        list_display=[
            'building_id',
            'building_quality_id',
            'building_type_id',
            'improvement_value',
            'land_area',
            'total_building_sqft',
            'non_residential_sqft',
            'residential_units',
            'sqft_per_unit',
            'year_built',
            'stories',
            'tax_exempt',
            'parcel_id',
            'parcel_local_id'
            ]
        field_attributes = dict(building_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_quality_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                improvement_value=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                land_area=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                total_building_sqft=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                non_residential_sqft=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                residential_units=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                sqft_per_unit=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                year_built=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1950, maximum=2050),
                                stories=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=150),
                                tax_exempt=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1),
                                parcel_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                parcel_local_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
            
class BuildingSqftPerJob(Entity):
    using_options(tablename='building_sqft_per_job')
    id = Field(Integer, primary_key=True)
    building_type_id = Field(Integer)
    zone_id = Field(Integer)
    building_sqft_per_job = Field(Integer)
    
    class Admin(EntityAdmin):
        verbose_name='Building Sqft Per Job'
        list_display=['building_type_id', 'zone_id', 'building_sqft_per_job']
        field_attributes = dict(building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                zone_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_sqft_per_job=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )

class BuildingType(Entity):
    using_options(tablename='building_types')
    id = Field(Integer, primary_key=True, colname='building_type_id')
    is_residential = Field(Integer)
    building_type_name = Field(String(20))
    building_type_description = Field(String(200))
    unit_name = Field(String(20))
    generic_building_type_id = Field(Integer)
    generic_building_type_name = Field(String(20))

    class Admin(EntityAdmin):
        verbose_name='Building Type'
        list_display=[
            'building_type_id',
            'is_residential',
            'building_type_name',
            'building_type_description',
            'unit_name',
            'generic_building_type_id',
            'generic_building_type_name'
            ]
        field_attributes = dict(building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                is_residential=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1),
                                generic_building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
            
#class City(Entity):
#    using_options(tablename='cities')
#    city_id = Field(Integer, primary_key=True)
#    city_name = Field(String(25))
#
#    class Admin(EntityAdmin):
#        verbose_name='Cities'
#        list_display=['city_id', 'city_name']
        
class County(Entity):
    using_options(tablename='counties')
    id = Field(Integer, primary_key=True, colname='county_id')
    county_name = Field(String(20))
    county_fips = Field(String(10))

    class Admin(EntityAdmin):
        verbose_name='Countie'
        list_display=['county_id', 'county_name', 'county_fips']
        field_attributes = dict(county_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1))
        
class DemolitionCostPerSqft(Entity):
    using_options(tablename='demolition_cost_per_sqft')
    id = Field(Integer, primary_key=True)
    building_type = ManyToOne('BuildingType', colname='building_type_id')
    #building_type_name = Field(String(20))
    demolition_cost_per_sqft = Field(Integer)
    
    class Admin(EntityAdmin):
        verbose_name='Demolition Cost per Sqft'
        list_display=['building_type_id','demolition_cost_per_sqft']
        field_attributes = dict(building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                demolition_cost_per_sqft=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
        
class DevelopmentConstraint(Entity):
    using_options(tablename='development_constraints')
    id = Field(Integer, primary_key=True)
    constraint_id = Field(Integer)
    generic_land_use_type = ManyToOne('GenericLandUseType', colname='generic_land_use_type_id')
    plan_type = ManyToOne('PlanType', colname='plan_type_id')
    minimum = Field(Integer)
    maximum = Field(Integer)
    
    class Admin(EntityAdmin):
        verbose_name='Development Constraint'
        list_display=['constraint_id', 'generic_land_use_type_id', 'plan_type_id', 'minimum', 'maximum']
        field_attributes = dict(constraint_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                generic_land_use_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                plan_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                minimum=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                maximum=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
        
class DevelopmentEventHistory(Entity):
    using_options(tablename='development_event_history')
    id = Field(Integer, primary_key=True)
    parcel = ManyToOne('Parcel', colname='parcel_id')
    building_type_id = Field(Integer)
    scheduled_year = Field(Integer)
    residential_units = Field(Integer)
    non_residential_sqft = Field(Integer)
    change_type = Field(String(1))
    
    class Admin(EntityAdmin):
        verbose_name='Development Event History'
        list_display=[
            'parcel_id',
            'building_type_id',
            'scheduled_year',
            'residential_units',
            'non_residential_sqft',
            'change_type'
            ]
        field_attributes = dict(parcel_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                scheduled_year=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1950, maximum=2050),
                                residential_units=dict(delegate=delegates.IntegerDelegate, calculator=False),
                                non_residential_sqft=dict(delegate=delegates.IntegerDelegate, calculator=False),
                                )
            
class DevelopmentProjectProposal(Entity):
    using_options(tablename='development_project_proposals')
    id = Field(Integer, primary_key=True, colname='proposal_id')
#    proposal_id = Field(Integer)
    parcel = ManyToOne('Parcel', colname='parcel_id')
    template = ManyToOne('DevelopmentTemplate', colname='template_id')
    status_id = Field(Integer) 
    #1 (in active development), 2 (proposed for development), 3 (planned and will be developed), 4 (tentative), 5 (not available), 6 (refused)
    start_year = Field(Integer)
    is_redevelopment = Field(Integer) # 1 requires redevelopment, 0 otherwise            
    
    class Admin(EntityAdmin):
        verbose_name='Development Project Proposal'
        list_display=[
            'proposal_id',
            'parcel_id',
            'template_id',
            'status_id',
            'start_year',
            'is_redevelopment'
            ]
        field_attributes = dict(proposal_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                parcel_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                template_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                status_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                start_year=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1950, maximum=2050),
                                is_redevelopment=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1)
                                )
            
class DevelopmentTemplate(Entity):
    using_options(tablename='development_templates')
    id = Field(Integer, primary_key=True)
    template_id = Field(Integer)
    percent_land_overhead = Field(Integer)
    land_sqft_min = Field(Integer)
    land_sqft_max = Field(Integer)
    density = Field(Float(2))
    density_type = Field(String(20))
    land_use_type_id = Field(Integer)
    development_type = Field(String(20))
    is_active = Field(Integer)
    
    class Admin(EntityAdmin):
        verbose_name='Development Template'
        list_display=[
            'template_id',
            'percent_land_overhead',
            'land_sqft_min',
            'land_sqft_max',
            'density',
            'density_type',
            'land_use_type_id',
            'development_type',
            'is_active'
            ]
        field_attributes = dict(template_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                percent_land_overhead=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=100),
                                land_sqft_min=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                land_sqft_max=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                density=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maxmimum=1),
                                land_use_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                is_active=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1)
                                )
                                
class DevelopmentTemplateComponents(Entity):
    using_options(tablename='development_template_components')
    id = Field(Integer, primary_key=True, colname='component_id')
    template_id = Field(Integer)
    building_type = ManyToOne('BuildingType', colname='building_type_id')
    percent_building_sqft = Field(Integer)
    construction_cost_per_unit = Field(Integer)
    building_sqft_per_unit = Field(Integer)
    
    class Admin(EntityAdmin):
        verbose_name='Development Template Component'
        list_display=[
            'component_id',
            'template_id',
            'building_type_id',
            'percent_building_sqft',
            'construction_cost_per_unit',
            'building_sqft_per_unit'
            ]
        field_attributes = dict(component_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                template_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                percent_building_sqft=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=100),
                                construction_cost_per_unit=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_sqft_per_unit=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
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
        
class GenericLandUseType(Entity):
    using_options(tablename='generic_land_use_types')
    id = Field(Integer, primary_key=True, colname='generic_land_use_type_id')
    generic_description = Field(String(50))

    class Admin(EntityAdmin):
        verbose_name='Generic Land Use Type'
        list_display=['generic_land_use_type_id', 'generic_description']
        field_attributes = dict(generic_land_use_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1))
        
class HomeBasedStatus(Entity):
    using_options(tablename='home_based_status')
    id = Field(Integer, primary_key=True)
    home_based_status = Field(Integer)
    name = Field(String(20))

    class Admin(EntityAdmin):
        verbose_name='Home Based Statuse'
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
    id = Field(Integer, primary_key=True)
    job_id = Field(Integer)
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
        
class LandUseType(Entity):
    using_options(tablename='land_use_types')
    id = Field(Integer, primary_key=True, colname='land_use_type_id')
    description = Field(String(40))
    land_use_name = Field(String(25))
    unit_name = Field(String(15))
    generic_land_use_type = ManyToOne('GenericLandUseType', colname='generic_land_use_type_id')

    class Admin(EntityAdmin):
        verbose_name='Land Use Type'
        list_display=[
            'land_use_type_id',
            'description',
            'land_use_name',
            'unit_name',
            'generic_land_use_type_id'
            ]
        field_attributes = dict(land_use_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                generic_land_use_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
            
class LargeArea(Entity):
    using_options(tablename='large_areas')
    id = Field(Integer, primary_key=True)
    large_area_id = Field(Integer)
    large_area_name = Field(String(50))
    county = ManyToOne('County', colname='county_id')
    
    class Admin(EntityAdmin):
        verbose_name='Large Area'
        list_display=['large_area_id', 'large_area_name', 'county_id']
        field_attributes = dict(large_area_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                county_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
        
class Parcel(Entity):
    using_options(tablename='parcels')
    id = Field(Integer, primary_key=True, colname='parcel_id')
    parcel_local_id = Field(Integer, index=True) #Store assessors key to merge other data
    land_value = Field(Integer)
    parcel_sqft = Field(Integer)
    plan_type = ManyToOne('PlanType', colname='plan_type_id')
    centroid_x = Field(Integer) #optional
    centroid_y = Field(Integer) #optional
    tax_exempt_flag = Field(Integer)
    county = ManyToOne('County', colname='county_id')
    zone = ManyToOne('Zone', colname='zone_id')
    census_tract_block = Field(String(20))
    
    class Admin(EntityAdmin):
        verbose_name='Parcel'
        list_display=[
            'parcel_id',
            'parcel_local_id',
            'land_value',
            'parcel_sqft',
            'plan_type_id',
            'centroid_x',
            'centroid_y',
            'tax_exempt_flag',
#            'city',
            'county_id',
            'zone_id',
            'census_tract_block'
            ]
        field_attributes = dict(parcel_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                land_value=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                parcel_sqft=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                plan_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                centroid_x=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                centroid_y=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                tax_exempt_flag=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1),
                                county_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                zone_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                )
            
class PlanType(Entity): #Needed for zones?
    using_options(tablename='plan_types')
    id = Field(Integer, primary_key=True)
    plan_type_id = Field(Integer)
    name = Field(String(50))

    class Admin(EntityAdmin):
        verbose_name='Plan Type'
        list_display=['plan_type_id', 'name']
        field_attributes = dict(plan_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1))
        
class RaceName(Entity):
    using_options(tablename='race_names')
    id = Field(Integer, primary_key=True, colname='race_id')
    minority = Field(Integer)
    name = Field(String(20))

    class Admin(EntityAdmin):
        verbose_name='Race Name'
        list_display=['race_id', 'minority', 'name']
        field_attributes = dict(race_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                minority=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1)
                                )
        
class Refinement(Entity):
#    refinement_id = Field(Integer)
    using_options(tablename='refinements')
    id = Field(Integer, primary_key=True)    
    transaction_id = Field(Integer)
    agent_dataset = Field(String(25))
    agent_expression = Field(String(200))
    amount = Field(Integer)
    location_capacity_attribute=Field(String(50))
    location_expression = Field(String(200))
    year = Field(Integer)

    class Admin(EntityAdmin):
        verbose_name='Refinement'
        list_display=[
            'transaction_id',
            'agent_dataset',
            'agent_expression',
            'amount',
            'location_capacity_attribute',
            'location_expression',
            'year'
            ]
        field_attributes = dict(transaction_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                amount=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
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
                                amount=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
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
        list_display=['year', 'action', 'attribute', 'amount', 'sector_id']
        field_attributes = dict(year=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1950, maximum=2050),
                                amount=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                sector_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )

class TargetVacancy(Entity):
    using_options(tablename='target_vacancies')
    id = Field(Integer, primary_key=True)
    year = Field(Integer)
    building_type = ManyToOne('BuildingType', colname='building_type_id')
    target_vacancy_rate = Field(Float(2))

    class Admin(EntityAdmin):
        verbose_name='Target Vacancie'
        list_display=['year', 'building_type_id', 'target_vacancy_rate']
        field_attributes = dict(year=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1950, maximum=2050),
                                building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                target_vacancy_rate=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1)
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
        
class VelocityFunction(Entity):
    using_options(tablename='velocity_functions')
    id = Field(Integer, primary_key=True, colname='velocity_function_id')
    annual_construction_schedule = Field(String) 
    #A numbered list in brackets of the form, '[p1, p2,...,pn]', indicating with each entry the percentage complete of the 
    #project each year from its start. The last entry must be '100'.
    building_type = ManyToOne('BuildingType', colname='building_type_id')
    minimum_units = Field(Integer)
    maximum_units = Field(Integer)
    
    class Admin(EntityAdmin):
        verbose_name='Velocity Function'
        list_display=[
            'velocity_function_id',
            'annual_construction_schedule',
            'building_type_id',
            'minimum_units',
            'maximum_units'
            ]
        field_attributes = dict(velocity_function_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                annual_construction_schedule=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                minimum_units=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                maximum_units=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
            
class Zone(Entity):
    using_options(tablename='zones')
    id = Field(Integer, primary_key=True, colname='zone_id')
#    city = ManyToOne('City', colname='city_id')    
    county = ManyToOne('County', colname='county_id')
    faz = ManyToOne('Faz', colname='faz_id')
    
    class Admin(EntityAdmin):
        verbose_name='Zone'
        list_display=['zone_id', 'county_id', 'faz_id']
        field_attributes = dict(zone_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                county_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                faz_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
                                

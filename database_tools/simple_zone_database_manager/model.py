import camelot.types
from camelot.model import metadata, Entity, Field, ManyToOne, OneToMany, Integer, String, Float, using_options
from camelot.view.controls import delegates
from camelot.view.elixir_admin import EntityAdmin
from camelot.view.forms import *

__metadata__ = metadata

class AnnualEmploymentControlTotal(Entity):
    using_options(tablename='annual_employment_control_totals')
    id = Field(Integer, primary_key=True)
    year = Field(Integer)
    sector = ManyToOne('EmploymentSector', colname='sector_id')
    total_number_of_jobs = Field(Integer)

    class Admin(EntityAdmin):
        verbose_name='Employment Control Total'
        list_display=['year', 'sector_id', 'total_number_of_jobs']
        #list_filter = ['sector_id', 'year']
        field_attributes = dict(year=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1900, maximum=2050),
                                sector_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=100),
                                total_number_of_jobs=dict(delegate=delegates.IntegerDelegate, calculator=False)
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

class Building(Entity):
    using_options(tablename='buildings')
    id = Field(Integer, primary_key=True, colname='building_id')
    building_type = ManyToOne('BuildingType', colname='building_type_id')
    households = Field(Integer)
    jobs = Field(Integer)
    max_households = Field(Integer)
    max_jobs = Field(Integer)
    zone = ManyToOne('Zone', colname='zone_id')

    class Admin(EntityAdmin):
        verbose_name='Building'
        list_display=[
            'building_id',
            'building_type_id',
            'households',
            'jobs',
            'max_households',
            'max_jobs',
            'zone_id'
            ]
        field_attributes = dict(building_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                households=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                jobs=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                max_households=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                max_jobs=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
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
                                is_residential=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1),
                                )
 
class EmploymentSector(Entity):
    using_options(tablename='employment_sectors')
    id = Field(Integer, primary_key=True, colname='sector_id')
    trm_code = Field(String(20))
    
    class Admin(EntityAdmin):
        verbose_name='Employment Sector'
        list_display=['sector_id', 'trm_code']
        field_attributes = dict(sector_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1))

class Household(Entity):
    using_options(tablename='households')
    id = Field(Integer, primary_key=True, colname='household_id')
    blockgroup_id = Field(Integer)
    building = ManyToOne('Building', colname='building_id')
    building_type = ManyToOne('BuildingType', colname='building_type_id')
    persons = Field(Integer)
    income = Field(Integer)
    age_of_head = Field(Integer)
    race_id = Field(Integer)
    workers = Field(Integer)
    children = Field(Integer)
    cars = Field(Integer)
    zone = ManyToOne('Zone', colname='zone_id')

    class Admin(EntityAdmin):
        verbose_name='Household'
        list_display=[
            'household_id',
            'blockgroup_id',
            'building_id',
            'building_type_id',
            'persons',
            'income',
            'age_of_head',
            'race_id',
            'workers',
            'children',
            'cars',
            'zone_id'
            ]
        field_attributes = dict(household_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                blockgroup_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_type_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                persons=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=15),
                                income=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=1000000),
                                age_of_head=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=100),
                                race_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                workers=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=15),
                                children=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=15),
                                cars=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1, maximum=15),
                                zone_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
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

class Job(Entity):
    using_options(tablename='jobs')
    id = Field(Integer, primary_key=True, colname='job_id')
    building = ManyToOne('Building', colname='building_id')
    home_based_status = Field(Integer)
    sector = ManyToOne('EmploymentSector', colname='sector_id')
    zone = ManyToOne('Zone', colname='zone_id')
    

    class Admin(EntityAdmin):
        verbose_name='Job'
        list_display=['job_id', 'building_id', 'home_based_status', 'sector_id', 'zone_id']
        field_attributes = dict(job_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                building_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                home_based_status=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=0, maximum=1),
                                sector_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                zone_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
        
class TravelData(Entity):
    using_options(tablename='travel_data')
    id = Field(Integer, primary_key=True)
    from_zone_id = Field(Integer)
    to_zone_id = Field(Integer)
    am_lov_distance = Field(Integer)
    am_lov_time = Field(Integer)
    #Enter any additional columns needed from travel model skims
    
    class Admin(EntityAdmin):
        verbose_name='Travel Data'
        list_display=['from_zone_id', 'to_zone_id', 'am_lov_distance', 'am_lov_time']
        field_attributes = dict(from_zone_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                to_zone_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                am_lov_distance=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                am_lov_time=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
        
class Zone(Entity):
    using_options(tablename='zones')
    id = Field(Integer, primary_key=True, colname='zone_id')
    area_type = Field(Integer)
    area = Field(Integer)
    dev_acres = Field(Integer)
    district_id = Field(Integer)
    final_taz = Field(Integer)
    county = Field(String(20))
    
    class Admin(EntityAdmin):
        verbose_name='Zone'
        list_display=['zone_id', 'area_type', 'area', 'dev_acres', 'district_id', 'final_taz', 'county']
        field_attributes = dict(zone_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                area=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                area_type=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                dev_acres=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                district_id=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1),
                                final_taz=dict(delegate=delegates.IntegerDelegate, calculator=False, minimum=1)
                                )
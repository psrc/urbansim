# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from travel_model.models.abstract_travel_model import AbstractTravelModel
from opus_core.session_configuration import SessionConfiguration
from opus_core.resources import Resources
from opus_core.logger import logger
from opus_core.simulation_state import SimulationState
from numpy import array, float32, ones
from opus_core.store.attribute_cache import AttributeCache
from opus_core.datasets.dataset import Dataset
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.sql_storage import sql_storage
from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.database_configuration import DatabaseConfiguration
from opus_core.misc import unique
from opus_core.variables.variable_name import VariableName
from opus_core.variables.attribute_type import AttributeType

class ExportUrbansimDataToOpenamos(AbstractTravelModel):
    """
    """

    def run(self, config, year):
        """ 
        """
        
        tm_config = config['travel_model_configuration']
        database_server_config = tm_config.get("database_server_configuration", 'postgres_test_database_server')
        database_name = tm_config.get("database_name", 'mag_zone_baseyear')
        
        cache_directory = config['cache_directory']
        simulation_state = SimulationState()
        simulation_state.set_cache_directory(cache_directory)
        simulation_state.set_current_time(year)
        attribute_cache = AttributeCache()
        dataset_pool = SessionConfiguration(new_instance=True,
                                            package_order=config['dataset_pool_configuration'].package_order,
                                            in_storage=attribute_cache).get_dataset_pool()
        db_server = DatabaseServer(DatabaseConfiguration(
                                                         database_name = database_name,
                                                         database_configuration = database_server_config
                                                         )
                                                         )

        if not db_server.has_database(database_name): 
            print "Db doesn't exist creating one"
            db_server.create_database(database_name)
        db = db_server.get_database(database_name) 
        output_storage = sql_storage(storage_location = db)
                                                            
        logger.start_block('Compute and export data to openAMOS...')
        hh = dataset_pool.get_dataset('household')
        syn_hh = dataset_pool.get_dataset('synthetic_household')

        hh_variables = ['houseid=household.household_id',
                        'one=household.disaggregate(synthetic_household.one)',
                        'household.homeown',
                        'household.urb',
                        'household.nwrkcnt',
                        'numadlts=household.numadlt',
                        'lifcycge2=household.disaggregate(synthetic_household.lifcycge2)',
                        'numwrkr=household.workers',
                        'household.rur',
                        'household.inclt35k',
                        'household.incge35k',
                        'household.incge75k',
                        'household.incge100k',
                        'household.drvrcnt',
                        'vdratio=household.disaggregate(synthetic_household.vdratio)',
                        'htaz = household.disaggregate(building.zone_id)'                        
                        ]
        hh.compute_variables(hh_variables)
        hh_variables_short_name = unique([VariableName(v).get_alias() for v in hh_variables]).tolist()
        for attr in hh_variables_short_name:
            hh.attribute_boxes[attr].set_type(AttributeType.PRIMARY)

        print 'persons variable names', hh_variables_short_name
        print 'Output storage - ', output_storage
        print 'database name - ', database_name


        hh.write_dataset(attributes=hh_variables_short_name,
                         out_storage=output_storage)
        dataset_pool._remove_dataset(hh.dataset_name)
        persons = dataset_pool.get_dataset('person')
        syn_persons = dataset_pool.get_dataset('synthetic_person')
        persons_variables = ['person.personid',
                             'one=person.disaggregate(synthetic_person.one)',
                             'person.wrkr',
                             #'tmtowrk=mag_zone.person.travel_time_from_home_to_work',
                             #'mag_zone.person.tmtowrk',
                             'tmtowrk=person.disaggregate(synthetic_person.tmtowrk)',
                             'person.ag11t14',
                             'person.agge15',
                             'person.hispanic',
                             'person.fulltim',
                             'person.parttim',
                             'selfemp=person.disaggregate(synthetic_person.selfemp)',
                             'wkhome=person.disaggregate(synthetic_person.wkhome)',
                             'mag_zone.person.wtaz',
                             'person.schtaz'
                             ]
        
        persons.compute_variables(persons_variables)
        persons_variables_short_name = unique([VariableName(v).get_alias() for v in persons_variables]).tolist()
        for attr in persons_variables_short_name:
            persons.attribute_boxes[attr].set_type(AttributeType.PRIMARY)

        print 'persons variable names', persons_variables_short_name
        print 'Output storage - ', output_storage
        print 'database name - ', database_name

                        
        persons.write_dataset(attributes=persons_variables_short_name,
                              out_storage=output_storage)
        dataset_pool._remove_dataset(persons.dataset_name)

        locations = dataset_pool.get_dataset('zone')
        locations_variables = [
                             'retail_employment=zone.aggregate(mag_zone.job.sector_group=="retail")',
                             'public_employment=zone.aggregate(mag_zone.job.sector_group=="public")',
                             'office_employment=zone.aggregate(mag_zone.job.sector_group=="office")',
                             'industrial_employment=zone.aggregate(mag_zone.job.sector_group=="individual")',
                             'other_employment=zone.aggregate(mag_zone.job.sector_group=="other")',

                             'retail_employment_density=zone.aggregate(mag_zone.job.sector_group=="retail")/zone.acres',
                             'public_employment_density=zone.aggregate(mag_zone.job.sector_group=="public")/zone.acres',
                             'office_employment_density=zone.aggregate(mag_zone.job.sector_group=="office")/zone.acres',
                             'industrial_employment_density=zone.aggregate(mag_zone.job.sector_group=="individual")/zone.acres',
                             'other_employment=zone.aggregate(mag_zone.job.sector_group=="other")/zone.acres',

                             'total_area=zone.acres',

                             'lowest_income=zone.aggregate(household.income < scoreatpercentile(household.income, 20))',
                             'low_income=zone.aggregate(household.income < scoreatpercentile(household.income, 40))',
                             'high_income=zone.aggregate(household.income > scoreatpercentile(household.income, 80))',

                             'institutional_population=zone.disaggregate(locations.institutional_population)',
                             'groupquarter_households=zone.disaggregate(locations.groupquarter_households)',

                             'residential_households=zone.number_of_agents(household)',

                             'locationid=zone.zone_id - 100',
                             ]
        
        locations.compute_variables(locations_variables)
        locations_variables_short_name = unique([VariableName(v).get_alias() for v in locations_variables]).tolist()
        for attr in locations_variables_short_name:
            locations.attribute_boxes[attr].set_type(AttributeType.PRIMARY)

        print 'locations variable names', locations_variables_short_name
        print 'Output storage - ', output_storage
        print 'database name - ', database_name

        locations.write_dataset(attributes=locations_variables_short_name,
                              out_storage=output_storage)
        dataset_pool._remove_dataset(locations.dataset_name)

        logger.end_block()
        
if __name__ == "__main__":

    try: import wingdbstub
    except: pass
        
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    (options, args) = parser.parse_args()

    resources = Resources(get_resources_from_file(options.resources_file_name))

    logger.enable_memory_logging()
    ExportUrbansimDataToOpenamos().run(resources, options.year)    

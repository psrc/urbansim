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
            db_server.create_database(database_name)
        db = db_server.get_database(database_name) 
        output_storage = sql_storage(storage_location = db)
                                                            
        logger.start_block('Compute and export data to openAMOS...')
        hh = dataset_pool.get_dataset('household')
        syn_hh = dataset_pool.get_dataset('synthetic_household')
        hh_variables = ['household.houseid',
                        'one=household.disaggregate(synthetic_household.one)',
                        'homeown=household.disaggregate(synthetic_household.homeown)',
                        'urb=household.disaggregate(synthetic_household.urb)',
                        'nwrkcnt=household.disaggregate(synthetic_household.nwrkcnt)',
                        'numadlts=household.disaggregate(synthetic_household.numadlts)',
                        'lifcycge2=household.disaggregate(synthetic_household.lifcycge2)',
                        'numwrkr=household.disaggregate(synthetic_household.numwrkr)',
                        'rur=household.disaggregate(synthetic_household.rur)',
                        'inclt35k=household.disaggregate(synthetic_household.inclt35k)',
                        'incge35k=household.disaggregate(synthetic_household.incge35k)',
                        'incge75k=household.disaggregate(synthetic_household.incge75k)',
                        'incge100=household.disaggregate(synthetic_household.incge100)',
                        'drvrcnt=household.disaggregate(synthetic_household.drvrcnt)',
                        'vdratio=household.disaggregate(synthetic_household.vdratio)',
                        'htaz = household.disaggregate(building.zone_id)'                        
                        ]
        hh.compute_variables(hh_variables)
        hh_variables_short_name = unique([VariableName(v).get_alias() for v in hh_variables]).tolist()
        for attr in hh_variables_short_name:
            hh.attribute_boxes[attr].set_type(AttributeType.PRIMARY)
        hh.write_dataset(attributes=hh_variables_short_name,
                         out_storage=output_storage)
        dataset_pool._remove_dataset(hh.dataset_name)
        
        persons = dataset_pool.get_dataset('person')
        syn_persons = dataset_pool.get_dataset('synthetic_person')
        persons_variables = ['person.personid',
                             'one=person.disaggregate(synthetic_person.one)',
                             'wrkr=person.disaggregate(synthetic_person.wrkr)',
                             'tmtowrk=person.disaggregate(synthetic_person.tmtowrk)',
                             'ag11t14=person.disaggregate(synthetic_person.ag11t14)',
                             'agge15=person.disaggregate(synthetic_person.agge15)',
                             'hisp=person.disaggregate(synthetic_person.hisp)',
                             'fulltim=person.disaggregate(synthetic_person.fulltim)',
                             'partim=person.disaggregate(synthetic_person.partim)',
                             'selfemp=person.disaggregate(synthetic_person.selfemp)',
                             'wkhome=person.disaggregate(synthetic_person.wkhome)',
                             'person.wtaz',
                             'person.schtaz'
                             ]
        
        persons.compute_variables(persons_variables)
        persons_variables_short_name = unique([VariableName(v).get_alias() for v in persons_variables]).tolist()
        for attr in persons_variables_short_name:
            persons.attribute_boxes[attr].set_type(AttributeType.PRIMARY)
                        
        persons.write_dataset(attributes=persons_variables_short_name,
                              out_storage=output_storage)
        dataset_pool._remove_dataset(persons.dataset_name)
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

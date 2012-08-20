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
        database_server_config = tm_config.get("database_server_configuration", 'simtravel_database_server')
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
        hh_recs = dataset_pool.get_dataset('households_recs')
        hh_recs.add_attribute(0,"htaz1")
        hh_recs.flush_dataset()
        #syn_hh = dataset_pool.get_dataset('synthetic_household')

        hh_variables = ['houseid=household.household_id',
                        "hhsize=household.number_of_agents(person)",
                        "one=(household.household_id>0).astype('i')",
                        "inclt35k=(household.income<35000).astype('i')",
                        "incge35k=(household.income>=35000).astype('i')",
                        "incge50k=(household.income>=50000).astype('i')",
                        "incge75k=(household.income>=75000).astype('i')",
                        "incge100k=(household.income>=100000).astype('i')",
                        "inc35t50=((household.income>=35000) & (household.income<50000)).astype('i')",
                        "inc50t75=((household.income>=50000) & (household.income<75000)).astype('i')",
                        "inc75t100=((household.income>=75000) & (household.income<100000)).astype('i')",
                        'htaz1 = (houseid>0)*(household.disaggregate(building.zone_id))',
                        'htaz = ((houseid>0) & (htaz1>100))*(htaz1-100)+((houseid>0) & (htaz1==-1))*1122',
                        "withchild = (household.aggregate(person.age<18)>0).astype('i')",
                        "noc = household.aggregate(person.age<18)",
                        "numadlt = household.aggregate(person.age>=18)",
                        "hinc=household.income",
                        "wif=household.workers",
                        #"wif=household.aggregate(mag_zone.person.is_employed)",
                        'numwrkr=household.workers',
                        #'numwrkr=household.aggregate(mag_zone.person.is_employed)',
                        'nwrkcnt=household.number_of_agents(person) - household.workers',
                        #'nwrkcnt=household.number_of_agents(person) - household.aggregate(mag_zone.person.is_employed)',

                        'yrbuilt=mag_zone.household.yrbuilt',
                        'mag_zone.household.sparent',
                        'mag_zone.household.rur',
                        'mag_zone.household.urb',
                        'zonetidi4 = household.disaggregate(building.zone_id) - 100',
                        ]
        
        self.prepare_attributes(hh, hh_variables)
        attrs_to_export = hh_recs.get_known_attribute_names()

        hh.write_dataset(attributes=attrs_to_export,
                         out_storage=output_storage)
        dataset_pool._remove_dataset(hh.dataset_name)

        persons = dataset_pool.get_dataset('person')

        # Recoding invalid work and school locations to some random valid values
        persons_recs = dataset_pool.get_dataset('persons_recs')
        persons_recs.add_attribute(persons['person_id'],"personuniqueid")
        persons_recs.add_attribute(persons['marriage_status'],"marstat")
        persons_recs.add_attribute(persons['student_status'],"schstat")
        persons_recs.add_attribute(persons['wtaz0'],"htaz_act")
        persons_recs.add_attribute(0,"wtaz_rec")
        persons_recs.add_attribute(0,"wtaz_rec1")
        persons_recs.add_attribute(0,"wtaz_rec2")
        persons_recs.add_attribute(0,"wtaz1")
        persons_recs.add_attribute(0,"wtaz1_1")
        persons_recs.add_attribute(0,"wtaz1_2")
        persons_recs.add_attribute(0,"wtaz1_3")
        persons_recs.add_attribute(persons['student_status'],"schstat")

        persons_recs.add_attribute(0,"htaz")

        persons_recs.flush_dataset()

        #syn_persons = dataset_pool.get_dataset('synthetic_person')
        persons_variables = ['personid=mag_zone.person.unique_member_id',
                             'personuniqueid=person.person_id',
                             'houseid=person.household_id',
                             "one=(person.person_id>0).astype('i')",
                             'trvtime=mag_zone.person.travel_time_from_home_to_work',
                             'timetowk=mag_zone.person.travel_time_from_home_to_work',
                             #'mag_zone.person.tmtowrk',
                             #'tmtowrk=person.disaggregate(synthetic_person.tmtowrk)',
                             "ag5t10=((person.age>=5) & (person.age<=10)).astype('i')",
                             "ag11t14=((person.age>=11) & (person.age<=14)).astype('i')",
                             "ag15t17=((person.age>=15) & (person.age<=17)).astype('i')",
                             "ag18t24=((person.age>=18) & (person.age<=24)).astype('i')",
                             "ag25t34=((person.age>=25) & (person.age<=34)).astype('i')",
                             "ag35t44=((person.age>=35) & (person.age<=44)).astype('i')",
                             "ag45t54=((person.age>=45) & (person.age<=54)).astype('i')",
                             "ag55t64=((person.age>=55) & (person.age<=64)).astype('i')",
                             "agge65=(person.age>=65).astype('i')",

                             "ag12t17=((person.age>=12) & (person.age<=17)).astype('i')",
                             "ag5t14=((person.age>=5) & (person.age<=14)).astype('i')",
                             "agge15=(person.age>=15).astype('i')",

                             "wrkr=(person.employment_status==1).astype('i')",
                             "isemploy=(person.employment_status==1).astype('i')",
                             "fulltim=(mag_zone.person.full_time==1).astype('i')",
                             'parttim=mag_zone.person.part_time',
                             'person.schtaz - 100',
                             
                             'htaz_act = (houseid>0)*(person.disaggregate(building.zone_id, intermediates=[household]))',
                             
                             'wtaz_rec1=0*(mag_zone.person.wtaz <= 100)',
                             'wtaz_rec2=mag_zone.person.wtaz*(mag_zone.person.wtaz > 100)',

                             'wtaz_rec=wtaz_rec1 + wtaz_rec2',

                             'htaz = ((houseid>0) & (htaz_act>100))*(htaz_act - 100)+((houseid>0) & (htaz_act==-1))*1122',

                             'wtaz1_1=(wtaz_rec-100)*((person.employment_status == 1) & (wtaz_rec>0)) ',
                             'wtaz1_2=(htaz-100)*((person.employment_status == 1) & (wtaz_rec<=0))',
                             'wtaz1_3=0*(person.employment_status == 0)',
                             'wtaz1=wtaz1_1 + wtaz1_2 + wtaz1_3',
                       



                             'wtaz = wtaz1',
                             'marstat = person.marriage_status',
                             'schstat = person.student_status',
                             'enroll = person.student_status',
                             'grade = person.student_status & person.education',
                             'educ = person.education',
                             'male = person.sex==1',
                             'female = person.sex==2',

                             "presch = (person.age <= 5).astype('i')",
                             "coled = (person.education >= 10).astype('i')",

                             'race1 = person.race',
                             'white = person.race == 1',
                             'person.hispanic',
                             ]
        
        self.prepare_attributes(persons, persons_variables)

        attrs_to_export = persons_recs.get_known_attribute_names()

        persons.write_dataset(attributes=attrs_to_export,
                              out_storage=output_storage)
        dataset_pool._remove_dataset(persons.dataset_name)
        raw_input("check tables for consistency")

        zones = dataset_pool.get_dataset('zone')
        zones_variables = [
                             "retail_employment=zone.aggregate(mag_zone.job.sector_group=='retail')",
                             "public_employment=zone.aggregate(mag_zone.job.sector_group=='public')",
                             "office_employment=zone.aggregate(mag_zone.job.sector_group=='office')",
                             "industrial_employment=zone.aggregate(mag_zone.job.sector_group=='individual')",
                             "other_employment=zone.aggregate(mag_zone.job.sector_group=='other')",

                             "retail_employment_density=zone.aggregate(mag_zone.job.sector_group=='retail')/zone.acres",
                             "public_employment_density=zone.aggregate(mag_zone.job.sector_group=='public')/zone.acres",
                             "office_employment_density=zone.aggregate(mag_zone.job.sector_group=='office')/zone.acres",
                             "industrial_employment_density=zone.aggregate(mag_zone.job.sector_group=='individual')/zone.acres",
                             "other_employment_density=zone.aggregate(mag_zone.job.sector_group=='other')/zone.acres",

                             "total_area=zone.acres",

                             "lowest_income=zone.aggregate(household.income < scoreatpercentile(household.income, 20))",
                             "low_income=zone.aggregate(household.income < scoreatpercentile(household.income, 40))",
                             "high_income=zone.aggregate(household.income > scoreatpercentile(household.income, 80))",

                             #"institutional_population=zone.disaggregate(locations.institutional_population)",
                             #"groupquarter_households=zone.disaggregate(locations.groupquarter_households)",

                             "residential_households=zone.number_of_agents(household)",

                             "locationid=zone.zone_id",
                             ]
        
        locations = dataset_pool['locations']
        self.prepare_attributes(zones, zones_variables, dataset2=locations)
        attrs_to_export = locations.get_known_attribute_names()

        locations.write_dataset(attributes=attrs_to_export,
                                out_storage=output_storage)
        dataset_pool._remove_dataset(locations.dataset_name)
        #raw_input("check location block")

        logger.end_block()

    def prepare_attributes(self, dataset1, variables_to_compute, dataset2=None):
        dataset1.compute_variables(variables_to_compute)
        variables_short_name = unique([VariableName(v).get_alias() for v in variables_to_compute]).tolist()

        if dataset2 is None:
            # dataset1 is the one to be exported
            for attr in variables_short_name:
                dataset1.attribute_boxes[attr].set_type(AttributeType.PRIMARY)
        else:
            # dataset2 is the one to be exported
            dataset2_index = dataset2.get_id_index(dataset1.get_id_attribute())
            for attr in variables_short_name:
                dataset2.modify_attribute(attr, dataset1[attr], dataset2_index)
        
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

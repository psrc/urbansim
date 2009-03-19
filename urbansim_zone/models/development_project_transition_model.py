# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.resources import Resources
from opus_core.misc import DebugPrinter
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.development_project_dataset import DevelopmentProjectDataset
from urbansim.datasets.development_event_dataset import DevelopmentEventTypeOfChange
from opus_core.model import Model
from numpy.random import randint
from opus_core.logger import logger
from numpy import arange, array, zeros, ones, float32, int32, concatenate, logical_and, round_

class DevelopmentProjectTransitionModel( Model ):
    """
    Creates development projects. Each development project is for a single type
    of development, e.g. 'industrial' or 'commercial'.  This model creates
    enough development projects to match the desired vacancy rates, as defined in the target_vacancies
    table.  It does not place any projects in locations; that is the job of the development project
    location choice models.  The distribution of project sizes (amount of space, value of space) is
    determined by sampling from the projects in the development_event_history table.
    """
    model_name = "Development Project Transition Model"
    project_units = {'commercial': 'commercial_job_spaces',
                     'industrial': 'industrial_job_spaces',
                     'residential': 'residential_units'}
    
    def __init__( self, debuglevel=0 ):
        self.debug = DebugPrinter( debuglevel )

    def pre_check( self, location_set, vacancy_table, types ):
        for ptype in types:
            if not ptype in self.project_units.keys():
                raise KeyError, "Project type %s is not included in project_units." % ptype
            self.check_for_space( location_set.get_attribute(self.project_units[ptype]))
            self.check_target_vacancy_is_not_100_percent( vacancy_table.get_attribute( "target_total_%s_vacancy" % ptype))

    def check_for_space( self, values ):
        """Check that this array of values sums to something > 0."""
        self.do_check( "x > 0", array( [values.sum()] ) )

    def check_target_vacancy_is_not_100_percent( self, value ):
        """Check that the target vacancy rate is not 100% (ratio == 1), because it doesn't make sense,
        and it also causes a divide by 0 error."""
        self.do_check( "x < 1", value )

    def run( self, vacancy_table, history_table, year, location_set, dataset_pool=None, resources=None ):
        self.dataset_pool=dataset_pool
        vacancy_attributes = vacancy_table.get_known_attribute_names()
        project_types = []
        for attr in vacancy_attributes:
            s = attr.split('_')
            if len(s) < 4:
                continue
            if '_'.join([s[0], s[1], s[3]]) == 'target_total_vacancy':
                project_types.append(s[2])
        self._compute_vacancy_and_total_units_variables(location_set, project_types, resources)
        self.pre_check( location_set, vacancy_table, project_types)
        target_rates = self._get_target_vacancy_rates(vacancy_table, year, project_types)
    
        projects = {}
        for project_type, target_vacancy_rate in target_rates.iteritems():
            # determine current-year vacancy rates
            vacant_units_sum = location_set.get_attribute(self.variable_for_vacancy[project_type]).sum()
            units_sum = float( location_set.get_attribute(self.variable_for_total_units[project_type]).sum() )
            should_develop_units = int(round(max( 0, ( target_vacancy_rate * units_sum - vacant_units_sum ) /
                                         ( 1 - target_vacancy_rate ) )))
            logger.log_status(project_type + ": vacant units: %d, should be vacant: %f, sum units: %d"
                          % (vacant_units_sum, target_vacancy_rate * units_sum, units_sum))

            if not should_develop_units:
                logger.log_note(("Will not build any " + project_type + " units, because the current vacancy of %d units\n"
                             + "is more than the %d units desired for the vacancy rate of %f.")
                            % (vacant_units_sum,
                               target_vacancy_rate * units_sum,
                               target_vacancy_rate))
            #create projects
            if should_develop_units > 0:
                projects[project_type] = self._create_projects(should_develop_units, project_type, history_table,
                                                               location_set, units_sum, resources)
                projects[project_type].add_submodel_categories()
            else:
                projects[project_type] = None
        return projects

    def _get_target_vacancy_rates(self, vacancy_table, year, project_types):
        rates = {}
        for ptype in project_types:
            rates[ptype] = vacancy_table.get_attribute_by_id("target_total_%s_vacancy" % ptype, year)
        return rates
    
    def _compute_vacancy_and_total_units_variables(self, location_set, project_types, resources=None):
        compute_resources = Resources(resources)
        compute_resources.merge({"debug":self.debug})
        self.variable_for_vacancy = {}
        self.variable_for_total_units = {}
        for ptype in project_types:
            self.variable_for_vacancy[ptype] = compute_resources.get(
                                    "%s_vacant_variable" % ptype,
                                    "urbansim_zone.%s.vacant_%s" % (location_set.get_dataset_name(),
                                                                     self.project_units[ptype]))
            self.variable_for_total_units[ptype] = compute_resources.get(
                                    "%s_total_units_variable" % ptype,
                                    "urbansim_zone.%s.%s" % (location_set.get_dataset_name(), self.project_units[ptype]))
            location_set.compute_variables([self.variable_for_vacancy[ptype], self.variable_for_total_units[ptype]], 
                                           dataset_pool=self.dataset_pool, resources = compute_resources)
            
    def _create_projects(self, should_develop_units, project_type, history_table, location_set, units_sum, resources=None):
        history_values = history_table.get_attribute(self.project_units[project_type])
        type_code_values = history_table.get_change_type_code_attribute(self.project_units[project_type])
        # take only non-zero history values and those that don't represent demolished buildings 
        history_values_without_zeros = history_values[logical_and( history_values > 0, 
                                                                  type_code_values !=  DevelopmentEventTypeOfChange.DELETE)]
        mean_size = history_values_without_zeros.mean()
        idx = array( [], dtype="int32" )
        # Ensure that there are some development projects to choose from.
        num_of_projects_to_select = max( 10, round_( should_develop_units / mean_size ) )
        while True:
            idx = concatenate( ( idx, randint( 0, history_values_without_zeros.size,
                                                num_of_projects_to_select ) ) )
            csum = history_values_without_zeros[idx].cumsum()
            idx1 = idx[csum <= should_develop_units]
            if idx1.size == 0: # at least one project should be selected
                idx = array([idx[0]], dtype="int32")
            else:
                idx = idx1
            if csum[-1] >= should_develop_units:
                break
        data = {self.project_units[project_type]: history_values_without_zeros[idx],
                     "project_id": arange( idx.size ) + 1,
                     location_set.get_id_name()[0]: zeros( ( idx.size, ), dtype=int32)}
 
        storage = StorageFactory().get_storage('dict_storage')

        development_projects_table_name = 'development_projects'
        storage.write_table(table_name=development_projects_table_name, table_data=data)

        return DevelopmentProjectDataset(
            in_storage = storage,
            in_table_name = development_projects_table_name,
            resources = resources,
            what = project_type,
            attribute_name = self.project_units[project_type],
            )

    
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.tests.stochastic_test_case import StochasticTestCase


class DPTMTests(StochasticTestCase):

    def setUp( self ):
        self.storage = StorageFactory().get_storage('dict_storage')

        self.storage.write_table(
            table_name='development_event_history',
            table_data={
                "zone_id":arange( 1, 100+1 ),
                "scheduled_year":array( 100*[1999] ),
                "residential_units":array( 100*[50] ),
                "commercial_job_spaces":array( 100*[500] ),
                "industrial_job_spaces":array( 100*[500] ),
                }
            )
#            create 10 zones, each with 200 residential units and space for 100 commercial jobs,
#            and 100 industrial jobs
        self.storage.write_table(
            table_name='zones',
            table_data={
                "zone_id": arange( 1, 10+1 ),
                }
            )
        self.storage.write_table(
            table_name='pseudo_buildings',
            table_data={
                "pseudo_building_id": arange(1,31), # 1 building per building_type and zone
                "zone_id": array( [1,1,1, 2,2,2, 3,3,3, 4,4,4, 5,5,5, 6,6,6, 7,7,7, 8,8,8, 9,9,9, 10,10,10] ),
                "building_type_id": array(10*[1,2,3]),
                "residential_units": array(10*[200, 0, 0]),
                "commercial_job_spaces": array(10*[0,100,0]),
                "industrial_job_spaces": array(10*[0,0,100])
                }
            )
#            create 1000 households, 100 in each of the 10 zones.
#            there will initially be 100 vacant residential units in each zone.
        self.storage.write_table(
            table_name='households',
            table_data={
                "household_id":arange( 1, 1000+1 ),
                "zone_id":array( 100*range(1,11) )
                }
            )
        self.storage.write_table(
            table_name='job_building_types',
            table_data={
                "id":array([1,2,3]),
                "name": array(["home_based", "commercial", "industrial"]),
                "home_based": array([1, 0, 0])
                }
            )
#            create 250 commercial jobs and distribute them equally across the 10 zones,
#            25 commercial jobs/zone
        self.storage.write_table(
            table_name='jobs',
            table_data={
                "job_id":arange( 1, 250+1 ),
                "zone_id":array( 25*range(1,11) ),
                "home_based":array( 250*[0] ),
                "building_type":array(250*[2])
                }
            )

        self.dataset_pool = DatasetPool(package_order=['urbansim_zone', "urbansim"],
                                        storage=self.storage)

        self.compute_resources = Resources({
                    "commercial_vacant_variable": "urbansim_zone.zone.number_of_vacant_commercial_jobs",
                    "industrial_vacant_variable": "urbansim_zone.zone.number_of_vacant_industrial_jobs",
        })

    def test_no_development_with_zero_target_vacancy( self ):
        """If the target vacany ratest are 0%, then no development should occur and thus,
        the results returned (which represents development projects) should be empty.
        In fact anytime the target vacancy rate is strictly less than the current vacancy rate,
        then no development should ever occur.
        """

        """specify that the target vacancies for the year 2000 should be 0% for both
        residential and non-residential. with these constrains, no new development projects
        should be spawned for any set of agents."""
        self.storage.write_table(
            table_name='target_vacancies',
            table_data={
                "year":array( [2000] ),
                "target_total_residential_vacancy":array( [0.0] ),
                "target_total_commercial_vacancy":array( [0.0] ),
                "target_total_industrial_vacancy":array( [0.0] )
                }
            )

        dptm = DevelopmentProjectTransitionModel()
        results = dptm.run(self.dataset_pool.get_dataset('target_vacancy'),
                           self.dataset_pool.get_dataset('development_event_history'),
                           2000,
                           self.dataset_pool.get_dataset('zone'),
                           dataset_pool=self.dataset_pool,
                           resources=self.compute_resources)

        self.assertEqual( results['residential'], None,
                         "No residential units should've been added/developed" )
        self.assertEqual( results['commercial'], None,
                         "No commercial units should've been added/developed" )
        self.assertEqual( results['industrial'], None,
                         "No industrial units should've been added/developed" )

    def test_development_with_nonzero_target_vacancy_and_equal_history( self ):
        """Test basic cases, where current residential vacancy = 50%, target residential vacancy is 75%,
        current commercial vacancy is 75%, and target nonresidential vacancy is 50%.
        Residential development projects should occur, and none for nonresidential"""
        self.storage.write_table(
            table_name='target_vacancies',
            table_data={
                "year":array( [2001] ),
                "target_total_residential_vacancy":array( [0.75] ),
                "target_total_commercial_vacancy":array( [0.50] ),
                "target_total_industrial_vacancy":array( [0.50] )
                }
            )

        dptm = DevelopmentProjectTransitionModel()
        results = dptm.run(self.dataset_pool.get_dataset('target_vacancy'),
                           self.dataset_pool.get_dataset('development_event_history'),
                           2001,
                           self.dataset_pool.get_dataset('zone'),
                           dataset_pool=self.dataset_pool,
                           resources=self.compute_resources )

        """2000 residential units should've been added because current ratio of
        1000 unoccupied / 2000 total = 0.5, and target residential vacancy rate
        is 0.75. add 2000 to numerator and denominator, and 3000 / 4000 = 0.75"""
        number_of_new_residential_units = results['residential'].get_attribute( 'residential_units' ).sum()
        self.assertEqual( number_of_new_residential_units, 2000,
                         """Exactly 2000 residential units should've been added/developed.
                         Instead, got %s""" % ( number_of_new_residential_units, ) )

        """Anytime the target vacancy rate is less than the current vacancy rate,
        no new development should occur."""
        self.assertEqual( results['commercial'], None,
                         "No commercial units should've been added/developed." )

        self.assertEqual( results['industrial'], None,
                         "No industrial units should've been added/developed." )

    def test_development_with_99_percent_target_vacancy_and_equal_history( self ):
        """Not too different from the basic case above, just trying the other extreme.
        """
        self.storage.write_table(
            table_name='target_vacancies',
            table_data={
                "year":array( [2001] ),
                "target_total_residential_vacancy":array( [0.99] ),
                "target_total_commercial_vacancy":array( [0.99] ),
                "target_total_industrial_vacancy":array( [0.99] )
                }
            )

        dptm = DevelopmentProjectTransitionModel()
        results = dptm.run(self.dataset_pool.get_dataset('target_vacancy'),
                           self.dataset_pool.get_dataset('development_event_history'),
                           2001,
                           self.dataset_pool.get_dataset('zone'),
                           dataset_pool=self.dataset_pool,
                           resources=self.compute_resources)

        """2000 residential units should've been added because current ratio of
        1000 unoccupied / 2000 total = 0.5, and target residential vacancy rate
        is 0.75. add 2000 to numerator and denominator, and 3000 / 4000 = 0.75"""
        number_of_new_residential_units = results['residential'].get_attribute( 'residential_units' ).sum()
        self.assertEqual( number_of_new_residential_units, 98000,
                         """Approximately 98000 residential units should've been added/developed.
                         Instead, got %s""" % ( number_of_new_residential_units, ) )

        new_commercial_jobs = results['commercial'].get_attribute( 'commercial_job_spaces' ).sum()
        self.assertEqual( new_commercial_jobs, 24000,
                         """Approximately 24000 commercial jobs should've been added/developed.
                         Instead, got %s""" % ( new_commercial_jobs, ) )

        self.assertEqual( results['industrial'], None,
                         "No industrial units should've been added/developed." )

    def test_development_with_varied_history( self ):
        """Tests the effectiveness of events history in influencing the new projects' sizes.
        Creates 1000 industrial events in the history, and 999 of these added 300
        industrial jobs, and the last event added 5000 industrial jobs.
        """
        def run_model():
            storage = StorageFactory().get_storage('dict_storage')

            storage.write_table(
                table_name='target_vacancies',
                table_data={
                    "year":array( [2000] ),
                    "target_total_residential_vacancy":array( [0.75] ),
                    "target_total_commercial_vacancy":array( [0.90] ),
                    "target_total_industrial_vacancy":array( [0.90] )
                    }
                )
            storage.write_table(
                table_name='development_event_history',
                table_data={
                    "zone_id":array( 10*range( 1, 100+1 ) ),
                    "scheduled_year":array( 1000*[1999] ),
                    "residential_units":array( 1000*[50] ),
                    "commercial_job_spaces":array( 1000*[500] ),
                    "industrial_job_spaces":array( 999*[300] + [5000] ),
                    }
                )
            storage.write_table(
                table_name='jobs',
                table_data={
                    "job_id":arange( 1, 250+1 ),
                    "zone_id":array( 25*range( 1, 10+1 ) ),
                    "home_based":array( 250*[0] ),
                    "building_type":array( 250*[3] )
                    }
                )

            dataset_pool = DatasetPool(package_order=['urbansim_zone', 'urbansim'],
                                       storage=storage)
            dataset_pool.add_datasets_if_not_included({'job_building_type': self.dataset_pool.get_dataset('job_building_type'),
                                                       'zone': self.dataset_pool.get_dataset('zone'),
                                                       'household': self.dataset_pool.get_dataset('household'),
                                                       'pseudo_building':self.dataset_pool.get_dataset('pseudo_building')
                                                      })
            dptm = DevelopmentProjectTransitionModel()
            results = dptm.run(dataset_pool.get_dataset('target_vacancy'),
                               dataset_pool.get_dataset('development_event_history'),
                               2000,
                               dataset_pool.get_dataset('zone'),
                               dataset_pool = dataset_pool,
                               resources = self.compute_resources
                       )
            self.assertEqual( results['commercial'], None,
                             "No commercial_sqft should've been added/developed." )
            return results

        def number_of_new_residential_units_from_model():
            results = run_model()
            return array(results['residential'].get_attribute( 'residential_units' ).sum())

        self.run_stochastic_test(__file__, number_of_new_residential_units_from_model, array([2000]), 10)

        def new_industrial_sqft_from_model():
            results = run_model()
            return array(results['industrial'].get_attribute( 'industrial_job_spaces' ).sum())

        self.run_stochastic_test(__file__, new_industrial_sqft_from_model, array([1500]), 10)

    def test_development_with_equal_history( self ):
        """Tests development with both commercial and industrial jobs occupying equal amounts of space
        in each zone, but the even history for each job type is different -
        1000 events adding 50 industrial jobs, and 1000 events adding 500 commercial jobs.
        Check the number of projects and jobs for each job type.
        """
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='target_vacancies',
            table_data={
                "year":array( [2000] ),
                "target_total_residential_vacancy":array( [0.75] ),
                "target_total_commercial_vacancy":array( [0.90] ),
                "target_total_industrial_vacancy":array( [0.80] )
            }
        )
        storage.write_table(
            table_name='development_event_history',
            table_data={
                "zone_id":array( 10*range( 1, 100+1 ) ),
                "scheduled_year":array( 1000*[1999] ),
                "residential_units":array( 1000*[50] ),
                "commercial_job_spaces":array( 1000*[500] ),
                "industrial_job_spaces":array( 1000*[50] ),
            }
        )
        storage.write_table(
            table_name='jobs',
            table_data={
                "job_id":arange( 1, 500+1 ),
                "zone_id":array( 50*range( 1, 10+1 ) ),
                "home_based":array( 500*[0] ),
                "building_type":array( 250*[3] + 250*[2] )
            }
        )

        dataset_pool = DatasetPool(package_order=['urbansim_zone', 'urbansim'],
                                   storage=storage)
        dataset_pool.add_datasets_if_not_included({'job_building_type': self.dataset_pool.get_dataset('job_building_type'),
                                                       'zone': self.dataset_pool.get_dataset('zone'),
                                                       'household': self.dataset_pool.get_dataset('household'),
                                                       'pseudo_building':self.dataset_pool.get_dataset('pseudo_building')
                                                      })

        dptm = DevelopmentProjectTransitionModel()
        results = dptm.run(dataset_pool.get_dataset('target_vacancy'),
                           dataset_pool.get_dataset('development_event_history'),
                           2000,
                           dataset_pool.get_dataset('zone'),
                           dataset_pool=dataset_pool,
                           resources=self.compute_resources
                           )

        number_of_new_residential_units = results['residential'].get_attribute( 'residential_units' ).sum()
        self.assertEqual( number_of_new_residential_units, 2000,
                         """Approximately 2000 residential units should've been added/developed.
                         Instead, got %s""" % ( number_of_new_residential_units, ) )

        new_commercial_jobs = results['commercial'].get_attribute( 'commercial_job_spaces' ).sum()
        self.assertEqual( new_commercial_jobs, 1500,
                         """Approximately 1500 commercial jobs should've been added/developed.
                         Instead, got %s""" % ( new_commercial_jobs, ) )

        number_of_new_commercial_projects = results['commercial'].get_attribute( 'commercial_job_spaces' ).size
        self.assertEqual( number_of_new_commercial_projects, 3,
                         """Approximately 3 commercial projects should've been added/developed.
                         Instead, got %s""" % ( number_of_new_commercial_projects, ) )

        number_of_new_industrial_projects = results['industrial'].get_attribute( 'industrial_job_spaces' ).size
        self.assertEqual( number_of_new_industrial_projects, 5,
                         """Approximately 5 industrial projects should've been added/developed.
                         Instead, got %s""" % ( number_of_new_industrial_projects, ) )

        new_industrial_jobs = results['industrial'].get_attribute( 'industrial_job_spaces' ).sum()
        self.assertEqual( new_industrial_jobs, 250,
                         """Approximately 250 industrial jobs should've been added/developed.
                         Instead, got %s""" % ( new_industrial_jobs, ) )

if __name__=="__main__":
    opus_unittest.main()

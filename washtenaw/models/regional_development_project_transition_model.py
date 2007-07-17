#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from opus_core.resources import Resources
from opus_core.misc import unique_values
from opus_core.logger import logger
from numpy import arange, array, where
from opus_core.datasets.dataset import DatasetSubset
from urbansim.models.development_project_transition_model import DevelopmentProjectTransitionModel

class RegionalDevelopmentProjectTransitionModel( DevelopmentProjectTransitionModel ):
    """
    It runs the urbansim development transition model for each large area.
    """
    model_name = "Regional Development Project Transition Model"
    
    def run( self, model_configuration, vacancy_table, history_table, year, location_set, resources=None ):
        large_area_ids = vacancy_table.get_attribute("large_area_id")
        locations_large_area_ids = location_set.compute_variables("washtenaw.%s.large_area_id" % location_set.get_dataset_name())
        unique_large_areas = unique_values(large_area_ids)
        self._compute_vacancy_variables(location_set, model_configuration, resources)

        projects = {}
        for area in unique_large_areas:
            location_index = where(locations_large_area_ids == area)[0]
            locations_for_this_area = DatasetSubset(location_set, location_index)
            target_residential_vacancy_rate, target_non_residential_vacancy_rate = self._get_target_vacancy_rates(vacancy_table, year, area)
            for project_type in model_configuration['development_project_types']:
                # determine current-year vacancy rates
                vacant_units_sum = locations_for_this_area.get_attribute(self.variable_for_vacancy[project_type]).sum()
                units_sum = float( locations_for_this_area.get_attribute(self.units_variable[project_type]).sum() )
                vacant_rate = self.safe_divide(vacant_units_sum, units_sum)
                if model_configuration['development_project_types'][project_type]['residential']:
                    target_vacancy_rate = target_residential_vacancy_rate
                else:
                    target_vacancy_rate = target_non_residential_vacancy_rate
                should_develop_units = int(round(max( 0, ( target_vacancy_rate * units_sum - vacant_units_sum ) /
                                             ( 1 - target_vacancy_rate ) )))
                #logger.log_status(project_type + ": vacant units: %d, should be vacant: %f, sum units: %d"
                #              % (vacant_units_sum, target_vacancy_rate * units_sum, units_sum))
    
                #if not should_develop_units:
                #    logger.log_note(("Will not build any " + project_type + " units, because the current vacancy of %d units\n"
                #                 + "is more than the %d units desired for the vacancy rate of %f.")
                #                % (vacant_units_sum,
                #                   target_vacancy_rate * units_sum,
                #                   target_vacancy_rate))
                #create projects
                if should_develop_units > 0:
                    project_dataset = self._create_projects(should_develop_units, project_type, history_table,
                                                                   locations_for_this_area, units_sum, model_configuration, 
                                                                   resources)
                    if (project_type not in projects.keys()) or (projects[project_type] is None):
                        projects[project_type] = project_dataset
                        projects[project_type].add_submodel_categories()
                    else:
                        projects[project_type].join_by_rows(project_dataset, change_ids_if_not_unique=True)
 
        for project_type in model_configuration['development_project_types']:
            if project_type not in projects.keys():
                projects[project_type] = None
            if projects[project_type] is None:
                size = 0
            else:
                size = projects[project_type].size()
            logger.log_status("%s %s projects to be built" % (size, project_type))  
        return projects

    def _get_target_vacancy_rates(self, vacancy_table, year, large_area):
        vacancy_table.get_attribute( "target_total_residential_vacancy" ) # assure that those attributes are loaded
        vacancy_table.get_attribute( "target_total_non_residential_vacancy" )
        target_residential_vacancy_rate = vacancy_table.get_data_element_by_id( (year, large_area) ).target_total_residential_vacancy
        target_non_residential_vacancy_rate = vacancy_table.get_data_element_by_id( (year, large_area) ).target_total_non_residential_vacancy
        return target_residential_vacancy_rate, target_non_residential_vacancy_rate
    

    
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from opus_core.tests.stochastic_test_case import StochasticTestCase

from urbansim.constants import Constants


class DPTMTests(StochasticTestCase):

    def setUp( self ):
        """specify the development event history for the gridcells. here, we simulate 50 residential units
        and 5000 commercial, industrial, and governmental sqft added to each of the gridcells in previous years.
        Also, we specify $1000 in value added to each gridcell for residential, commercial, industrial, governmental.
        These values are so boring because they really don't matter for this test case, where there will be absolutely
        no development, and thus, nothing will be sampled from the development_history"""
        self.storage = StorageFactory().get_storage('dict_storage')

        self.storage._write_dataset(
            'development_event_history',
            {
                "grid_id":arange( 1, 100+1 ),
                "scheduled_year":array( 100*[1999] ),
                "residential_units":array( 100*[50] ),
                "commercial_sqft":array( 100*[5000] ),
                "industrial_sqft":array( 100*[5000] ),
                "governmental_sqft":array( 100*[5000] ),
                "residential_improvement_value":array( 100*[1000] ),
                "commercial_improvement_value":array( 100*[1000] ),
                "industrial_improvement_value":array( 100*[1000] ),
                "governmental_improvement_value":array( 100*[1000] )
                }
            )
        self.storage._write_dataset(
            'gridcells',
#            create 100 gridcells, each with 200 residential units and space for 100 commercial jobs,
#            100 industrial jobs, and residential, industrial, and commercial value at $500,000 each
            {
                "grid_id": arange( 1, 100+1 ),
                "residential_units":array( 100*[200] ),
                "commercial_sqft":array( 100*[10000] ),
                "commercial_sqft_per_job":array( 100*[100] ),
                "industrial_sqft":array( 100*[10000] ),
                "industrial_sqft_per_job":array( 100*[100] ),
                "residential_improvement_value":array( 100*[500000] ),
                "commercial_improvement_value":array( 100*[500000] ),
                "industrial_improvement_value":array( 100*[500000] ),
                "large_area_id": array(50*[1] + 50*[2])
                }
            )
        self.storage._write_dataset(
            'households',
#            create 10000 households, 100 in each of the 100 gridcells.
#            there will initially be 100 vacant residential units in each gridcell then.
            {
                "household_id":arange( 1, 10000+1 ),
                "grid_id":array( 100*range( 1, 100+1 ) )
                }
            )
        self.storage._write_dataset(
            'job_building_types',
            {
                "id":array([Constants._governmental_code,
                            Constants._commercial_code,
                            Constants._industrial_code,
                            Constants._residential_code]),
                "name": array(["governmental", "commercial", "industrial", "home_based"]),
                "home_based": array([0, 0, 0, 1])
                }
            )
        self.storage._write_dataset(
#            create 2500 commercial jobs and distribute them equally across the 100 gridcells,
#            25 commercial jobs/gridcell
            'jobs',
            {
                "job_id":arange( 1, 2500+1 ),
                "grid_id":array( 25*range( 1, 100+1 ) ),
                "sector_id":array( 2500*[1] ),
                "home_based":array( 2500*[0] ),
                "building_type":array(2500*[Constants._commercial_code])
                }
            )
        self.storage._write_dataset(
            'urbansim_constants',
            {
                "acres": array([105.0]),
            }
        )

        self.dataset_pool = DatasetPool(package_order=['washtenaw', 'urbansim'],
                                        storage=self.storage)

        self.compute_resources = Resources({
            "household": self.dataset_pool.get_dataset('household'),
            "job": self.dataset_pool.get_dataset('job'),
            "job_building_type": self.dataset_pool.get_dataset('job_building_type'),
            'urbansim_constant': self.dataset_pool.get_dataset('urbansim_constant'),
        })

        from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
        self.model_configuration = AbstractUrbansimConfiguration()['models_configuration']

    def test_no_development_with_zero_target_vacancy( self ):
        """If the target vacany ratest are 0%, then no development should occur and thus,
        the results returned (which represents development projects) should be empty.
        """

        """specify that the target vacancies for the year 2000 should be 0% for both
        residential and non-residential, for 2 large areas. With these constrains, no new development projects
        should be spawned for any set of agents."""
        self.storage._write_dataset(
            'target_vacancies',
            {
                "year":array( [2000, 2000] ),
                "target_total_residential_vacancy":array( [0.0, 0] ),
                "target_total_non_residential_vacancy":array( [0.0, 0] ),
                "large_area_id": array([1,2])
                }
            )

        dptm = RegionalDevelopmentProjectTransitionModel()
        results = dptm.run(self.model_configuration,
                           self.dataset_pool.get_dataset('target_vacancy'),
                           self.dataset_pool.get_dataset('development_event_history'),
                           2000,
                           self.dataset_pool.get_dataset('gridcell'),
                           resources=self.compute_resources)

        self.assertEqual( results['residential'], None,
                         "No residential units should've been added/developed" )
        self.assertEqual( results['commercial'], None,
                         "No commercial units should've been added/developed" )
        self.assertEqual( results['industrial'], None,
                         "No industrial units should've been added/developed" )

    def test_development_with_nonzero_target_vacancy_and_equal_history( self ):
        """Test basic cases, where current residential vacancy = 50%, target residential vacancy is 75%,
        current non_residential vacancy is 75% (commercial), and target nonresidential vacancy is 50%.
        Residential development projects should occur in area 1, and none for nonresidential"""
        self.storage._write_dataset(
            'target_vacancies',
            {
                "year":array( [2001, 2001] ),
                "target_total_residential_vacancy":array( [0.75, 0] ),
                "target_total_non_residential_vacancy":array( [0.50, 0] ),
                "large_area_id": array([1,2])
                }
            )

        dptm = RegionalDevelopmentProjectTransitionModel()
        results = dptm.run(self.model_configuration,
                           self.dataset_pool.get_dataset('target_vacancy'),
                           self.dataset_pool.get_dataset('development_event_history'),
                           2001,
                           self.dataset_pool.get_dataset('gridcell'),
                           resources=self.compute_resources )

        """10000 residential units should've been added because current ratio of
        5000 unoccupied / 10000 total = 0.5, and target residential vacancy rate
        is 0.75. add 10000 to numerator and denominator, and 15000 / 20000 = 0.75"""
        number_of_new_residential_units = results['residential'].get_attribute( 'residential_units' ).sum()
        self.assertEqual( number_of_new_residential_units, 10000,
                         """Exactly 10000 residential units should've been added/developed.
                         Instead, got %s""" % ( number_of_new_residential_units, ) )

        """Anytime the target vacancy rate is less than the current vacancy rate,
        no new development should occur."""
        self.assertEqual( results['commercial'], None,
                         "No commercial units should've been added/developed." )

        self.assertEqual( results['industrial'], None,
                         "No industrial units should've been added/developed." )

    def xtest_development_with_99_percent_target_vacancy_and_equal_history( self ):
        """Not too different from the basic case above, just trying the other extreme.
        Notice that a 100% target vacancy rate doesn't really make sense and is not possible unless
        the current vacancy rate is also 100% (also not feasible)."""
        self.storage._write_dataset(
            'target_vacancies',
            {
                "year":array( [2001] ),
                "target_total_residential_vacancy":array( [0.99] ),
                "target_total_non_residential_vacancy":array( [0.99] )
                }
            )

        dptm = DevelopmentProjectTransitionModel()
        results = dptm.run(self.model_configuration,
                           self.dataset_pool.get_dataset('target_vacancy'),
                           self.dataset_pool.get_dataset('development_event_history'),
                           2001,
                           self.dataset_pool.get_dataset('gridcell'),
                           resources=self.compute_resources)

        """20000 residential units should've been added because current ratio of
        10000 unoccupied / 20000 total = 0.5, and target residential vacancy rate
        is 0.75. add 20000 to numerator and denominator, and 30000 / 40000 = 0.75"""
        number_of_new_residential_units = results['residential'].get_attribute( 'residential_units' ).sum()
        self.assertEqual( number_of_new_residential_units, 980000,
                         """Approximately 980000 residential units should've been added/developed.
                         Instead, got %s""" % ( number_of_new_residential_units, ) )

        new_commercial_sqft = results['commercial'].get_attribute( 'commercial_sqft' ).sum()
        self.assertEqual( new_commercial_sqft, 24000000,
                         """Approximately 24000000 commercial sqft should've been added/developed.
                         Instead, got %s""" % ( new_commercial_sqft, ) )

        self.assertEqual( results['industrial'], None,
                         "No industrial units should've been added/developed." )

    def xtest_development_with_varied_history( self ):
        """Tests the effectiveness of events history in influencing the new projects' sizes.
        Creates 1000 industrial events in the history, and 999 of these added 6000
        industrial sqft, and the last event added 500000 industrial sqft.
        Since the target vacancy rate is 90%, we estimate approximately 250 industrial projects
        to be spawned, each adding 6000 industrial sqft (to match the history).
        (7500 * 100 + 6000*250) / (10000 * 100.0 + 6000*250)
        """
        def run_model():
            storage = StorageFactory().get_storage('dict_storage')

            storage._write_dataset(
                'target_vacancies',
                {
                    "year":array( [2000] ),
                    "target_total_residential_vacancy":array( [0.75] ),
                    "target_total_non_residential_vacancy":array( [0.90] )
                    }
                )
            storage._write_dataset(
                'development_event_history',
                {
                    "grid_id":array( 10*range( 1, 100+1 ) ),
                    "scheduled_year":array( 1000*[1999] ),

                    "residential_units":array( 1000*[50] ),
                    "commercial_sqft":array( 1000*[5000] ),
                    "industrial_sqft":array( 999*[6000] + [500000] ),
                    "governmental_sqft":array( 1000*[5000] ),

                    "residential_improvement_value":array( 1000*[1000] ),
                    "commercial_improvement_value":array( 1000*[1000] ),
                    "industrial_improvement_value":array( 1000*[20000] ),
                    "governmental_improvement_value":array( 1000*[1000] )
                    }
                )
            storage._write_dataset(
                'gridcells',
                {
                    "grid_id": arange( 1, 100+1 ),
                    "residential_units":array( 100*[200] ),
                    "commercial_sqft":array( 100*[10000] ),
                    "commercial_sqft_per_job":array( 100*[100] ),
                    "industrial_sqft":array( 100*[10000] ),
                    "industrial_sqft_per_job":array( 100*[100] ),
                    "residential_improvement_value":array( 100*[500000] ),
                    "commercial_improvement_value":array( 100*[500000] ),
                    "industrial_improvement_value":array( 100*[500000] )
                    }
                )
            storage._write_dataset(
                'households',
                {
                    "household_id":arange( 1, 10000+1 ),
                    "grid_id":array( 100*range( 1, 100+1 ) )
                    }
                )
            storage._write_dataset(
                'jobs',
                {
                    "job_id":arange( 1, 2500+1 ),
                    "grid_id":array( 25*range( 1, 100+1 ) ),
                    "sector_id":array( 2500*[1] ),
                    "home_based":array( 2500*[0] ),
                    "building_type":array( 2500*[Constants._industrial_code] )
                    }
                )

            dataset_pool = DatasetPool(package_order=['urbansim'],
                                       storage=storage)
            dptm = DevelopmentProjectTransitionModel()
            results = dptm.run(self.model_configuration,
                               dataset_pool.get_dataset('target_vacancy'),
                               dataset_pool.get_dataset('development_event_history'),
                               2000,
                               self.dataset_pool.get_dataset('gridcell'),
                               resources=Resources({"household":dataset_pool.get_dataset('household'),
                                                    "job":dataset_pool.get_dataset('job'),
                                                    "job_building_type": self.dataset_pool.get_dataset('job_building_type'),
                                                    'urbansim_constant':self.dataset_pool.get_dataset('urbansim_constant')}) )
            self.assertEqual( results['commercial'], None,
                             "No commercial_sqft should've been added/developed." )
            return results

        def number_of_new_residential_units_from_model():
            results = run_model()
            return array(results['residential'].get_attribute( 'residential_units' ).sum())

        self.run_stochastic_test(__file__, number_of_new_residential_units_from_model, array([20000]), 10)

        def new_industrial_sqft_from_model():
            results = run_model()
            return array(results['industrial'].get_attribute( 'industrial_sqft' ).sum())

        #self.run_stochastic_test(__file__, new_industrial_sqft_from_model, array([1500000]), 10)

    def xtest_development_with_equal_history( self ):
        """Tests development with both commercial and industrial jobs occupying equal amounts of space
        in each gridcell, but the even history for each job type is different -
        1000 events adding 6000 industrial sqft., and 1000 events adding 5000 commercial sqft.
        The total sqft. added for each job type should be the same (1500000 sqft.), but the number of
        projects and sqft./project should be different for each job type
        """
        storage = StorageFactory().get_storage('dict_storage')

        storage._write_dataset(
            'target_vacancies',
            {
                "year":array( [2000] ),
                "target_total_residential_vacancy":array( [0.75] ),
                "target_total_non_residential_vacancy":array( [0.90] )
            }
        )
        storage._write_dataset(
            'development_event_history',
            {
                "grid_id":array( 10*range( 1, 100+1 ) ),
                "scheduled_year":array( 1000*[1999] ),

                "residential_units":array( 1000*[50] ),
                "commercial_sqft":array( 1000*[5000] ),
                "industrial_sqft":array( 1000*[6000] ),
                "governmental_sqft":array( 1000*[5000] ),

                "residential_improvement_value":array( 1000*[1000] ),
                "commercial_improvement_value":array( 1000*[1000] ),
                "industrial_improvement_value":array( 1000*[20000] ),
                "governmental_improvement_value":array( 1000*[1000] )
            }
        )
        storage._write_dataset(
            'gridcells',
            {
                "grid_id": arange( 1, 100+1 ),
                "residential_units":array( 100*[200] ),
                "commercial_sqft":array( 100*[10000] ),
                "commercial_sqft_per_job":array( 100*[100] ),
                "industrial_sqft":array( 100*[10000] ),
                "industrial_sqft_per_job":array( 100*[100] ),
                "residential_improvement_value":array( 100*[500000] ),
                "commercial_improvement_value":array( 100*[500000] ),
                "industrial_improvement_value":array( 100*[500000] )
            }
        )
        storage._write_dataset(
            'households',
            {
                "household_id":arange( 1, 10000+1 ),
                "grid_id":array( 100*range( 1, 100+1 ) )
            }
        )
        storage._write_dataset(
            'jobs',
            {
                "job_id":arange( 1, 5000+1 ),
                "grid_id":array( 50*range( 1, 100+1 ) ),
                "sector_id":array( 5000*[1] ),
                "home_based":array( 5000*[0] ),
                "building_type":array( 2500*[Constants._industrial_code]
                                       + 2500*[Constants._commercial_code] )
            }
        )

        dataset_pool = DatasetPool(package_order=['urbansim'],
                                   storage=storage)

        dptm = DevelopmentProjectTransitionModel()
        results = dptm.run(self.model_configuration,
                           dataset_pool.get_dataset('target_vacancy'),
                           dataset_pool.get_dataset('development_event_history'),
                           2000,
                           dataset_pool.get_dataset('gridcell'),
                           resources=Resources({"household":dataset_pool.get_dataset('household'),
                                                "job":dataset_pool.get_dataset('job'),
                                                "job_building_type": self.dataset_pool.get_dataset('job_building_type'),
                                                'urbansim_constant':self.dataset_pool.get_dataset('urbansim_constant')}) )

        number_of_new_residential_units = results['residential'].get_attribute( 'residential_units' ).sum()
        self.assertEqual( number_of_new_residential_units, 20000,
                         """Approximately 20000 residential units should've been added/developed.
                         Instead, got %s""" % ( number_of_new_residential_units, ) )

        new_commercial_sqft = results['commercial'].get_attribute( 'commercial_sqft' ).sum()
        self.assertEqual( new_commercial_sqft, 1500000,
                         """Approximately 1500000 commercial sqft should've been added/developed.
                         Instead, got %s""" % ( new_commercial_sqft, ) )

        number_of_new_commercial_projects = results['commercial'].get_attribute( 'commercial_sqft' ).size
        self.assertEqual( number_of_new_commercial_projects, 300,
                         """Approximately 299 commercial sqft should've been added/developed.
                         Instead, got %s""" % ( number_of_new_commercial_projects, ) )

        number_of_new_industrial_projects = results['industrial'].get_attribute( 'industrial_sqft' ).size
        self.assertEqual( number_of_new_industrial_projects, 250,
                         """Approximately 249 industrial sqft should've been added/developed.
                         Instead, got %s""" % ( number_of_new_industrial_projects, ) )

        new_industrial_sqft = results['industrial'].get_attribute( 'industrial_sqft' ).sum()
        self.assertEqual( new_industrial_sqft, 1500000,
                         """Approximately 1500000 industrial sqft should've been added/developed.
                         Instead, got %s""" % ( new_industrial_sqft, ) )

if __name__=="__main__":
    opus_unittest.main()
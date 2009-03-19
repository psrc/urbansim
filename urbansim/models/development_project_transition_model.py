# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.resources import Resources
from opus_core.misc import DebugPrinter
from opus_core.storage_factory import StorageFactory
from urbansim.datasets.development_project_dataset import DevelopmentProjectDataset
from urbansim.datasets.development_event_dataset import DevelopmentEventTypeOfChange
from opus_core.model import Model
from numpy.random import randint #@UnresolvedImport
from opus_core.logger import logger
from numpy import arange, array, zeros, ones, float32, int32, concatenate, logical_and #@UnresolvedImport

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
    
    def __init__( self, debuglevel=0 ):
        self.debug = DebugPrinter( debuglevel )

    def pre_check( self, location_set, vacancy_table, types ):
        for type in types:
            self.check_for_space( location_set.get_attribute( types[type]["units"] ) )
        self.check_target_vacancy_is_not_100_percent( vacancy_table.get_attribute( "target_total_residential_vacancy" ) )
        self.check_target_vacancy_is_not_100_percent( vacancy_table.get_attribute( "target_total_non_residential_vacancy" ) )

    def check_for_space( self, values ):
        """Check that this array of values sums to something > 0."""
        self.do_check( "x > 0", array( [values.sum()] ) )

    def check_target_vacancy_is_not_100_percent( self, value ):
        """Check that the target vacancy rate is not 100% (ratio == 1), because it doesn't make sense,
        and it also causes a divide by 0 error."""
        self.do_check( "x != 1", value )

    #TODO: there should be a check that the years and grid ids in dev. event history are unique (one gridcell can only have one event/year)

    def safe_divide(self, numerator, denominator, return_value_if_denominator_is_zero=0, type=float):
        """If denominator == 0, return return_value_if_denominator_is_zero.
        Else return numerator / denominator.
        """
        if denominator == 0:
            return return_value_if_denominator_is_zero
        return type(numerator) / denominator

    def run(self, vacancy_table, history_table, year, 
             location_set, resources = None,  development_models = None, 
             models_configuration = None, model_configuration = None):
        """
        Defining the development project types can be done in two ways;
        either by using a small part of configuration located under
        'development_project_types' that lists only the needed information
        OR: they can be defined as part of the development project models.
        Configurations that pass the development_models argument assume to 
        use the latter method.
        """
        # check that we get the correct arguments
        if development_models is not None and models_configuration is None:
            raise StandardError('Configurations that pass a list of development'
                                ' models (argument: "development_models") must '
                                'also pass a reference to the entire models '
                                'configuration (argument: "models_'
                                'configuration") note: plural model[s].')

        dev_model_configs = {}
        if development_models is None: # assume this means that we use old conf
            # try to get a reference to the external information for development
            # project types
            try:
                dev_model_configs = model_configuration['development_project_types']
            except:
                dev_model_configs = models_configuration['development_project_types']
        else:
            # pull in information from the specified development project models
            for dev_proj_model in development_models:
                model_conf = models_configuration[dev_proj_model]
                proj_type = model_conf['controller']['init']['arguments']['project_type'].strip('\'"')
                dev_model_configs[proj_type] = {}
                dev_model_configs[proj_type]['units'] = model_conf['controller']['init']['arguments']['units'].strip('\'"')
                dev_model_configs[proj_type]['residential'] = model_conf['controller']['init']['arguments']['residential']
                dev_model_configs[proj_type]['categories'] = model_conf['controller']['prepare_for_estimate']['arguments']['categories']

        self.pre_check( location_set, vacancy_table, dev_model_configs)
        target_residential_vacancy_rate, target_non_residential_vacancy_rate = self._get_target_vacancy_rates(vacancy_table, year)
        self._compute_vacancy_variables(location_set, dev_model_configs, resources)
        projects = {}
        for project_type in dev_model_configs:
            # determine current-year vacancy rates
            vacant_units_sum = location_set.get_attribute(self.variable_for_vacancy[project_type]).sum()
            units_sum = float( location_set.get_attribute(self.units_variable[project_type]).sum() )
            if dev_model_configs[project_type]['residential']:
                target_vacancy_rate = target_residential_vacancy_rate
            else:
                target_vacancy_rate = target_non_residential_vacancy_rate
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
                                                               location_set, units_sum, dev_model_configs, resources)
                projects[project_type].add_submodel_categories()
            else:
                projects[project_type] = None
        return projects

    def _get_target_vacancy_rates(self, vacancy_table, year):
        target_residential_vacancy_rate = vacancy_table.get_data_element_by_id( year ).target_total_residential_vacancy
        target_non_residential_vacancy_rate = vacancy_table.get_data_element_by_id( year ).target_total_non_residential_vacancy
        return target_residential_vacancy_rate, target_non_residential_vacancy_rate
    
    def _compute_vacancy_variables(self, location_set, dev_model_configs, resources):
        compute_resources = Resources(resources)
        compute_resources.merge({"debug":self.debug})
        self.units_variable = {}
        self.variable_for_vacancy = {}
        for project_type in dev_model_configs:
            self.units_variable[project_type] =  dev_model_configs[project_type]['units']
            self.variable_for_vacancy[project_type] = compute_resources.get(
                                    "%s_vacant_variable" % project_type,
                                    "urbansim.%s.vacant_%s" % (location_set.get_dataset_name(),
                                                                     self.units_variable[project_type]))
            location_set.compute_variables([self.variable_for_vacancy[project_type]],
                                        resources = compute_resources)
            
    def _create_projects(self, should_develop_units, project_type, history_table, location_set, units_sum, dev_model_configs,
                         resources=None):
        average_improvement_value = None
        if (project_type+"_improvement_value") in location_set.get_known_attribute_names():
            average_improvement_value = self.safe_divide(
                location_set.get_attribute(project_type+"_improvement_value" ).sum(), units_sum)
        categories = dev_model_configs[project_type]['categories']
        history_values = history_table.get_attribute(self.units_variable[project_type])
        type_code_values = history_table.get_change_type_code_attribute(self.units_variable[project_type])
        # take only non-zero history values and those that don't represent demolished buildings 
        history_values_without_zeros = history_values[logical_and( history_values > 0, 
                                                                  type_code_values !=  DevelopmentEventTypeOfChange.DELETE)]
        #TODO: what happens if history has only zeroes?
        mean_size = history_values_without_zeros.mean()
        idx = array( [], dtype="int32" )
        # Ensure that there are some development projects to choose from.
        #TODO: should the 'int' in the following line be 'ceil'?
        num_of_projects_to_select = max( 10, int( should_develop_units / mean_size ) )
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
        data = {self.units_variable[project_type]: history_values_without_zeros[idx],
                     "project_id": arange( idx.size ) + 1,
                     location_set.get_id_name()[0]: zeros( ( idx.size, ), dtype=int32)}
        if average_improvement_value is not None:
            data["improvement_value"] = (ones( ( idx.size, ))*average_improvement_value).astype(float32)

        storage = StorageFactory().get_storage('dict_storage')

        development_projects_table_name = 'development_projects'
        storage.write_table(table_name=development_projects_table_name, table_data=data)

        return DevelopmentProjectDataset(
            in_storage = storage,
            in_table_name = development_projects_table_name,
            categories = categories,
            resources = resources,
            what = project_type,
            attribute_name = self.units_variable[project_type],
            )

    
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
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

        self.storage.write_table(
            table_name='development_event_history',
            table_data={
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
#            create 100 gridcells, each with 200 residential units and space for 100 commercial jobs,
#            100 industrial jobs, and residential, industrial, and commercial value at $500,000 each
        self.storage.write_table(
            table_name='gridcells',
            table_data={
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
#            create 10000 households, 100 in each of the 100 gridcells.
#            there will initially be 100 vacant residential units in each gridcell then.
        self.storage.write_table(
            table_name='households',
            table_data={
                "household_id":arange( 1, 10000+1 ),
                "grid_id":array( 100*range( 1, 100+1 ) )
                }
            )
        self.storage.write_table(
            table_name='job_building_types',
            table_data={
                "id":array([Constants._governmental_code,
                            Constants._commercial_code,
                            Constants._industrial_code,
                            Constants._residential_code]),
                "name": array(["governmental", "commercial", "industrial", "home_based"]),
                "home_based": array([0, 0, 0, 1])
                }
            )
#            create 2500 commercial jobs and distribute them equally across the 100 gridcells,
#            25 commercial jobs/gridcell
        self.storage.write_table(
            table_name='jobs',
            table_data={
                "job_id":arange( 1, 2500+1 ),
                "grid_id":array( 25*range( 1, 100+1 ) ),
                "sector_id":array( 2500*[1] ),
                "home_based":array( 2500*[0] ),
                "building_type":array(2500*[Constants._commercial_code])
                }
            )
        self.storage.write_table(
            table_name='urbansim_constants',
            table_data={
                "acres": array([105.0]),
            }
        )

        self.dataset_pool = DatasetPool(package_order=['urbansim'],
                                        storage=self.storage)

        self.compute_resources = Resources({
            "household": self.dataset_pool.get_dataset('household'),
            "job": self.dataset_pool.get_dataset('job'),
            "job_building_type": self.dataset_pool.get_dataset('job_building_type'),
            'urbansim_constant': self.dataset_pool.get_dataset('urbansim_constant'),
        })

        #
        # ? dynamically get these datasets?
        # Replace uses of 'constants' with 'urbansim_constant'?
        #

        from urbansim.configs.base_configuration import AbstractUrbansimConfiguration
        # fake development project models
                
        #dev_models = {
           #'residential_model':{
                #'controller':{
                    #'init':{
                        #'arguments':{
                            #'project_type':'residential',
                            #'residential':True,
                            #'units':'residential_units'
                        #}
                    #},
                    #'prepare_for_estimate':{
                        #'arguments':{
                            #'categories':[1, 2, 3, 5, 10, 20]
                        #}
                    #}
                #}
            #},
            #'commercial_model':{
                #'controller':{
                    #'init':{
                        #'arguments':{
                            #'project_type':'commercial',
                            #'residential':False,
                            #'units': 'commercial_sqft'
                        #}
                    #},
                    #'prepare_for_estimate':{
                        #'arguments': {
                            #'categories':[1000, 2000, 5000, 10000]
                        #}
                    #}
                #}
            #},
            #'industrial_model':{
                #'controller':{
                    #'init':{
                        #'arguments':{
                            #'project_type':'industrial',
                            #'residential':False,
                            #'units':'industrial_sqft'
                        #}
                    #},
                    #'prepare_for_estimate':{
                        #'arguments':{
                            #'categories':[1000, 2000, 5000, 10000]
                        #}
                    #}
                    
                #}
            #}
        #}

        self.models_configuration = AbstractUrbansimConfiguration()['models_configuration']

    def test_no_development_with_zero_target_vacancy( self ):
        """If the target vacany ratest are 0%, then no development should occur and thus,
        the results returned (which represents development projects) should be empty.
        In fact anytime the target vacancy rate is strictly less than the current vacancy rate,
        then no development should ever occur... and no, there is no eviction :-)
        """

        """specify that the target vacancies for the year 2000 should be 0% for both
        residential and non-residential. with these constrains, no new development projects
        should be spawned for any set of agents."""
        self.storage.write_table(
            table_name='target_vacancies',
            table_data={
                "year":array( [2000] ),
                "target_total_residential_vacancy":array( [0.0] ),
                "target_total_non_residential_vacancy":array( [0.0] )
                }
            )

        dptm = DevelopmentProjectTransitionModel()
        args = {'models_configuration': self.models_configuration,
                'vacancy_table': self.dataset_pool.get_dataset('target_vacancy'),
                'history_table': self.dataset_pool.get_dataset('development_event_history'),
                'year': 2000,
                'location_set': self.dataset_pool.get_dataset('gridcell'),
                'resources': self.compute_resources
                }

        results = dptm.run(**args)

        self.assertEqual( results['residential'], None,
                         "No residential units should've been added/developed" )
        self.assertEqual( results['commercial'], None,
                         "No commercial units should've been added/developed" )
        self.assertEqual( results['industrial'], None,
                         "No industrial units should've been added/developed" )

    def test_development_with_nonzero_target_vacancy_and_equal_history( self ):
        """Test basic cases, where current residential vacancy = 50%, target residential vacancy is 75%,
        current non_residential vacancy is 75% (commercial), and target nonresidential vacancy is 50%.
        Residential development projects should occur, and none for nonresidential"""
        self.storage.write_table(
            table_name='target_vacancies',
            table_data={
                "year":array( [2001] ),
                "target_total_residential_vacancy":array( [0.75] ),
                "target_total_non_residential_vacancy":array( [0.50] )
                }
            )

        dptm = DevelopmentProjectTransitionModel()
        args = {'models_configuration': self.models_configuration,
        'vacancy_table': self.dataset_pool.get_dataset('target_vacancy'),
        'history_table': self.dataset_pool.get_dataset('development_event_history'),
        'year': 2001,
        'location_set': self.dataset_pool.get_dataset('gridcell'),
        'resources': self.compute_resources
        }
        results = dptm.run(**args)

        """20000 residential units should've been added because current ratio of
        10000 unoccupied / 20000 total = 0.5, and target residential vacancy rate
        is 0.75. add 20000 to numerator and denominator, and 30000 / 40000 = 0.75"""
        number_of_new_residential_units = results['residential'].get_attribute( 'residential_units' ).sum()
        self.assertEqual( number_of_new_residential_units, 20000,
                         """Exactly 20000 residential units should've been added/developed.
                         Instead, got %s""" % ( number_of_new_residential_units, ) )

        """Anytime the target vacancy rate is less than the current vacancy rate,
        no new development should occur."""
        self.assertEqual( results['commercial'], None,
                         "No commercial units should've been added/developed." )

        self.assertEqual( results['industrial'], None,
                         "No industrial units should've been added/developed." )

    def test_development_with_99_percent_target_vacancy_and_equal_history( self ):
        """Not too different from the basic case above, just trying the other extreme.
        Notice that a 100% target vacancy rate doesn't really make sense and is not possible unless
        the current vacancy rate is also 100% (also not feasible)."""
        self.storage.write_table(
            table_name='target_vacancies',
            table_data={
                "year":array( [2001] ),
                "target_total_residential_vacancy":array( [0.99] ),
                "target_total_non_residential_vacancy":array( [0.99] )
                }
            )

        dptm = DevelopmentProjectTransitionModel()
        args = {'models_configuration': self.models_configuration,
        'vacancy_table': self.dataset_pool.get_dataset('target_vacancy'),
        'history_table': self.dataset_pool.get_dataset('development_event_history'),
        'year': 2001,
        'location_set': self.dataset_pool.get_dataset('gridcell'),
        'resources': self.compute_resources
        }
        results = dptm.run(**args)

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

    def test_development_with_varied_history( self ):
        """Tests the effectiveness of events history in influencing the new projects' sizes.
        Creates 1000 industrial events in the history, and 999 of these added 6000
        industrial sqft, and the last event added 500000 industrial sqft.
        Since the target vacancy rate is 90%, we estimate approximately 250 industrial projects
        to be spawned, each adding 6000 industrial sqft (to match the history).
        (7500 * 100 + 6000*250) / (10000 * 100.0 + 6000*250)
        """
        def run_model():
            storage = StorageFactory().get_storage('dict_storage')

            storage.write_table(
                table_name='target_vacancies',
                table_data={
                    "year":array( [2000] ),
                    "target_total_residential_vacancy":array( [0.75] ),
                    "target_total_non_residential_vacancy":array( [0.90] )
                    }
                )
            storage.write_table(
                table_name='development_event_history',
                table_data={
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
            storage.write_table(
                table_name='gridcells',
                table_data={
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
            storage.write_table(
                table_name='households',
                table_data={
                    "household_id":arange( 1, 10000+1 ),
                    "grid_id":array( 100*range( 1, 100+1 ) )
                    }
                )
            storage.write_table(
                table_name='jobs',
                table_data={
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
            args = {
                'models_configuration': self.models_configuration,
                'vacancy_table': dataset_pool.get_dataset('target_vacancy'),
                'history_table': dataset_pool.get_dataset('development_event_history'),
                'year': 2000,
                'location_set': self.dataset_pool.get_dataset('gridcell'),
                'resources': Resources({"household":dataset_pool.get_dataset('household'),
                                "job":dataset_pool.get_dataset('job'),
                                "job_building_type": self.dataset_pool.get_dataset('job_building_type'),
                                'urbansim_constant':self.dataset_pool.get_dataset('urbansim_constant')})
            }
            results = dptm.run(**args)
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

    def test_development_with_equal_history( self ):
        """Tests development with both commercial and industrial jobs occupying equal amounts of space
        in each gridcell, but the even history for each job type is different -
        1000 events adding 6000 industrial sqft., and 1000 events adding 5000 commercial sqft.
        The total sqft. added for each job type should be the same (1500000 sqft.), but the number of
        projects and sqft./project should be different for each job type
        """
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='target_vacancies',
            table_data={
                "year":array( [2000] ),
                "target_total_residential_vacancy":array( [0.75] ),
                "target_total_non_residential_vacancy":array( [0.90] )
            }
        )
        storage.write_table(
            table_name='development_event_history',
            table_data={
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
        storage.write_table(
            table_name='gridcells',
            table_data={
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
        storage.write_table(
            table_name='households',
            table_data={
                "household_id":arange( 1, 10000+1 ),
                "grid_id":array( 100*range( 1, 100+1 ) )
            }
        )
        storage.write_table(
            table_name='jobs',
            table_data={
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
        args = {
            'models_configuration': self.models_configuration,
            'vacancy_table': dataset_pool.get_dataset('target_vacancy'),
            'history_table': dataset_pool.get_dataset('development_event_history'),
            'year': 2000,
            'location_set': self.dataset_pool.get_dataset('gridcell'),
            'resources': Resources({"household":dataset_pool.get_dataset('household'),
                            "job":dataset_pool.get_dataset('job'),
                            "job_building_type": self.dataset_pool.get_dataset('job_building_type'),
                            'urbansim_constant':self.dataset_pool.get_dataset('urbansim_constant')})
        }
        results = dptm.run(**args)

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
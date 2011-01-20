# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from opus_core.misc import DebugPrinter
from opus_core.variables.variable_name import VariableName
from opus_core.model import Model
from numpy.random import randint
from opus_core.logger import logger
from numpy import arange, array, where, zeros, ones, float32, int32, int8, concatenate


class BuildingTransitionModel( Model ):
    """
    Creates buildings of different building types, according to target_vacancies for each building type. The vacancy table
    must have attributes 'target_total_%s_vacancy' % type (e.g. target_total_commercial_vacancy) for each building type
    that the transition model should run.
    """
    def __init__( self, debuglevel=0 ):
        self.debug = DebugPrinter( debuglevel )
        self.model_name = "Building Transition Model"

    def check_for_space( self, values ):
        """Check that this array of values sums to something > 0."""
        self.do_check( "x > 0", array( [sum( values )] ) )

    def check_target_vacancy_is_not_100_percent( self, value ):
        """Check that the target vacancy rate is not 100% (ratio == 1), because it doesn't make sense,
        and it also causes a divide by 0 error."""
        self.do_check( "x != 1", value )

    def safe_divide(self, numerator, denominator, return_value_if_denominator_is_zero=0, type=float):
        """If denominator == 0, return return_value_if_denominator_is_zero.
        Else return numerator / denominator.
        """
        if denominator == 0:
            return return_value_if_denominator_is_zero
        return type(numerator) / denominator

    def run( self, building_set, building_types_table, vacancy_table, year, location_set,
            building_categories=None, dataset_pool=None, resources=None ):
        building_types = building_types_table.get_attribute("name")
        building_id_name = building_set.get_id_name()[0]
        location_id_name = location_set.get_id_name()[0]
        new_buildings = {building_id_name: array([], dtype=building_set.get_data_type(building_id_name)),
                         "building_type_id":array([], dtype=building_set.get_data_type("building_type_id", int8)),
                         "year_built": array([], dtype=building_set.get_data_type("year_built", int32)),
                         "sqft": array([], dtype=building_set.get_data_type("sqft", int32)),
                         "residential_units": array([], dtype=building_set.get_data_type("residential_units", int32)),
                         "improvement_value": array([], dtype= building_set.get_data_type("improvement_value", float32)),
                         "land_value": array([], dtype= building_set.get_data_type("land_value", float32)),
                         location_id_name: array([], dtype=building_set.get_data_type(location_id_name, int32))}
        max_id = building_set.get_id_attribute().max()
        buildings_set_size_orig = building_set.size()

        for itype in range(building_types_table.size()): # iterate over building types
            type = building_types[itype]
            type_code = building_types_table.get_id_attribute()[itype]
            is_residential = building_types_table.get_attribute("is_residential")[itype]
            vacancy_attribute = 'target_total_%s_vacancy' % type
            if vacancy_attribute not in vacancy_table.get_known_attribute_names():
                logger.log_warning("No target vacancy for building type '%s'. Transition model for this building type skipped." % type)
                continue
            vacancy_table.get_attribute(vacancy_attribute)  # ensures that the attribute is loaded
            target_vacancy_rate = eval("vacancy_table.get_data_element_by_id( year ).%s" % vacancy_attribute)

            compute_resources = Resources(resources)
            compute_resources.merge({"debug":self.debug})
            units_attribute = building_types_table.get_attribute('units')[itype]

            # determine current-year vacancy rates
            if is_residential:
                default_vacancy_variable = "urbansim.%s.vacant_%s_units_from_buildings" % (
                                                                   location_set.get_dataset_name(), type)
            else:
                default_vacancy_variable = "urbansim.%s.vacant_%s_sqft_from_buildings" % (
                                                                   location_set.get_dataset_name(), type)
            variable_for_vacancy = compute_resources.get(
                                    "%s_vacant_variable" % type, default_vacancy_variable)
            location_set.compute_variables([variable_for_vacancy, "urbansim.%s.buildings_%s_space" % (
                                                                      location_set.get_dataset_name(),type)],
                                        dataset_pool=dataset_pool, resources = compute_resources)

            vacant_units_sum = location_set.get_attribute(variable_for_vacancy).sum()
            units_sum = float( location_set.get_attribute("buildings_%s_space" % type).sum() )
            vacant_rate = self.safe_divide(vacant_units_sum, units_sum)

            should_develop_units = int(round(max( 0, ( target_vacancy_rate * units_sum - vacant_units_sum ) /
                                         ( 1 - target_vacancy_rate ) )))
            logger.log_status(type + ": vacant units: %d, should be vacant: %f, sum units: %d"
                          % (vacant_units_sum, target_vacancy_rate * units_sum, units_sum))

            if not should_develop_units:
                logger.log_note(("Will not build any " + type + " units, because the current vacancy of %d units\n"
                             + "is more than the %d units desired for the vacancy rate of %f.")
                            % (vacant_units_sum,
                               target_vacancy_rate * units_sum,
                               target_vacancy_rate))
                continue

            improvement_value = building_set.compute_variables("urbansim.%s.%s_improvement_value" % (
                                                                     building_set.get_dataset_name(), type),
                                                                   dataset_pool=dataset_pool,
                                                                   resources=compute_resources)
            average_improvement_value = improvement_value.sum()/ units_sum

            #create buildings
            is_building_type = building_set.compute_variables("urbansim.building.is_building_type_%s" % type,
                                                              dataset_pool=dataset_pool,
                                                              resources=compute_resources)
            units_of_this_type = building_set.compute_variables(units_attribute, dataset_pool=dataset_pool,
                                           resources=compute_resources)
            units_of_this_type = units_of_this_type*is_building_type
            units_without_zeros_idx = where(units_of_this_type > 0)[0]
            history_values_without_zeros = units_of_this_type[units_without_zeros_idx]
            history_improvement_values_without_zeros = where(improvement_value[units_without_zeros_idx]>0,
                                                             improvement_value[units_without_zeros_idx],
                                                             average_improvement_value)
            mean_size = history_values_without_zeros.mean()
            idx = array( [], dtype="int32" )
            # Ensure that there are some development projects to choose from.
            num_of_projects_to_select = max( 10, int( should_develop_units / mean_size ) )
            while True:
                idx = concatenate( ( idx, randint( 0, history_values_without_zeros.size,
                                                   size=num_of_projects_to_select) ) )
                csum = history_values_without_zeros[idx].cumsum()
                idx = idx[where( csum <= should_develop_units )]
                if csum[-1] >= should_develop_units:
                    break
            nbuildings = idx.size
            new_buildings["building_type_id"] = concatenate((new_buildings["building_type_id"], type_code*ones(nbuildings)))
            new_buildings["year_built"] = concatenate((new_buildings["year_built"], year*ones(nbuildings)))
            new_max_id = max_id + nbuildings
            new_buildings[building_id_name]=concatenate((new_buildings[building_id_name], arange(max_id+1, new_max_id+1)))
            max_id = new_max_id
            new_buildings["improvement_value"] = concatenate((new_buildings["improvement_value"],
                                                              history_improvement_values_without_zeros[idx]))

            if is_residential:
                target_size_attribute = "residential_units"
                zero_attribute = "sqft"
            else:
                target_size_attribute = "sqft"
                zero_attribute = "residential_units"
            new_buildings[target_size_attribute] = concatenate((new_buildings[target_size_attribute], history_values_without_zeros[idx]))
            new_buildings[zero_attribute] = concatenate((new_buildings[zero_attribute], zeros(nbuildings)))
            new_buildings[location_id_name] = concatenate((new_buildings[location_id_name], zeros(nbuildings)))
            new_buildings["land_value"] = concatenate((new_buildings["land_value"], zeros(nbuildings)))
            logger.log_status("Creating %s %s of %s %s buildings." % (history_values_without_zeros[idx].sum(),
                                                                   target_size_attribute, nbuildings, type))

        building_set.add_elements(new_buildings, require_all_attributes=False)
        if building_categories: # should be a dictionary of categories for each building type
            building_set.resources['building_categories'] = building_categories
        # add submodel attribute
        category_variables = map(lambda type: "urbansim.%s.size_category_%s" % (building_set.get_dataset_name(), type),
                                           building_types)

        for category_var in category_variables:
            var = VariableName(category_var)
            if var.get_alias() in building_set.get_known_attribute_names():
                building_set.delete_one_attribute(var)
            building_set.compute_variables(var, dataset_pool=dataset_pool, resources = compute_resources)
            building_set.add_primary_attribute(building_set.get_attribute(var), var.get_alias())

        difference = building_set.size() - buildings_set_size_orig
        return difference

from opus_core.tests import opus_unittest
from opus_core.tests.stochastic_test_case import StochasticTestCase
from numpy import array, arange, where
from numpy import ma
from opus_core.resources import Resources
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.datasets.job_dataset import JobDataset
from urbansim.datasets.target_vacancy_dataset import TargetVacancyDataset
from opus_core.datasets.dataset_pool import DatasetPool
from urbansim.datasets.building_type_dataset import BuildingTypeDataset
from urbansim.datasets.job_building_type_dataset import JobBuildingTypeDataset
from urbansim.datasets.building_dataset import BuildingDataset
from opus_core.storage_factory import StorageFactory


class BTMTests(StochasticTestCase):

    def setUp( self ):
        """here, we simulate 50 residential units
        and 5000 commercial, industrial, and governmental sqft added to each of the gridcells in previous years.
        """

        ### TODO: do not redefine these constants.
        self.comc = 1
        self.indc = 3
        self.govc = 2
        self.sfhc = 4
        self.mfhc = 5

        storage = StorageFactory().get_storage('dict_storage')

        gridcells_table_name = 'gridcells'
#            create 100 gridcells, each with 200 residential units and space for 100 commercial jobs,
#            100 industrial jobs, and residential, industrial, and commercial value at $500,000 each
        storage.write_table(
            table_name=gridcells_table_name,
            table_data={
                "grid_id": arange( 1, 100+1 ),
                "commercial_sqft_per_job":array( 100*[100] ),
                "industrial_sqft_per_job":array( 100*[100] ),
                "single_family_improvement_value":array( 100*[500000] ),
                "commercial_improvement_value":array( 100*[500000] ),
                "industrial_improvement_value":array( 100*[500000] )
                }
            )
        self.gridcells = GridcellDataset(in_storage=storage, in_table_name=gridcells_table_name)

        buildings_table_name = 'buildings'
#            2000 buildings (1000 with 20 residential units each, 500 with 20 commercial job and 500 with 20 industrial job each)
        storage.write_table(
            table_name=buildings_table_name,
            table_data={
                "building_id":arange( 1, 2000+1 ), # 2000 buildings
                "grid_id":array( 20*range( 1, 100+1 ), dtype=int32 ), # spread evenly across 100 gridcells
                "building_type_id":array(1000*[self.sfhc] +
                                         500*[self.comc] +
                                         500*[self.indc], dtype=int8),
                "sqft": array(1000*[0] +
                              500*[2000] +
                              500*[2000], dtype=int32),
                "residential_units": array(1000*[20] +
                                           500* [0] +
                                           500* [0], dtype=int32),
                "improvement_value": array(1000*[50] +
                                           500* [50] +
                                           500* [50], dtype=float32),
                "year_built": array(1000*[1940] +
                                    500* [1940] +
                                    500* [1940], dtype=int32)
                }
            )
        self.buildings = BuildingDataset(in_storage=storage, in_table_name=buildings_table_name)

        households_table_name = 'households'
#            create 10000 households, 100 in each of the 100 gridcells.
#            there will initially be 100 vacant residential units in each gridcell then.
        storage.write_table(
            table_name=households_table_name,
            table_data={
                "household_id":arange( 1, 10000+1 ),
                "grid_id":array( 100*range( 1, 100+1 ), dtype=int32 )
                }
            )
        self.households = HouseholdDataset(in_storage=storage, in_table_name=households_table_name)

        building_types_table_name = 'building_types'
        storage.write_table(
            table_name=building_types_table_name,
            table_data={
                "building_type_id":array([self.govc,self.comc,self.indc, self.sfhc, self.mfhc], dtype=int8),
                "name": array(["governmental", "commercial", "industrial", "single_family","multiple_family"]),
                "units": array(["governmental_sqft", "commercial_sqft", "industrial_sqft", "residential_units", "residential_units"]),
                "is_residential": array([0,0,0,1,1], dtype='?')
                }
            )
        self.building_types = BuildingTypeDataset(in_storage=storage, in_table_name=building_types_table_name)

        job_building_types_table_name = 'job_building_types'
        storage.write_table(
            table_name=job_building_types_table_name,
            table_data={
                "id":array([self.govc,self.comc,self.indc, self.sfhc, self.mfhc], dtype=int8),
                "name": array(["governmental", "commercial", "industrial", "single_family","multiple_family"])
                }
            )
        self.job_building_types = JobBuildingTypeDataset(in_storage=storage, in_table_name=job_building_types_table_name)

        jobs_table_name = 'jobs'
#            create 2500 commercial jobs and distribute them equally across the 100 gridcells,
#            25 commercial buildings/gridcell
        storage.write_table(
            table_name=jobs_table_name,
            table_data={
                "job_id":arange( 1, 2500+1 ),
                "grid_id":array( 25*range( 1, 100+1 ), dtype=int32 ),
                "sector_id":array( 2500*[1], dtype=int32 ),
                "building_type":array(2500*[self.comc], dtype=int8)
                }
            )
        self.jobs = JobDataset(in_storage=storage, in_table_name=jobs_table_name)

        self.dataset_pool = DatasetPool()
        self.dataset_pool.add_datasets_if_not_included({
                                            "household":self.households,
                                            "job":self.jobs,
                                            "building":self.buildings,
                                            "building_type": self.building_types,
                                            "job_building_type": self.job_building_types})

        self.building_categories = {'commercial': array([1000,5000]),
                                    'industrial': array([500,800,1000])}

    def test_no_development_with_zero_target_vacancy( self ):
        """If the target vacany ratest are 0%, then no development should occur and thus,
        the building set should remain unchanged (should have the same size).
        """

        """specify that the target vacancies for the year 2000 should be 0% for
        commercial building type."""
        storage = StorageFactory().get_storage('dict_storage')

        target_vacancies_table_name = 'target_vacancies'
        storage.write_table(
            table_name=target_vacancies_table_name,
            table_data={
                "year":array( [2000] ),
                "target_total_commercial_vacancy":array( [0.0] )
                }
            )
        target_vacancies = TargetVacancyDataset(in_storage=storage, in_table_name=target_vacancies_table_name)

        nbuildings = self.buildings.size()
        btm = BuildingTransitionModel()
        results = btm.run(self.buildings, self.building_types,
                           target_vacancies,
                           2000,
                           self.gridcells, building_categories=self.building_categories,
                           dataset_pool=self.dataset_pool)

        self.assertEqual( results, 0, "No buildings should've been added/developed" )
        self.assertEqual( nbuildings, self.buildings.size(), "No buildings should've been added/developed" )

    def test_development_with_nonzero_target_vacancy( self ):
        """Test basic cases, where current single family vacancy = 50%, target single family vacancy is 75%,
        current commercial vacancy is 75%, and target commercial vacancy is 50%.
        Single family development projects should occur, and none for commercial"""

        storage = StorageFactory().get_storage('dict_storage')

        target_vacancies_table_name = 'target_vacancies'
        storage.write_table(
            table_name=target_vacancies_table_name,
            table_data={
                "year":array( [2001], dtype=int32 ),
                "target_total_single_family_vacancy":array( [0.75] ),
                "target_total_commercial_vacancy":array( [0.50] )
                }
            )
        target_vacancies = TargetVacancyDataset(in_storage=storage, in_table_name=target_vacancies_table_name)

        resunits_before, commercial_before, industrial_before, tmp1, tmp2, tmp3 = self.get_residential_commercial_industrial_units(self.buildings)

        btm = BuildingTransitionModel()
        results = btm.run(self.buildings, self.building_types,
                           target_vacancies,
                           2001,
                           self.gridcells, building_categories=self.building_categories,
                           dataset_pool=self.dataset_pool )

        """20000 residential units should've been added because current ratio of
        10000 unoccupied / 20000 total = 0.5, and target residential vacancy rate
        is 0.75. add 20000 to numerator and denominator, and 30000 / 40000 = 0.75"""
        resunits_after, commercial_after, industrial_after, tmp1, tmp2, tmp3 = self.get_residential_commercial_industrial_units(self.buildings)

        self.assertEqual( resunits_after-resunits_before, 20000,
                         """Exactly 20000 residential units should've been added/developed.
                         Instead, got %s""" % ( resunits_after-resunits_before, ) )

        """Anytime the target vacancy rate is less than the current vacancy rate,
        no new development should occur."""
        self.assertEqual( commercial_before - commercial_after, 0,
                         "No commercial units should've been added/developed." )

        self.assertEqual( industrial_before-industrial_after, 0,
                         "No industrial units should've been added/developed." )

        """Check categories"""
        self.assertEqual(ma.allequal(self.buildings.get_categories("commercial"), self.building_categories["commercial"]), True,
                         "Error in creating categories for commercial buildings.")
        self.assertEqual(ma.allequal(self.buildings.get_categories("industrial"), self.building_categories["industrial"]), True,
                         "Error in creating categories for industrial buildings.")

    def test_development_with_99_percent_target_vacancy( self ):
        """Not too different from the basic case above, just trying the other extreme.
        Notice that a 100% target vacancy rate doesn't really make sense and is not possible unless
        the current vacancy rate is also 100% (also not feasible)."""

        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='target_vacancies',
            table_data={
                'year':array([2001], dtype=int32),
                'target_total_single_family_vacancy':array([0.99]),
                'target_total_commercial_vacancy':array([0.99]),
                'target_total_industrial_vacancy':array([0.99])
                },
            )
        target_vacancies = TargetVacancyDataset(in_storage=storage, in_table_name='target_vacancies')

        resunits_before, commercial_before, industrial_before, tmp1, tmp2, tmp3 = self.get_residential_commercial_industrial_units(self.buildings)

        btm = BuildingTransitionModel()
        results = btm.run(self.buildings, self.building_types,
                           target_vacancies,
                           2001,
                           self.gridcells, building_categories=self.building_categories,
                           dataset_pool=self.dataset_pool)

        """20000 residential units should've been added because current ratio of
        10000 unoccupied / 20000 total = 0.5, and target residential vacancy rate
        is 0.75. add 20000 to numerator and denominator, and 30000 / 40000 = 0.75"""
        resunits_after, commercial_after, industrial_after, tmp1, tmp2, tmp3 = self.get_residential_commercial_industrial_units(self.buildings)

        """
        .01 = 10000 / (20000 + x)

        x = (10000 - (.01*20000))/.01
        """
        residential_units_developed = (10000 - (.01*20000))/.01
        max_difference = 50
        self.assert_(self.is_close(resunits_after - resunits_before, residential_units_developed, max_difference),
                         """Approximately %s residential units should've been added/developed.
                         Instead, got %s""" % (residential_units_developed, resunits_after - resunits_before))

        """
        2500 commercial jobs * 100 occupied square feet per commercial job is
        250,000 commercial square feet occupied

        250,000 / (1,000,000 + x) = .01

        which converts into:
        x = (250,000 - .01*1,000,000)/.01

        x = 24,000,000
        """
        commercial_sqft_developed = (250000 - (.01*1000000))/.01
        max_difference = 5000
        self.assert_(self.is_close(commercial_after - commercial_before, commercial_sqft_developed, max_difference),
                         """Approximately %s commercial sqft should've been added/developed.
                         Instead, got %s""" % (commercial_sqft_developed, commercial_after - commercial_before))

        self.assertEqual(industrial_before - industrial_after, 0,
                         "No industrial units should've been added/developed.")

    def get_residential_commercial_industrial_units(self, buildings):
        resunits = buildings.get_attribute("residential_units").sum()
        buildings.compute_variables([
                  "urbansim.building.is_building_type_commercial", "urbansim.building.is_building_type_industrial",
                  "urbansim.building.is_building_type_single_family"],
                                         dataset_pool=self.dataset_pool)
        commercial = (buildings.get_attribute("sqft")*buildings.get_attribute("is_building_type_commercial")).sum()
        industrial = (buildings.get_attribute("sqft")*buildings.get_attribute("is_building_type_industrial")).sum()
        return (resunits, commercial, industrial,
                buildings.get_attribute("is_building_type_single_family").sum(),
                buildings.get_attribute("is_building_type_commercial").sum(),
                buildings.get_attribute("is_building_type_industrial").sum())

    def is_close(self, first_value, second_value, max_difference):
        return abs(first_value - second_value) <= max_difference


if __name__=="__main__":
    opus_unittest.main()
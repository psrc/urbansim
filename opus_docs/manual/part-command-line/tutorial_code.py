# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


# Test of the installation
from opus_core.opus_package_info import package as opus_core_package
opus_core_package().info()
from urbansim.opus_package_info import package as urbansim_package
urbansim_package().info()

# Working with datasets
import os
import urbansim
us_path = urbansim.__path__[0]
from opus_core.storage_factory import StorageFactory
storage = StorageFactory().get_storage('tab_storage',
    storage_location = os.path.join(us_path, "data/tutorial"))

from opus_core.datasets.dataset import Dataset
households = Dataset(in_storage = storage,
                         in_table_name = 'households', 
                         id_name='household_id',
                         dataset_name='household')
households.get_attribute_names()
households.get_id_attribute()
households.size()
households.get_attribute("income")
households.get_attribute_names()
households.load_dataset()
households.get_attribute_names()
#households.plot_histogram("income", bins = 10)
#households.r_histogram("income")
#households.r_scatter("persons", "income")
households.correlation_coefficient("persons", "income")
households.correlation_matrix(["persons", "income"])
households.summary()
households.add_primary_attribute(data=[4,6,9,2,4,8,2,1,3,2], name="location")
households.get_attribute_names()
households.modify_attribute(name="location", data=[0,0], index=[0,1])
households.get_attribute("location")
households.get_data_element_by_id(5).location

#households.write_dataset(out_storage=storage, out_table_name="households_output")


households.get_dataset_name()

# Working with models
from opus_core.choice_model import ChoiceModel
choicemodel = ChoiceModel(choice_set=[1,2,3],
                       utilities = "opus_core.linear_utilities",
                       probabilities = "opus_core.mnl_probabilities",
                       choices = "opus_core.random_choices")
from numpy import array
from opus_core.equation_specification import EquationSpecification
specification = EquationSpecification(
      coefficients = array([
        "beta01",      "beta12",         "beta03",    "beta13"
                              ]),
      variables = array([
        "constant","household.persons", "constant", "household.persons"
                        ]),
      equations = array([
           1,              2,                3,             3
                          ])
      )

households.add_primary_attribute(data=[1,2,2,2,1,3,3,1,2,1], name="choice_id")

coefficients, other_results = choicemodel.estimate(specification,
                         households, procedure="opus_core.bhhh_mnl_estimation")
                         
#
# Uncomment to output mycoef.tab
#
#coefficients.write(out_storage=storage, out_table_name="mycoef")

from numpy.random import seed
seed(1)
choices = choicemodel.run(
                 specification,  coefficients, households, debuglevel=1)
households.modify_attribute(name="choice_id", data=choices)

from opus_core.coefficients import Coefficients
coefficients = Coefficients(
                     names=array(["beta01", "beta12", "beta03", "beta13"]),
                     values=array([0.5,      0.2,       -5.0,     1.3]))

# LCM
locations = Dataset(in_storage = storage,
                        in_table_name = 'locations', 
                        id_name='location',
                        dataset_name='gridcell')


coefficients = Coefficients(names=("costcoef", ), values=(-0.01,))
specification = EquationSpecification(variables=("gridcell.cost", ),
                                      coefficients=("costcoef", ))

from urbansim.models.household_location_choice_model import HouseholdLocationChoiceModel
hlcm = HouseholdLocationChoiceModel(
    location_set = locations,
    sampler=None, compute_capacity_flag=False)
seed(1)
results = hlcm.run(specification, coefficients, agent_set=households)
households.get_attribute("location")
coef, results = hlcm.estimate(specification, agent_set=households)
#hlcm.plot_choice_histograms(capacity=locations.get_attribute("capacity"))

number_of_agents = "gridcell.number_of_agents(household)"
hlcm2 = HouseholdLocationChoiceModel(
                         location_set = locations,
                         sampler=None,
                         choices="urbansim.lottery_choices",
                         compute_capacity_flag=True,
                         capacity_string="capacity",
                         number_of_agents_string=number_of_agents,
                         number_of_units_string="capacity",
                         run_config={"lottery_max_iterations":10})
seed(1)
result = hlcm2.run(specification, coefficients, households)
#coef, results = hlcm2.estimate(specification, agent_set=households, debuglevel=1)
#hlcm2.plot_choice_histograms(capacity=locations.get_attribute("capacity"))
households.get_attribute("location")

# Regression model
locations.add_primary_attribute(name="distance_to_cbd", data=[5,10,5,1,20,0,7,7,3])

from opus_core.regression_model import RegressionModel
rm = RegressionModel(regression_procedure="opus_core.linear_regression")
specification = EquationSpecification(
                          variables=array(["constant", "gridcell.distance_to_cbd"]),
                          coefficients=array(["constant", "dcbd_coef"]))

coef, other_results = rm.estimate(specification, dataset=locations, 
                                  outcome_attribute="gridcell.cost", 
                                  procedure="opus_core.estimate_linear_regression")
coef.summary()

dstorage = StorageFactory().get_storage('dict_storage')
dstorage.write_table(
    table_name = 'gridcells',
    table_data = {'id':array([1,2,3,4]),
             'distance_to_cbd':array([2,4,6,8])
             })

ds = Dataset(in_storage=dstorage, in_table_name='gridcells',
             id_name='id', dataset_name='gridcell')

cost = rm.run(specification, coefficients=coef, dataset=ds)


# Variables

# Concept
locations.get_dataset_name()

locations.add_primary_attribute(name="percent_wetland",
                            data=[85,20,0,90,35,51,0,10,5])

from opus_core.datasets.dataset_pool import DatasetPool
dataset_pool = DatasetPool(package_order=['urbansim', 'opus_core'], storage=storage)
dataset_pool.datasets_in_pool()
hs = dataset_pool.get_dataset("household")
dataset_pool.datasets_in_pool()
hs.size()
constant = dataset_pool.get_dataset("urbansim_constant")
constant["percent_coverage_threshold"] = 50
locations.compute_variables(["urbansim.gridcell.is_in_wetland"], dataset_pool=dataset_pool)
locations.get_attribute("is_in_wetland")

# Interaction variables
from opus_core.datasets.interaction_dataset import InteractionDataset
interactions = InteractionDataset(dataset1 = households, dataset2 = locations)
interactions.get_dataset_name()

from numpy import arange
interactions = InteractionDataset(dataset1 = households, dataset2 = locations, index1 = arange(5), index2 = arange(3))
interactions.compute_variables(["urbansim.household_x_gridcell.cost_times_income"])

specification = EquationSpecification(
                     variables=array([
                          "gridcell.cost",
                          "urbansim.household_x_gridcell.cost_times_income"]),
                     coefficients=array(["costcoef", "cti_coef"]))
households.add_primary_attribute(data=[2,8,3,1,5,4,9,7,3,6], name="location")
coef, other_results = hlcm.estimate(specification, households)

# Versioning
households.get_version("income")
res = interactions.compute_variables(["urbansim.household_x_gridcell.cost_times_income"])
interactions.get_version("cost_times_income")
households.modify_attribute(name="income", data=[14000], index=[9])
households.get_version("income")
res = interactions.compute_variables(["urbansim.household_x_gridcell.cost_times_income"])
interactions.get_version("cost_times_income")

# Using numbers
res = locations.compute_variables(
                                  map(lambda threshold:
                                      "urbansim.gridcell.is_near_cbd_if_threshold_is_%s" % threshold, [2,4,7]))
locations.get_attribute("is_near_cbd_if_threshold_is_2")
locations.get_attribute("is_near_cbd_if_threshold_is_4")
locations.get_attribute("is_near_cbd_if_threshold_is_7")

# Transformations
locations.compute_variables([
 "sqrt_distance_to_cbd = sqrt(gridcell.distance_to_cbd)"])
locations.get_attribute("sqrt_distance_to_cbd")

specification = EquationSpecification(
      variables=("gridcell.cost",
         "ln(urbansim.household_x_gridcell.cost_times_income)"),
      coefficients=("costcoef", "cti_coef"))

# Aggregate, disaggregate
dstorage = StorageFactory().get_storage('dict_storage')
dstorage.write_table(table_name='neighborhoods',
                     table_data={"nbh_id":array([1,2,3])}
                      )
dstorage.write_table(table_name='zones',
                     table_data={"zone_id":array([1,2,3,4,5]),
                                "nbh_id":  array([3,3,1,2,1]),
                                }
                      )


neighborhoods = Dataset(in_storage=dstorage, in_table_name='neighborhoods', dataset_name="neighborhood", id_name="nbh_id")
zones = Dataset(in_storage=dstorage, in_table_name='zones', dataset_name="zone", id_name="zone_id")
locations.add_primary_attribute(name="zone_id", data=[3,5,2,2,1,1,3,5,3])
dataset_pool = DatasetPool(package_order=['urbansim', 'opus_core'],
                               datasets_dict={'gridcell': locations,
                                              'zone': zones, 
                                              'neighborhood':neighborhoods})
aggr_var = "aggregated_capacity = zone.aggregate(gridcell.capacity)"
zones.compute_variables(aggr_var, dataset_pool=dataset_pool)
zones.get_attribute("aggregated_capacity")
aggr_var = "zone.aggregate(urbansim.gridcell.is_near_cbd_if_threshold_is_2, function=maximum)"
zones.compute_variables(aggr_var, dataset_pool=dataset_pool)
print 'this %s' % zones.get_attribute(aggr_var)

aggr_var2 = "neighborhood.aggregate(gridcell.capacity, intermediates=[zone], function=sum)"
neighborhoods.compute_variables(aggr_var2, dataset_pool=dataset_pool)

neighborhoods.add_primary_attribute(name="is_cbd", data=[0,0,1])
disaggr_var = "is_cbd = gridcell.disaggregate(neighborhood.is_cbd, intermediates=[zone])"
locations.compute_variables(disaggr_var, dataset_pool=dataset_pool)

from opus_core.datasets.alldata_dataset import AlldataDataset
alldata = AlldataDataset(dataset_name="alldata")
alldata.compute_variables(
                      "total_capacity = alldata.aggregate_all(gridcell.capacity, function=sum)",
                      dataset_pool=dataset_pool)

# Number of agents
households.modify_attribute(name="location", data=[2, 8, 3, 1, 5, 4, 9, 7, 3, 6])
dataset_pool.add_datasets_if_not_included({'household': households})
locations.compute_variables("gridcell.number_of_agents(household)",
                        dataset_pool=dataset_pool)
neighborhoods.compute_variables("neighborhood.number_of_agents(zone)",
                            dataset_pool=dataset_pool)

# Creating a model
from opus_core.model import Model
from opus_core.logger import logger
class MyModel(Model):
    model_name = "my model"
    def run(self):
        logger.log_status("I'm running!")
        return

MyModel().run()

from opus_core.chunk_model import ChunkModel
from numpy import apply_along_axis
from numpy.random import normal

class MyChunkModel(ChunkModel):
    model_name = "my chunk model"
    def run_chunk(self, index, dataset, mean_attribute, variance_attribute, n=1):
        mean_values = dataset.get_attribute_by_index(mean_attribute, index)
        variance_values = dataset.get_attribute_by_index(variance_attribute, 
                                                         index)
        def draw_rn (mean_var, n):
            return normal(mean_var[0], mean_var[1], size=n)
        normal_values = apply_along_axis(draw_rn, 0, (mean_values, variance_values), n)
        return normal_values.mean(axis=0)

from numpy import arange, array
from opus_core.storage_factory import StorageFactory
storage = StorageFactory().get_storage('dict_storage')
storage.write_table(table_name='dataset',
                   table_data={'id':arange(100000)+1,
                           'means':array(50000*[0]+50000*[10]),
                           'variances':array(50000*[1]+50000*[5])
                          }
                 )
from opus_core.datasets.dataset import Dataset
mydataset = Dataset(in_storage=storage, in_table_name='dataset',
                id_name='id', dataset_name='mydataset')

seed(1)
results = MyChunkModel().run(chunk_specification={'nchunks':5},
                             dataset=mydataset,
                             mean_attribute="means", variance_attribute="variances", n=10)
results[0:50000].mean()
results[50000:].mean()

#from shutil import rmtree
#if os.path.exists(my_directory):
#    rmtree(my_directory)
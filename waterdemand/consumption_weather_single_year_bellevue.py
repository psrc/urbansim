# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os

from numpy import where, logical_or, logical_and, ones, zeros, exp

from opus_core.resources import Resources
from opus_core.variables.attribute_type import AttributeType
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.storage_factory import StorageFactory
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from opus_core.regression_model import RegressionModel
from opus_core.equation_specification import EquationSpecification
from opus_core.datasets.multiple_year_dataset_view import MultipleYearDatasetView

import waterdemand
from waterdemand.datasets.weather_dataset import WeatherDataset


#======================================================================
# The estimation and simulation runs from a cache.
# If your data is in MySQL, use create_baseyear_cache first.
#======================================================================
print "Create gridcell and water conpsumption dataset from cache directory"
cache_directory = r"C:\tab\bellevue7"

year = 2000

SimulationState().set_cache_directory(cache_directory)
SimulationState().set_current_time(year)

SessionConfiguration(
    new_instance = True,
    package_order = ['waterdemand', 'psrc', 'urbansim', 'opus_core'],
    in_storage = AttributeCache()
    )
    
dataset_pool = SessionConfiguration().get_dataset_pool()

# what type of water consumption
consumption_type = 'consumption_re'

consumption = SessionConfiguration().get_dataset_from_pool(consumption_type)

print "Create Dataset object for weather"

us_path = waterdemand.__path__[0]

weather_storage = StorageFactory().get_storage('tab_storage', storage_location=us_path)

weather = WeatherDataset(
    in_storage = weather_storage,
    in_table_name = "weather", 
    id_name="year_id")

# Group records by month into sub model...
# categorize months into group, and assign a sub_model id for each group
# we will estimate a set of coefficient for each sub model group
#category_bins = [2,4,6,8,10,12]
#sub_model_ids = consumption.categorize("month", category_bins) + 1 
#consumption.add_attribute(sub_model_ids, "sub_model_id")

#or
#"""Arranging consumption data by 2-month bill period"""
#print "Selecting data for bimonthly period"
months = [7, 8] # which two months to estimate and simulate
weather_attributes = ["t_max4"] # what are (is) the correspondent weather attribute name(s)

filter_indices = where(
    logical_and(
        logical_or(
            consumption.get_attribute("month") == months[0],
            consumption.get_attribute("month") == months[1],
            ),
        consumption.get_attribute('year') == year
        ),
    )[0]

index_est = filter_indices

# records consumption for a single year in given 2 months are less than 50000, so don't do sample
# but use full set by set index_set to None
#index_est = array(sample(month_index,50000))

#attache weather attribute to consumption data, as PRIMARY attribute

#consumption.join(weather, name=weather_attributes, join_attribute="year", 
#                 metadata=AttributeType.PRIMARY)

print "Create Specification"

specification = EquationSpecification(
                  variables = 
                   (#"constant",
#                    "consumption:opus_core.func.disaggregate(urbansim.gridcell.residential_units) as residential_units",
#                    "consumption:opus_core.func.disaggregate(urbansim.gridcell.average_income_per_housing_unit) as avg_income",
                  # "consumption:opus_core.func.disaggregate(urbansim.gridcell.ln_commercial_sqft) as ln_com_sqft",
                   # "t_max4",
#                    "sum_demand_lag1"  # we can add variables of last year (in this case, 1999) by using variable name + "_lag1"
#                    "sum_demand_times_2",
                    "waterdemand.consumption_re.something_like_sum_demand",
                   ),
                  coefficients = 
                   (#"constant",
                    #"residential_units",
#                    "avg_income",
                   #"commercial_sqft",
                   #"t_max",
#                   "demand_lag1"
#                    "sum_demand_times_2",
                    "waterdemand.consumption_re.something_like_sum_demand",
                   )
                 )

print "Create a model object"

years = range(2001, 2003)

# single
model = RegressionModel()
print "Estimate coefficients - single"
coefficients, other_est_results = model.estimate(specification, consumption, 
                    outcome_attribute="waterdemand.%s.sum_demand" % consumption_type,  # if outcome_attribute is opus_core.func.ln(), the simulation results need to take exp()
                    index=index_est, 
                    procedure="opus_core.estimate_linear_regression",
                    data_objects=dataset_pool.datasets_in_pool())


"""Simulate over the set of years."""
for year in years:  
    print "\nSimulate water demand %s" % year
    SimulationState().set_current_time(year)
    dataset_pool = SessionConfiguration().get_dataset_pool()
    dataset_pool.remove_all_datasets()
    gridcells = dataset_pool.get_dataset("gridcell")
    
    #create a ConsumptionDataset instance out of gridcells - simulate water demand for every gridcell
    resources = Resources({'data':{
            "grid_id":gridcells.get_id_attribute(),
            "year":year * ones(gridcells.size()),
            "month":months[0] * ones(gridcells.size()),
            "sum_demand":zeros(gridcells.size())
            }})
    this_consumption = dataset_pool.get_dataset(consumption_type)
    
    #join consumption set with weather data
    this_consumption.join(weather, name=weather_attributes, join_attribute="year", 
                     metadata=AttributeType.PRIMARY)
    #run simulation
    result = model.run(specification, coefficients, this_consumption, index=None,
                       chunk_specification={'nchunks':3},
                       data_objects=dataset_pool.datasets_in_pool())
    
    #result = exp(result)
    this_consumption.modify_attribute("sum_demand", result)
    
    #keep only those with meanful water demand pridiction, e.g. residential_units > 0 
    keep_index = where(result>0)[0]
    
    this_consumption.subset_by_index(keep_index)
    
    year_dir = os.path.join(cache_directory, str(year))
    out_storage = StorageFactory().get_storage(type="tab_storage", storage_location=year_dir)
    
    this_consumption.flush_dataset()
    print result







# Estimate with a multi-year dataset: 

print "Create Specification - multi-year dataset"

specification = EquationSpecification(
                  variables = 
                   (#"constant",
#                    "consumption:opus_core.func.disaggregate(urbansim.gridcell.residential_units) as residential_units",
#                    "consumption:opus_core.func.disaggregate(urbansim.gridcell.average_income_per_housing_unit) as avg_income",
                  # "consumption:opus_core.func.disaggregate(urbansim.gridcell.ln_commercial_sqft) as ln_com_sqft",
                   # "t_max4",
#                    "sum_demand_lag1"  # we can add variables of last year (in this case, 1999) by using variable name + "_lag1"
#                    "sum_demand_times_2",
                    "urbansim.gridcell.industrial_sqft",
                   ),
                  coefficients = 
                   (#"constant",
                    #"residential_units",
#                    "avg_income",
                   #"commercial_sqft",
                   #"t_max",
#                   "demand_lag1"
#                    "sum_demand_times_2",
                    "urbansim.gridcell.industrial_sqft",
                   )
                 )

multi_year_gridcells = MultipleYearDatasetView(
    name_of_dataset_to_merge = 'gridcell',
    in_table_name = 'gridcells',
    attribute_cache = AttributeCache(),
    years_to_merge = [year, year-1],# baseyear and the year before
    )

model = RegressionModel()
print "Estimate coefficients - multi"
coefficients, other_est_results = model.estimate(specification, multi_year_gridcells, 
                    outcome_attribute="urbansim.gridcell.industrial_improvement_value",  # if outcome_attribute is opus_core.func.ln(), the simulation results need to take exp()
                    index=index_est, 
                    procedure="opus_core.estimate_linear_regression",
                    data_objects=dataset_pool.datasets_in_pool())
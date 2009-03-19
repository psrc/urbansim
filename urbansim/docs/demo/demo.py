# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE


import os

from numpy.random import seed
from numpy import ones, array, where
from random import sample

from opus_core.coefficients import Coefficients
from opus_core.equation_specification import EquationSpecification
from opus_core.resources import Resources
from opus_core.storage_factory import StorageFactory
from opus_core.session_configuration import SessionConfiguration

from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.datasets.zone_dataset import ZoneDataset
from urbansim.datasets.job_dataset import JobDataset
from urbansim.models.household_location_choice_model_creator import HouseholdLocationChoiceModelCreator

from opus_core.database_management.database_server import DatabaseServer
from opus_core.database_management.configurations.scenario_database_configuration import ScenarioDatabaseConfiguration


# Datasets
##########
# agents from householdset.tab
agents = HouseholdDataset(in_storage = StorageFactory().get_storage('tab_storage', storage_location='.'),
                      in_table_name = "householdset", id_name="agent_id")

agents.summary()
agents.get_attribute("income")
agents.plot_histogram("income", bins = 10)
agents.r_histogram("income")
agents.r_scatter("income", "persons")

# gridcells from PSRC
locations_psrc = GridcellDataset(in_storage = StorageFactory().get_storage('flt_storage', 
        storage_location = "/home/hana/bandera/urbansim/data/GPSRC"), 
    in_table_name = "gc")
locations_psrc.summary()
locations_psrc.plot_histogram("distance_to_highway", bins = 15)
locations_psrc.r_image("distance_to_highway")
locations_psrc.plot_map("distance_to_highway")

locations_psrc.compute_variables("urbansim.gridcell.ln_total_land_value")
locations_psrc.plot_map("ln_total_land_value")

# Models
########

#HLCM

# locations from gridcellset.tab
locations= GridcellDataset(in_storage = StorageFactory().get_storage('tab_storage', storage_location = "."),
                       in_table_name = "gridcellset", id_name="location")
locations.summary()

seed(1)

coefficients = Coefficients(names=("costcoef", ), values=(-0.01,))

specification = EquationSpecification(variables=("gridcell.cost", ), 
                                   coefficients=("costcoef", ))

hlcm = HouseholdLocationChoiceModelCreator().get_model(
    location_set = locations,
    sampler=None,
    utilities="opus_core.linear_utilities",
    probabilities="opus_core.mnl_probabilities",
    choices="opus_core.random_choices_from_index", 
    compute_capacity_flag=False)

agents.get_attribute("location")
results = hlcm.run(specification, coefficients, agents)
agents.get_attribute("location")
hlcm.upc_sequence.plot_choice_histograms( 
                    capacity=locations.get_attribute("vacant_units"))
hlcm.upc_sequence.show_plots()

coef, results = hlcm.estimate(specification, agents)

results = hlcm.run(specification, coef, agents)
hlcm.upc_sequence.plot_choice_histograms( 
                    capacity=locations.get_attribute("vacant_units"))
hlcm.upc_sequence.show_plots()

hlcm2 = HouseholdLocationChoiceModelCreator().get_model(
    location_set = locations,
    sampler=None,
    utilities="opus_core.linear_utilities",
    probabilities="opus_core.mnl_probabilities",
    choices="urbansim.lottery_choices", 
    compute_capacity_flag=True, 
    run_config=Resources({"capacity_string":"gridcell.vacant_units"}))

agents.set_values_of_one_attribute("location", -1*ones(agents.size()))
agents.get_attribute("location")

results = hlcm2.run(specification, coefficients, agents)
agents.get_attribute("location")
hlcm2.upc_sequence.plot_choice_histograms( 
                    capacity=locations.get_attribute("vacant_units"))
hlcm2.upc_sequence.show_plots()
coef, results = hlcm2.estimate(specification, agents)

#HLCM on PSRC
# households from PSRC
agents_psrc = HouseholdDataset(in_storage = StorageFactory().get_storage('flt_storage', 
        storage_location = "/home/hana/bandera/urbansim/data/GPSRC"), 
    in_table_name = "hh")
agents_psrc.summary()

dbcon = []

config = ScenarioDatabaseConfiguration()
server = DatabaseServer(config)
db = server.get_database('PSRC_2000_baseyear')
                   
storage = StorageFactory().get_storage(
    'sql_storage',
    storage_location = db)

coefficients = Coefficients(in_storage=storage)
coefficients.load(in_table_name="household_location_choice_model_coefficients")
specification = EquationSpecification(in_storage=storage)
specification.load(in_table_name="household_location_choice_model_specification")
specification.get_variable_names()


hlcm_psrc = HouseholdLocationChoiceModelCreator().get_model(
    location_set = locations_psrc,
    sampler = "opus_core.samplers.weighted_sampler", 
    sample_size_locations=10,
    choices="urbansim.lottery_choices", 
    compute_capacity_flag=True, 
    run_config=Resources({"capacity_string":"urbansim.gridcell.vacant_residential_units"}))

result = hlcm_psrc.run(specification, coefficients, agents_psrc, 
                       agents_index=sample(range(agents_psrc.size()), 500),
                       debuglevel=4)
# run it again

idx = where(agents_psrc.get_attribute("grid_id")>0)[0]
idx.size
coef, result = hlcm_psrc.estimate(specification, agents_psrc, 
                    agents_index=idx,
                    estimate_config=Resources({"estimation_size_agents":0.01}),
                    debuglevel=4)

result = hlcm_psrc.run(specification, coef, agents_psrc, 
                       agents_index=sample(range(agents_psrc.size()), 500),
                       debuglevel=4)

storage = StorageFactory().get_storage(
    'sql_storage',
    storage_location = db)

zones_psrc = ZoneDataset(in_storage = storage)
hlcm_psrc_zones = HouseholdLocationChoiceModelCreator().get_model(
    location_set = zones_psrc,
    sampler = "opus_core.samplers.weighted_sampler", 
    sample_size_locations=10,
    choices="opus_core.random_choices_from_index", 
    compute_capacity_flag=False,
    estimate_config=Resources({"weights_for_estimation_string":None}))

specification = EquationSpecification(variables=(
    "urbansim.zone.number_of_jobs", 
    "urbansim.household.income"), 
                                      coefficients=(
    "NOJ", "INC"))

agents_psrc.compute_variables(["urbansim.household.zone_id"],
                              resources=Resources({"gridcell":locations_psrc}))
jobs_psrc = JobDataset(in_storage = StorageFactory().get_storage('flt_storage', 
        storage_location = "/home/hana/urbansim/data/GPSRC"), 
    in_table_name = "jobs")
coef, result = hlcm_psrc_zones.estimate(specification, agents_psrc, 
                    agents_index=idx,
                    estimate_config=Resources({"estimation_size_agents":0.01}),
                    data_objects={"job":jobs_psrc, "gridcell":locations_psrc},
                    debuglevel=4)

result = hlcm_psrc_zones.run(specification, coef, agents_psrc, 
                       agents_index=array(sample(range(agents_psrc.size()), 500)),
                       data_objects={"job":jobs_psrc, "gridcell":locations_psrc},
                       debuglevel=4)
# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.configs.base_config_zone import run_configuration as config
from urbansim.configs.estimation_base_config import estimation_configuration
from opus_core.configuration import Configuration

run_configuration = Configuration(config)
run_configuration.merge(estimation_configuration)
run_configuration["models_configuration"]["prepare_datasets_for_aggregation"]["controller"]["run"]["arguments"] = {
                     "datasets_variables": "{household: ['urbansim.household.zone_id'], " + 
                         "job: ['urbansim.job.zone_id'], " + 
                         "building: ['urbansim.building.zone_id'], " + 
                         "zone: ['urbansim.zone.industrial_sqft_per_job', " + 
                                  "'urbansim.zone.commercial_sqft_per_job', " + 
                                  "'is_near_arterial = zone.aggregate(urbansim.gridcell.is_near_arterial, function=aggregate)', " + 
                                  "'is_near_highway = zone.aggregate(urbansim.gridcell.is_near_highway, function=aggregate)', " + 
                                  "'acres_of_land = zone.aggregate(urbansim.gridcell.acres_of_land)', " + 
                                  "'urbansim.zone.avg_val_per_unit_commercial', " + 
                                  "'urbansim.zone.avg_val_per_unit_industrial', " + 
                                  "'urbansim.zone.avg_val_per_unit_governmental', " + 
                                  "'urbansim.zone.avg_val_per_unit_vacant_land', " + 
                                  "'urbansim.zone.avg_val_per_unit_residential', ]" + 
                             "}",
                      "data_objects": "datasets"
                      }
run_configuration["models_configuration"]["household_location_choice_model"]["controller"]["run"]["arguments"]["maximum_runs"]=1
run_configuration["models_configuration"]["employment_location_choice_model"]["controller"]["run"]["arguments"]["maximum_runs"]=1
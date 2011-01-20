# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.estimation.hlcm_parcel_estimation_config import run_configuration
from urbansim.estimation.estimator import update_controller_by_specification_from_module

run_configuration = update_controller_by_specification_from_module(
    run_configuration,"household_location_choice_model", "estimation_HLCM_parcel_specification")

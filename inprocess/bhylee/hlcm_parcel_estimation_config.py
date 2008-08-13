#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from urbansim.estimation.hlcm_parcel_estimation_config import run_configuration
from urbansim.estimation.estimator import update_controller_by_specification_from_module

run_configuration = update_controller_by_specification_from_module(
    run_configuration,"household_location_choice_model", "estimation_HLCM_parcel_specification")

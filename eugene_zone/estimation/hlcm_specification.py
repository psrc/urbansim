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

# estimate HLCM with:

# python -i urbansim/tools/start_estimation.py -c eugene_zone.configs.baseline_estimation -s eugene_zone.estimation.hlcm_specification -m "household_location_choice_model"
specification = {
        -2:
            [ 
            ("urbansim_zone.household_x_zone.ln_sampling_probability_for_bias_correction_mnl_vacant_residential_units", "bias", 1), # bias correction for sampling alternatives
            ('urbansim.household_x_zone.is_high_income_x_percent_high_income','BHIxHI'),
            ('urbansim.household_x_zone.is_low_income_x_percent_low_income','BLIxLI'),
            ('urbansim.household_x_zone.is_1_persons_x_percent_size_1_persons','B1x1'),
            ('ln(urbansim.household_x_zone.income_times_zone_average_income)','BLNINxAVI'),
            ('urbansim.zone.population', 'BPOP'), 
            ('lsfc = ln(urbansim_zone.zone.commercial_sqft)', 'BLSFC'),
            ('ldu = ln(urbansim_zone.zone.residential_units)', 'BLDU'),
            ('lemp20 = ln(eugene.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone)', 'BLEMP20'),
            ]
    }
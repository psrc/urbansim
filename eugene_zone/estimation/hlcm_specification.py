# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

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
            ('lsfc = ln(urbansim_zone.zone.total_commercial_job_space)', 'BLSFC'),
            ('ldu = ln(urbansim_zone.zone.residential_units)', 'BLDU'),
            ('lemp20 = ln(eugene.zone.employment_within_20_minutes_travel_time_hbw_am_drive_alone)', 'BLEMP20'),
            ]
    }
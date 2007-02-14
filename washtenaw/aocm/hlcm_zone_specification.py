#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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


specification = {
        -2:   #submodel_id
            [
#            "opus_core.func.ln(urbansim.zone.average_housing_cost)",
            "opus_core.func.ln(urbansim.zone.average_income)",
#            "opus_core.func.ln(psrc.zone.number_of_jobs_per_acre)",
#            "psrc.household_x_zone.age_times_population_per_acre",
#            "psrc.household_x_zone.persons_times_average_household_size",
#            "opus_core.func.ln(urbansim.household_x_zone.income_times_zone_average_income)",
            #"urbansim.household_x_zone.cost_to_income_ratio",
#            "opus_core.func.ln(psrc.zone.population_per_acre)",
            #"opus_core.func.ln(urbansim.zone.residential_units)",
#            "psrc.zone.ln_employment_within_30_minutes_travel_time_hbw_am_drive_alone",
#            "psrc.household_x_zone.worker1_travel_time_hbw_am_drive_alone_from_home_to_work",
#            "psrc.household_x_zone.worker1_am_total_transit_time_walk_from_home_to_work",
            "urbansim.household_x_zone.income_and_ln_improvement_value_per_unit", 
            ]
    }

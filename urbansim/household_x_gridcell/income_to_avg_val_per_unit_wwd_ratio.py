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

from income_to_avg_val_per_unit_ratio import income_to_avg_val_per_unit_ratio

class income_to_avg_val_per_unit_wwd_ratio(income_to_avg_val_per_unit_ratio):
    """ income / (avg_val_per_unit_residential_wwd/10)""" 
    
    val_per_unit = "residential_avg_val_per_unit_within_walking_distance"
    hh_income = "income"

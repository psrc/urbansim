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

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
   "generic_land_use_type_id=development_template.disaggregate(land_use_type.generic_land_use_type_id)",
    ##TODO(lmwang): not compute cost at template, but at component level, and have proposals sum cost by proposal_components
    #aggregate construction_cost_per_unit from unit_cost for each building component
    #result = sum over all components (percent_of_building_sqft * construction_cost_per_unit / sqft_per_unit)
    ##TODO: do we want to specify the construction cost of residential buildings by $/unit or $/sqft
    #this variable compute the former
    # "construction_cost_per_unit = (development_template.aggregate(urbansim_parcel.development_template_component.construction_cost_per_component)).astype(float32)"
   ]
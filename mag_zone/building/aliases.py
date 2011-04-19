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
    "skyharbor_enplanement_capacity = (building.other_spaces_name=='skyharbor_enplanement_capacity')*(building.other_spaces)",
    "williamsgateway_enplanement_capacity = (building.other_spaces_name=='williamsgateway_enplanement_capacity')*(building.other_spaces)",
    "hotel_motel_rooms = (building.other_spaces_name=='hotel_motel_rooms')*(building.other_spaces)",
    "is_developing_type = (building.building_type_id==1)+(building.building_type_id==2)+(building.building_type_id==3)+(building.building_type_id==4)+(building.building_type_id==5)",
    "bldg_sqft_constructed_this_year = (building.non_residential_sqft - building.non_residential_sqft_lag1)+((building.residential_units*building.sqft_per_unit)-(building.residential_units_lag1*building.sqft_per_unit))",
           ]


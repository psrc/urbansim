# 
# UrbanSim software. Copyright (C) 1998-2004 University of Washington 
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
 
specification ={} 
specification = {   
 
1:   #submodel 
          [         
             "ln_residential_units=ln(building.residential_units)", 
#             "building.year_built", 
             "building.bedrooms", 
#             "sanfrancisco.building.building_sqft",               
             "sanfrancisco.building.building_sqft_per_unit", 
             "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])", 
             "lot_area=building.disaggregate(parcel.area)", 
             "employment_within_60_minutes_bus_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_60_minutes_bus_travel_time,intermediates=[parcel])", 
             "employment_within_20_minutes_hwy_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])", 
             "ln_employment_of_sector_cie_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_sector_cie,intermediates=[parcel])",              
            ], 
2:   #submodel 
          [         
             "ln_residential_units=ln(building.residential_units)", 
#             "building.year_built", 
             "building.bedrooms", 
#             "sanfrancisco.building.building_sqft",               
#             "sanfrancisco.building.building_sqft_per_unit", 
             "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])", 
#             "employment_within_10_minutes_bus_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_10_minutes_bus_travel_time,intermediates=[parcel])", 
             "lot_area=building.disaggregate(parcel.area)",              
             "employment_within_60_minutes_bus_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_60_minutes_bus_travel_time,intermediates=[parcel])", 
#             "employment_within_20_minutes_hwy_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])"              
             "employment_of_sector_cie_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_sector_cie,intermediates=[parcel])",
            ], 
3:   #submodel 
          [         
             "ln_residential_units=ln(building.residential_units)," 
             "building.year_built", 
             "building.bedrooms", 
#             "sanfrancisco.building.building_sqft",               
#             "sanfrancisco.building.building_sqft_per_unit", 
             "households_in_zone=building.disaggregate(sanfrancisco.zone.number_of_households,intermediates=[parcel])", 
#             "employment_within_10_minutes_bus_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_10_minutes_bus_travel_time,intermediates=[parcel])", 
             "lot_area=building.disaggregate(parcel.area)", 
#             "employment_within_60_minutes_bus_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_60_minutes_bus_travel_time,intermediates=[parcel])", 
             "employment_within_20_minutes_hwy_travel_time=building.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,intermediates=[parcel])", 
             "employment_of_sector_cie_in_zone=building.disaggregate(sanfrancisco.zone.employment_of_sector_cie,intermediates=[parcel])", 
            ], 
 
}             

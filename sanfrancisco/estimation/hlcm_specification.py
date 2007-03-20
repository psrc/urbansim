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
             "building:opus_core.func.ln(building.residential_units) as ln_residential_units",
#             "building.year_built",
             "building.bedrooms",
#             "sanfrancisco.building.building_sqft",              
             "sanfrancisco.building.building_sqft_per_unit",
             "building:opus_core.func.disaggregate(sanfrancisco.zone.number_of_households,[parcel]) as households_in_zone",
             "building:opus_core.func.disaggregate(parcel.area) as lot_area",
             "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_within_60_minutes_bus_travel_time,[parcel]) as employment_within_60_minutes_bus_travel_time",             
             "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,[parcel]) as employment_within_20_minutes_hwy_travel_time",             
             "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_of_sector_cie,[parcel]) as ln_employment_of_sector_cie_in_zone",             
            ],
2:   #submodel
          [        
             "building:opus_core.func.ln(building.residential_units) as ln_residential_units",
#             "building.year_built",
             "building.bedrooms",
#             "sanfrancisco.building.building_sqft",              
#             "sanfrancisco.building.building_sqft_per_unit",
             "building:opus_core.func.disaggregate(sanfrancisco.zone.number_of_households,[parcel]) as households_in_zone",
#             "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_within_10_minutes_bus_travel_time,[parcel]) as employment_within_10_minutes_bus_travel_time",             
             "building:opus_core.func.disaggregate(parcel.area) as lot_area",             
             "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_within_60_minutes_bus_travel_time,[parcel]) as employment_within_60_minutes_bus_travel_time",             
#             "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,[parcel]) as employment_within_20_minutes_hwy_travel_time",             
             "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_of_sector_cie,[parcel]) as employment_of_sector_cie_in_zone",             
            ],
3:   #submodel
          [        
             "building:opus_core.func.ln(building.residential_units) as ln_residential_units",
             "building.year_built",
             "building.bedrooms",
#             "sanfrancisco.building.building_sqft",              
#             "sanfrancisco.building.building_sqft_per_unit",
             "building:opus_core.func.disaggregate(sanfrancisco.zone.number_of_households,[parcel]) as households_in_zone",
#             "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_within_10_minutes_bus_travel_time,[parcel]) as employment_within_10_minutes_bus_travel_time",             
             "building:opus_core.func.disaggregate(parcel.area) as lot_area",             
#             "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_within_60_minutes_bus_travel_time,[parcel]) as employment_within_60_minutes_bus_travel_time",             
             "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_within_20_minutes_hwy_travel_time,[parcel]) as employment_within_20_minutes_hwy_travel_time",             
             "building:opus_core.func.disaggregate(sanfrancisco.zone.employment_of_sector_cie,[parcel]) as employment_of_sector_cie_in_zone",             
            ],

}            

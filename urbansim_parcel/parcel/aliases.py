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

# this is a test of the expression alias file
# one of the aliases uses a primary attribute in the expression, the other a variable

aliases = [
   "is_residential_land_use_type = parcel.disaggregate(generic_land_use_type.unit_name == 'residential_units', [land_use_type])",
   "plan_1=parcel.plan_type_id==1",
    "plan_2=parcel.plan_type_id==2",
    "plan_3=parcel.plan_type_id==3",
    "plan_4=parcel.plan_type_id==4",
    "plan_5=parcel.plan_type_id==5",
    "plan_6=parcel.plan_type_id==6",
    "plan_7=parcel.plan_type_id==7",
    "plan_8=parcel.plan_type_id==8",
    "plan_9=parcel.plan_type_id==9",
    "plan_10=parcel.plan_type_id==10",
    "plan_11=parcel.plan_type_id==11",
    "plan_12=parcel.plan_type_id==12",
    "plan_13=parcel.plan_type_id==13",
    "plan_14=parcel.plan_type_id==14",
    "plan_15=parcel.plan_type_id==15",
    "plan_16=parcel.plan_type_id==16",
    "plan_17=parcel.plan_type_id==17",
    "plan_18=parcel.plan_type_id==18",
    "plan_19=parcel.plan_type_id==19",
    "plan_20=parcel.plan_type_id==20",
    # Carefull: the following two variables depend on the contents of the table plan_types
    "is_residential_plan_type = (%s + %s + %s + %s + %s + %s + %s + %s + %s + %s + %s + %s + %s + %s) > 0" % (
              "urbansim_parcel.parcel.plan_1",
              "urbansim_parcel.parcel.plan_3",
              "urbansim_parcel.parcel.plan_4",
              "urbansim_parcel.parcel.plan_6",
              "urbansim_parcel.parcel.plan_7",
              "urbansim_parcel.parcel.plan_8",
              "urbansim_parcel.parcel.plan_9",
              "urbansim_parcel.parcel.plan_11",
              "urbansim_parcel.parcel.plan_12",
              "urbansim_parcel.parcel.plan_13",
              "urbansim_parcel.parcel.plan_16",
              "urbansim_parcel.parcel.plan_17",
              "urbansim_parcel.parcel.plan_19",
              "urbansim_parcel.parcel.plan_20"),
    "is_non_residential_plan_type = (%s + %s + %s + %s + %s + %s + %s + %s + %s) > 0" % (
              "urbansim_parcel.parcel.plan_5",
              "urbansim_parcel.parcel.plan_6",
              "urbansim_parcel.parcel.plan_10",
              "urbansim_parcel.parcel.plan_12",
              "urbansim_parcel.parcel.plan_14",
              "urbansim_parcel.parcel.plan_15",
              "urbansim_parcel.parcel.plan_16",
              "urbansim_parcel.parcel.plan_18",
              "urbansim_parcel.parcel.plan_20"),
       "used_land_area = (parcel.aggregate(building.land_area, function=sum)).astype(int32)",
       "unit_name = parcel.disaggregate(land_use_type.unit_name)",
       "building_sqft = (parcel.aggregate(urbansim_parcel.building.building_sqft)).astype(int32)",
       "building_sqft_per_unit = urbansim_parcel.parcel.building_sqft/(urbansim_parcel.parcel.residential_units).astype(float32)",
       "residential_units = (parcel.aggregate(building.residential_units)).astype(int32)",
       "parcel_sqft_per_unit = parcel.parcel_sqft/(urbansim_parcel.parcel.residential_units).astype(float32)",
       #"unit_price = (parcel.land_value + parcel.improvement_value) / (urbansim_parcel.parcel.existing_units).astype(float32)"
       "unit_price = (parcel.land_value + parcel.improvement_value) / (urbansim_parcel.parcel.building_sqft).astype(float32)"
           ]
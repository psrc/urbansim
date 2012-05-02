# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

"""
       income breaks:
          1 - Less than $25K;
          2 - $25K to $45K;
          3 - $45 to $75K;
          4 - More than $75K.
"""

aliases = [
    "income_4 = 1 * (household.income < 20700) +" + \
                         " 2 * numpy.logical_and(household.income >= 20700, household.income < 47620) +" + \
                         " 3 * numpy.logical_and(household.income >= 47620, household.income < 80800 ) +" + \
                         " 4 * (household.income >= 80800 )",
    "income_4_person_3 = 1 * (household.income < 25000)*(household.persons < 2) +" + \
                         " 2 * numpy.logical_and(household.income >= 25000, household.income < 45000)*(household.persons < 2) +" + \
                         " 3 * numpy.logical_and(household.income >= 45000, household.income < 75000)*(household.persons < 2) +" + \
                         " 4 * (household.income >= 75000)*(household.persons < 2) +" +\
                         " 5 * (household.income < 25000)*(household.persons == 2) +" + \
                         " 6 * numpy.logical_and(household.income >= 25000, household.income < 45000)*(household.persons == 2) +" + \
                         " 7 * numpy.logical_and(household.income >= 45000, household.income < 75000)*(household.persons == 2) +" + \
                         " 8 * (household.income >= 75000)*(household.persons == 2) +" +\
                         " 9 * (household.income < 25000)*(household.persons > 2) +" + \
                         " 10 * numpy.logical_and(household.income >= 25000, household.income < 45000)*(household.persons > 2) +" + \
                         " 11 * numpy.logical_and(household.income >= 45000, household.income < 75000)*(household.persons > 2) +" + \
                         " 12 * (household.income >= 75000)*(household.persons > 2)",
    "income_4_tenure_2 = 1 * (household.income < 25000)*(household.tenure == 1) +" + \
                         " 2 * numpy.logical_and(household.income >= 25000, household.income < 45000)*(household.tenure == 1) +" + \
                         " 3 * numpy.logical_and(household.income >= 45000, household.income < 75000)*(household.tenure == 1) +" + \
                         " 4 * (household.income >= 75000)*(household.tenure == 1) +" +\
                         " 5 * (household.income < 25000)*(household.tenure == 2) +" + \
                         " 6 * numpy.logical_and(household.income >= 25000, household.income < 45000)*(household.tenure == 2) +" + \
                         " 7 * numpy.logical_and(household.income >= 45000, household.income < 75000)*(household.tenure == 2) +" + \
                         " 8 * (household.income >= 75000)*(household.tenure == 2)" ,
    "income_4_buildingtype_4 = 1 * (household.income < 25000)*(honolulu_parcel.household.residential_building_type_id ==1) +" + \
                         " 2 * numpy.logical_and(household.income >= 25000, household.income < 45000)*(honolulu_parcel.household.residential_building_type_id ==1) +" + \
                         " 3 * numpy.logical_and(household.income >= 45000, household.income < 75000)*(honolulu_parcel.household.residential_building_type_id ==1) +" + \
                         " 4 * (household.income >= 75000)*(honolulu_parcel.household.residential_building_type_id ==1) +" +\
                         " 5 * (household.income < 25000)*(honolulu_parcel.household.residential_building_type_id == 2) +" + \
                         " 6 * numpy.logical_and(household.income >= 25000, household.income < 45000)*(honolulu_parcel.household.residential_building_type_id == 2) +" + \
                         " 7 * numpy.logical_and(household.income >= 45000, household.income < 75000)*(honolulu_parcel.household.residential_building_type_id == 2) +" + \
                         " 8 * (household.income >= 75000)*(honolulu_parcel.household.residential_building_type_id == 2) +" +\
                         " 9 * (household.income < 25000)*(honolulu_parcel.household.residential_building_type_id == 3) +" + \
                         " 10 * numpy.logical_and(household.income >= 25000, household.income < 45000)*(honolulu_parcel.household.residential_building_type_id == 3) +" + \
                         " 11 * numpy.logical_and(household.income >= 45000, household.income < 75000)*(honolulu_parcel.household.residential_building_type_id == 3) +" + \
                         " 12 * (household.income >= 75000)*(honolulu_parcel.household.residential_building_type_id == 3) +" +\
                         " 13 * (household.income < 25000)*(honolulu_parcel.household.residential_building_type_id == 4) +" + \
                         " 14 * numpy.logical_and(household.income >= 25000, household.income < 45000)*(honolulu_parcel.household.residential_building_type_id == 4) +" + \
                         " 15 * numpy.logical_and(household.income >= 45000, household.income < 75000)*(honolulu_parcel.household.residential_building_type_id == 4) +" + \
                         " 16 * (household.income >= 75000)*(honolulu_parcel.household.residential_building_type_id == 4)",
    "submarket_id = household.disaggregate(honolulu_parcel.building.submarket_id)",
    "residential_building_type_id = household.disaggregate(honolulu_parcel.building.residential_building_type_id)"

           ]

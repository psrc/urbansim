# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

aliases = [
           "parcel_id=household.disaggregate(building.parcel_id)",
           "zone_id=household.disaggregate(parcel.zone_id, intermediates=[building])",
           "persons=household.number_of_agents(person)",
           "income_break = 1 * (household.income < 25000) +" + \
                         " 2 * numpy.logical_and(household.income >= 25000, household.income < 45000) +" + \
                         " 3 * numpy.logical_and(household.income >= 45000, household.income < 75000) +" + \
                         " 4 * (household.income >= 75000)",
           ]

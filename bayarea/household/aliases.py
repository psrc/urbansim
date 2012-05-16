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
    "income_4 = 1 * (household.income < 25000) +" + \
              " 2 * numpy.logical_and(household.income >= 25000, household.income < 45000) +" + \
              " 3 * numpy.logical_and(household.income >= 45000, household.income < 75000) +" + \
              " 4 * (household.income >= 75000)",
    "income_category = bayarea.household.income_4",
    "income_1989 = bayarea.household.income * .7201",  #base year household.income is in 2000 dollars
    "income_1989_category = 1 * (bayarea.household.income_1989 < 25000) +" + \
                         " 2 * numpy.logical_and(bayarea.household.income_1989 >= 25000, bayarea.household.income_1989 < 45000) +" + \
                         " 3 * numpy.logical_and(bayarea.household.income_1989 >= 45000, bayarea.household.income_1989 < 75000) +" + \
                         " 4 * (bayarea.household.income_1989 >= 75000)",
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
    "submarket_id = household.disaggregate(bayarea.building.submarket_id)",

           ]

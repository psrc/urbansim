# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

"""
       logsum breaks by income:
          1 - Less than $25K;
          2 - $25K to $45K;
          3 - $45 to $75K;
          4 - More than $75K.
"""

aliases = [
    "logsum_income_break = 1 * (household.income < 25000) +" + \
                         " 2 * numpy.logical_and(household.income >= 25000, household.income < 45000) +" + \
                         " 3 * numpy.logical_and(household.income >= 45000, household.income < 75000) +" + \
                         " 4 * (household.income >= 75000)",
           ]

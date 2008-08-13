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

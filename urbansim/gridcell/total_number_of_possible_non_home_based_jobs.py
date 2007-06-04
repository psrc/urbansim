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

from opus_core.variables.variable import Variable
from urbansim.functions import attribute_label
from variable_functions import my_attribute_label
from numpy import ma
from numpy import float32

class total_number_of_possible_non_home_based_jobs(Variable):
    """Computed by dividing the total sqft. available for non-home-based-jobs by the 
    amount of square feet of the non-home-based jobs' development type ID
    """
    
    def dependencies(self):
        return [my_attribute_label("total_number_of_possible_commercial_jobs"), 
                my_attribute_label("total_number_of_possible_industrial_jobs")]

    def compute(self, dataset, arguments):
        return self.get_dataset().get_attribute("total_number_of_possible_commercial_jobs") + \
               self.get_dataset().get_attribute("total_number_of_possible_industrial_jobs")

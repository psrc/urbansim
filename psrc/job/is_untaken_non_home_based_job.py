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

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import ones, int8, logical_and

class is_untaken_non_home_based_job(Variable):
    """return if a job is untaken and non home-based"""

    def dependencies(self):
        return [my_attribute_label("is_untaken"),
                "job.home_based"]
        
    def compute(self, dataset_pool):
        jobs = self.get_dataset()
        results = logical_and(jobs.get_attribute("is_untaken"),
                              1 - jobs.get_attribute("home_based"))
        return results
    

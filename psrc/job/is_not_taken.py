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
from variable_functions import my_attribute_label
from urbansim.functions import attribute_label
from numpy import ones, int8

class is_not_taken(Variable):
    """return if a job has a match to person in persons table"""

    def dependencies(self):
        return [my_attribute_label("job_id"),
                "person.job_id", "person.person_id"]
        
    def compute(self, dataset_pool):
        jobs = self.get_dataset()
        persons = arguments.translate("person")
        hh_ids = jobs.get_join_data(persons, "person_id", join_attribute="job_id",
                           return_value_if_not_found=-1)
        return (hh_ids == -1)
    

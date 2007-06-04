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
from urbansim.gridcell.vacant_commercial_job_space import vacant_commercial_job_space as gc_vacant_commercial_job_space


class vacant_commercial_job_space(Variable):
    """ The commercial_sqft/commercial_sqft_per_job - number_of_commercial_jobs. """ 

    number_of_commercial_jobs = "number_of_commercial_jobs"
    commercial_sqft = "commercial_sqft = zone.aggregate(gridcell.commercial_sqft, function=sum)"
    sqft = "commercial_sqft_per_job = zone.aggregate(gridcell.commercial_sqft_per_job, function=mean)"

    def dependencies(self):
        return [my_attribute_label(self.number_of_commercial_jobs), 
                self.commercial_sqft, self.sqft]                             

    def compute(self, dataset_pool):
        vacant_job_space = gc_vacant_commercial_job_space()
        vacant_job_space.set_dataset(self.get_dataset())
        return vacant_job_space.compute(dataset_pool)
    


from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.vacant_commercial_job_space"

    def test_my_inputs(self):
        number_of_commercial_jobs = array([12, 39])
        commercial_sqft = array([1200, 16, 3900, 15])
        commercial_sqft_per_job = array([20, 3, 30, 0])

        values = VariableTestToolbox().compute_variable(self.variable_name, 
            {"zone":{ 
                "number_of_commercial_jobs":number_of_commercial_jobs}, 
              "gridcell":{
                "commercial_sqft":commercial_sqft, 
                "commercial_sqft_per_job":commercial_sqft_per_job,
                 "zone_id":array([1,1,2,2])}}, 
            dataset = "zone")
        should_be = array([93, 222])
        
        self.assertEqual(ma.allequal(values, should_be), True, msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()
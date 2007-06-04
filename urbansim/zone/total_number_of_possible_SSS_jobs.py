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

from urbansim.gridcell.total_number_of_possible_SSS_jobs_from_buildings import total_number_of_possible_SSS_jobs_from_buildings as gc_total_number_of_possible_SSS_jobs_from_buildings
from variable_functions import my_attribute_label

class total_number_of_possible_SSS_jobs(gc_total_number_of_possible_SSS_jobs_from_buildings):
    """ Sums number of possible jobs over zones.
    """
        
    def dependencies(self):
        return [my_attribute_label(self.sqft), 
                my_attribute_label(self.sqft_per_job)] 
        
from opus_core.tests import opus_unittest
from urbansim.variable_test_toolbox import VariableTestToolbox
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    variable_name = "urbansim.zone.total_number_of_possible_commercial_jobs"

    def test_my_inputs( self ):
        #declare an array of four locations, each with the specified sector ID below

        commercial_sqft = array([1000, 500, 5000, 233])
        commercial_sqft_per_job = array([20, 0, 100, 33])

        values = VariableTestToolbox().compute_variable( self.variable_name, 
            {"zone":{ 
                "buildings_commercial_sqft":commercial_sqft, 
                "commercial_sqft_per_job":commercial_sqft_per_job}}, 
            dataset = "zone" )

        #notice that the computation code above purposely truncates decimal results,
        #which makes sense because fractions of jobs don't exist
        should_be = array( [50.0, 0.0, 50.0, 7.0] )
        self.assertEqual( ma.allequal( values, should_be), True, msg = "Error in " + self.variable_name )


if __name__=='__main__':
    opus_unittest.main()

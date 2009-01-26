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

# from scipy.ndimage import correlate
from opus_core.ndimage import correlate
from numpy import ma
from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label

class abstract_within_walking_distance(Variable):
    """Abstract variable for any '_within_walking_distance' variable that belongs to the gridcell set.
"""
    _return_type= "float32"
    dependent_variable = "not_defined" # to be defined in the child class (must be gridcell variable)
    filled_value = 0.0 # value that goes to the masked spots
    mode = "reflect" # mode for the 'correlate' function

    def dependencies(self):
        return [my_attribute_label(self.dependent_variable)]

    def compute(self, dataset_pool):
        summed = correlate( ma.filled( self.get_dataset().get_2d_attribute( self.dependent_variable ),
                                      self.filled_value ).astype(self._return_type),
                            dataset_pool.get_dataset('urbansim_constant')["walking_distance_footprint"], mode=self.mode)
        return self.get_dataset().flatten_by_id( summed )


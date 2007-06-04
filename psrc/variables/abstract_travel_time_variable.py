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
from numpy import where, repeat, ones, float32, resize, array
from numpy import ma
from urbansim.functions import attribute_label
from opus_core.logger import logger

class abstract_travel_time_variable(Variable):
    """abstract variable for bunch of interaction travel time variables"""

    default_value = 180.0
    agent_zone_id = 'to_be_defined_in_fully_qualified_name'
    location_zone_id = 'to_be_defined_in_fully_qualified_name'
    travel_data_attribute = 'to_be_defined_in_fully_qualified_name'
    direction_from_home = True

    def dependencies(self):
        return [ self.agent_zone_id, self.location_zone_id, self.travel_data_attribute]

    def compute(self, dataset_pool):
        interaction_dataset = self.get_dataset()
        travel_data = dataset_pool.get_dataset('travel_data')
        var1 = interaction_dataset.get_dataset(1).get_attribute_by_index(self.agent_zone_id,
                                                                      interaction_dataset.get_2d_index_of_dataset1())
        var2 = interaction_dataset.get_2d_dataset_attribute(self.location_zone_id)
        if self.direction_from_home:
            home_zone = var1
            work_zone = var2
        else:
            home_zone = var2
            work_zone = var1
        times = resize(array([self.default_value], dtype=float32), home_zone.shape)
        positions = ones(home_zone.shape, dtype="int32")
        #create indices for 2d array of (origin, destination)
        ij = map(lambda x, y: (x, y), where(positions)[0], where(positions)[1])
        for a in ij:
            i, j = a
            try:
                times[i,j] = travel_data.get_attribute_by_id(self.travel_data_attribute, (home_zone[i,j], work_zone[i,j]))
            except:
                logger.log_warning("zone pairs (%s, %s) is not in zoneset; value set to %s." % (home_zone[i,j], work_zone[i,j], self.default_value))

        return times

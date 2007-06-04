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
from numpy import resize, array

class nonhome_based_workers_category(Variable):
    """return if a household has DDD nonhome based worker"""

    def dependencies(self):
        return ["psrc.household.number_of_nonhome_based_workers"]

    def compute(self, dataset_pool):
        nhb_workers = self.get_dataset().get_attribute("number_of_nonhome_based_workers")
        results = resize(array([-1], dtype="int16"), nhb_workers.size)
        results[nhb_workers == 0] = 0
        results[nhb_workers == 1] = 1
        results[nhb_workers >= 2] = 2
        return results
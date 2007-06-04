#
# Opus software. Copyright (C) 1998-2007 University of Washington
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
from numpy import zeros, float32

class time(Variable):
    def compute(self, dataset_pool):
        ds = self.get_dataset()
        choice_names = ds.get_attribute_of_dataset("names", 2)
        result = zeros(ds.size()[0], dtype=float32)
        for ichoice in range(ds.get_reduced_m()):
            result[:, ichoice] = ds.get_attribute_of_dataset(choice_names[ichoice] + "_time")
        return result
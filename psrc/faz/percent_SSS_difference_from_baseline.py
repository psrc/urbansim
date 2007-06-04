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
from numpy import float32
from numpy import ma

class percent_SSS_difference_from_baseline(Variable):
    """percent difference of variable SSS from baseline_SSS"""

    def __init__(self, variable_name):
        self.variable_name = variable_name
        Variable.__init__(self)
    
    def dependencies(self):
        #resource and construction sectors are hard-coded as sector 1 and 2
        return ["urbansim.faz." + self.variable_name,
                my_attribute_label("baseline_%s" % self.variable_name)]

    def compute(self, dataset_pool):
        gridcells = self.get_dataset()
        base = gridcells.get_attribute("baseline_%s" % self.variable_name)
        return ma.filled(( gridcells.get_attribute(self.variable_name) - base) * 100 / \
                ma.masked_where(base==0, base.astype(float32),0.0))

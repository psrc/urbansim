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
from numpy import where, zeros, bool8

class is_pre_DDD(Variable):
    """Returns a boolean indicating if the parcel was built before 1940"""
    
    def __init__(self, number):
        self.year = number
        Variable.__init__(self)
        
    def dependencies(self):
        return ["_is_pre_%s = parcel.year_built < %s" % (self.year, self.year)]

    def compute(self,  dataset_pool):
        return self.get_dataset().get_attribute("_is_pre_%s" % self.year)

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x == False or x == True", values)

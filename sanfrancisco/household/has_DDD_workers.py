#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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
    
class has_DDD_workers(Variable):
    """if a household has DDD workers"""

    def __init__(self, nworkers):
        self.nworkers = nworkers
        Variable.__init__(self)
        
    def dependencies(self):
        return ["_has_%s_workers = household.nfulltime==%s" % (self.nworkers, self.nworkers)
                ]
        
    def compute(self,  dataset_pool):
        return  self.get_dataset().get_attribute("_has_%s_workers" % self.nworkers )

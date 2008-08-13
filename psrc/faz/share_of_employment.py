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
from urbansim.functions import attribute_label
from numpy import float32

class share_of_employment(Variable):
    """share of jobs in the faz.
"""
    _return_type="float32"
    
    
    def dependencies(self):
        return ["psrc.faz.number_of_jobs_without_resource_construction_sectors"]
    
    def compute(self, dataset_pool):
        jobs = self.get_dataset().get_attribute("number_of_jobs_without_resource_construction_sectors")
        return jobs.astype(float32) / jobs.sum()

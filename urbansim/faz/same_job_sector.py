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
from numpy import ones
from urbansim.functions import attribute_label

class same_job_sector(Variable):
    """This variable is not meant to return a useful value but to (re-)create the same_job_sector_table of the faz dataset
    whenever one of the dependent variables changes."""
    def dependencies(self):
        return [attribute_label("job", "sector_id"), attribute_label("job", "faz_id")]

    def compute(self, dataset_pool):
        self.get_dataset().create_same_job_sector_table(dataset_pool.get_dataset('job'))
        return ones((self.get_dataset().size(),))

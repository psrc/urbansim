# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

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

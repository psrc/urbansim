# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.variables.variable import Variable
from numpy import where

class empscaled(Variable):
    """Returns a boolean indicating if the neighborhood is in Paris"""

    dept = "dept"

    def dependencies(self):
        return ["neighborhood.emptot9"]

    def compute(self, dataset_pool):
        emptot9 = self.get_dataset().get_attribute("emptot9")
        return emptot9/1000

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)



# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import where

class is_in_paris(Variable):
    """Returns a boolean indicating if the neighborhood is in Paris"""

    dept = "dept"

    def dependencies(self):
        return ["neighborhood.dept"]

    def compute(self, dataset_pool):
        dept = self.get_dataset().get_attribute("dept")
        return where(dept == 75, True, False)

    def post_check(self, values, dataset_pool):
        self.do_check("x == False or x == True", values)



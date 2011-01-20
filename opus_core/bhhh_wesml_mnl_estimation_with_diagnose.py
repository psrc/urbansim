# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.bhhh_wesml_mnl_estimation import bhhh_wesml_mnl_estimation
from opus_core.linear_utilities_diagnose import linear_utilities_diagnose

class bhhh_wesml_mnl_estimation_with_diagnose(bhhh_wesml_mnl_estimation):
    def run(self, data, *args, **kwargs):
        self._last_coefficients = None
        result = bhhh_wesml_mnl_estimation.run(self, data, *args, **kwargs)
        # run a diagnose procedure
        if self._last_coefficients is not None:
            utilities_class = linear_utilities_diagnose()
            utilities_class.run(data, self._last_coefficients, resources=self.resources)
        return result
        
    def mnl_loglikelihood(self, data, b, depm):
        self._last_coefficients = b
        return bhhh_wesml_mnl_estimation.mnl_loglikelihood(self, data, b, depm)

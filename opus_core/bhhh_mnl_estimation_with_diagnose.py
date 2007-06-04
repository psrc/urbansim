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

from opus_core.bhhh_mnl_estimation import bhhh_mnl_estimation
from opus_core.linear_utilities_diagnose import linear_utilities_diagnose

class bhhh_mnl_estimation_with_diagnose(bhhh_mnl_estimation):
    def run(self, data, *args, **kwargs):
        self._last_coefficients = None
        result = bhhh_mnl_estimation.run(self, data, *args, **kwargs)
        # run a diagnose procedure
        if self._last_coefficients is not None:
            utilities_class = linear_utilities_diagnose()
            utilities_class.run(data, self._last_coefficients, resources=self.resources)
        return result
        
    def mnl_loglikelihood(self, data, b, depm):
        self._last_coefficients = b
        return bhhh_mnl_estimation.mnl_loglikelihood(self, data, b, depm)

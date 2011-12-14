# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import where, exp
from opus_core.variables.variable import Variable
from opus_core.logger import logger

class exp_expected_rate_of_return_on_investment(Variable):
    """Exponentiate the expected_rate_of_return_on_investment, but clip everything larger than 
    the max of computable range to the max. (We think these are weird data points.) 
    Note that the minimum of expected_rate_of_return_on_investment
    is -1 by construction, so no clipping is necessary on the lower end.
    """
    computable_range = (-87.0, 87.0)   # float32
#    computable_range = (-703.0, 703.0) # float64
    _return_type="float32"
        
    def dependencies(self):
        return ["psrc_parcel.development_project_proposal.expected_rate_of_return_on_investment"]
    
    def compute(self,  dataset_pool):
        dpp = self.get_dataset()
        roi = dpp["expected_rate_of_return_on_investment"]
        idxup = where(roi > self.computable_range[1])[0]
        if idxup.size > 0:
            roi[idxup] = self.computable_range[1]
            logger.log_warning('Exponentiating expected_rate_of_return_on_investment: %s values clipped to maximum value of %s.' % (idxup.size, self.computable_range[1]))
        #if (roi > self.computable_range[1]).any():
        #    roi = roi - (roi.max() - self.computable_range[1]) # shift the roi into a computable range
        return exp(roi)
    
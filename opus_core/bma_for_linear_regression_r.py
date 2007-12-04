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
from rpy import r, set_default_mode, NO_CONVERSION
from numpy import zeros, float32, swapaxes, array, resize
from opus_core.misc import check_dimensions
from opus_core.logger import logger

class bma_for_linear_regression_r(object):
    """    Class for variable selection in a linear regression using R package BMA.
    It prints out results computed by the R function bic.glm and plots an image of the results.
    You need to have installed R, rpy and the R package BMA.
    """
    def run(self, data, regression, resources=None):
        """
        Expects an entry 'outcome' in resources that provides the values of the dependent variable.
        'data' is a 2D numpy array of the acctual data (nobservations x ncoefficients),
            it can be created by Dataset.create_regression_data_for_estimation(...).
        'regression' is an instance of a regression class.
        Return a dictionary with results.
        """
        if data.ndim < 2:
            raise StandardError, "Argument 'data' must be a 2D numpy array."

        nobs = data.shape[0]
        nvar = data.shape[1]
        constant_position = resources.get("constant_position",  array([], dtype='int32')) #position for intercept

        if constant_position.size == 0: #position for intercept
            constant_position=-1
            nvalues = nvar
        else:
            constant_position=constant_position[0]
            nvalues = nvar+1

        beta = zeros(nvalues).astype(float32)

        coef_names = resources.get("coefficient_names",  nvar*[])
        outcome = resources["outcome"].astype("float64")
        #from opus_core.misc import write_to_text_file, write_table_to_text_file
        #write_to_text_file("/Users/hana/bma/outcome", outcome)
        #write_table_to_text_file("/Users/hana/bma/dat", resize(array(coef_names), (1,nvar)))
        #write_table_to_text_file("/Users/hana/bma/dat", data, mode="a")
        #return {}
        set_default_mode(NO_CONVERSION)
        r.library("BMA")
        data_for_r = data.astype("float64")
        d = r.data_frame(r.matrix(data_for_r, ncol=nvar, dimnames=[[],coef_names]))
        fit = r.bic_glm(x=d, y=outcome, glm_family="gaussian", strict=1)
        fit[20] = '' # to have less output in the summary
        r.summary(fit)
        #r.postscript(file="/Users/hana/bma/imageplot.ps")
        r.imageplot_bma(fit)
        #r.dev_off()
        return {}


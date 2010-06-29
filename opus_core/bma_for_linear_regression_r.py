# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.estimation_procedure import EstimationProcedure
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri # this turns on an automatic conversion from numpy to rpy2 objects
from rpy2.robjects.packages import importr
from numpy import zeros, float32, array
from opus_core.logger import logger

class bma_for_linear_regression_r(EstimationProcedure):
    """    Class for variable selection in a linear regression using R package BMA.
    It prints out results computed by the R function bic.glm and plots an image of the results.
    You need to have installed R, rpy2 and the R package BMA.
    """
    def run(self, data, regression, resources=None):
        """
        The method prints out summary of the BMA procedure and creates an imageplot.
        If resources has an entry 'bma_imageplot_filename', the imageplot is sent to this file as pdf.
        The method does not return any useful results - it is a tool for variable selection.
        Once you selected your variables, use estimate_linear_regression for further usage of the coefficients. 
        
        Expects an entry 'outcome' in resources that provides the values of the dependent variable.
        'data' is a 2D numpy array of the actual data (nobservations x ncoefficients),
            it can be created by Dataset.create_regression_data_for_estimation(...).
        'regression' is an instance of a regression class.
        """
        r = robjects.r
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
        data_for_r = {}
        for icoef in range(len(coef_names)):
            data_for_r[coef_names[icoef]] = data[:, icoef]
        bma = importr("BMA")
        d = robjects.DataFrame(data_for_r)
        try:
            bma_params = {'x': d, 'y': resources["outcome"], 'glm.family': "gaussian", 'strict':1}
            #fit = bma.bic_glm(x=d, y=resources["outcome"], glm_family="gaussian", strict=1)
            fit = bma.bic_glm(**bma_params)
            fit[20] = '' # to have less output in the summary
            r.summary(fit)
            filename = resources.get('bma_imageplot_filename', None)
            if filename is not None:
                r.pdf(file=filename)
                bma.imageplot_bma(fit)
                r['dev.off']()
            else:
                r.X11()
                bma.imageplot_bma(fit)
        except:
            logger.log_warning("Error in BMA procedure.")
        return {}

from numpy import arange, random, concatenate
from opus_core.tests import opus_unittest
from opus_core.equation_specification import EquationSpecification
from opus_core.datasets.dataset import Dataset
from opus_core.regression_model import RegressionModel
from opus_core.storage_factory import StorageFactory

class BMATests(opus_unittest.OpusTestCase):
    def skip_test_bma(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='dataset',
            table_data={
                "id":arange(100)+1,
                "attr1":concatenate((random.randint(0,10, 50), random.randint(20,40, 50))),
                "attr2":random.ranf(100),
                "outcome": array(50*[0]+50*[1])
                }
            )

        ds = Dataset(in_storage=storage, in_table_name='dataset', id_name="id")
        specification = EquationSpecification(
                          variables=array(["constant", "attr2", "attr1"]),
                          coefficients=array(["constant", "ba2", "ba1"]))

        filename = 'bma_output.pdf'
        model = RegressionModel(estimate_config={'bma_imageplot_filename': filename})
        model.estimate(specification, ds, "outcome", procedure="opus_core.bma_for_linear_regression_r")

 

if __name__ == "__main__":
    opus_unittest.main()
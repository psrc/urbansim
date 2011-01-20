# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


from opus_core.tests import opus_unittest
import os
import biogeme.working_directory
from numpy import array, arange
from opus_core.datasets.dataset import Dataset
from opus_core.choice_model import ChoiceModel
from opus_core.equation_specification import EquationSpecification
from opus_core.resources import Resources
from opus_core.logger import logger
import re

class AkivaModelTest(opus_unittest.OpusTestCase):
    # Because the way Biogeme is working, there can be only one test running at the time.

    def setUp(self):
        # create a dataset
        self.dataset = Dataset(
            data={
                "car_time": array([
                    52.9, 4.10, 4.10 , 56.20, 51.80, 
                    0.20, 27.60, 89.90, 41.50, 95.00, 
                    99.10, 18.50, 82.00, 8.60, 22.50, 
                    51.40, 81.00, 51.00, 62.20, 95.10,  
                    41.60]),
                "bus_time": array([
                    4.4, 28.50, 86.90, 31.60, 20.20,  
                    91.20, 79.70,  2.20, 24.50, 43.50, 
                    8.40, 84.00, 38.00, 1.60, 74.10, 
                    83.80, 19.20, 85.00,  90.10, 22.20, 
                    91.50]),
                "choice": array([
                    2, 2, 1, 2, 2,     
                    1, 1, 2, 2, 2,     
                    2, 1, 1, 2, 1,     
                    1, 2, 1, 1, 2,     
                    1]),
                "id": arange(21)+1
                }, 
            id_name = "id", 
            dataset_name = "person")
        choices = Dataset(
            data={"choice": array([1,2]), "names": array(["car", "bus"])}, 
            id_name = "choice", 
            dataset_name="transport"
            )

        self.choicemodel = ChoiceModel(choice_set=choices,
                           utilities = "opus_core.linear_utilities",
                           probabilities = "opus_core.mnl_probabilities",
                           choices = "opus_core.random_choices")

        self.specification = EquationSpecification(
          coefficients=
              ("beta1",      "beta2",          "beta2"),
          variables=
              ("constant","biogeme.person_transport.time", "biogeme.person_transport.time"),
          equations=
              (   1,              1,                2)
          )

    def cleanup(self, dir, model_name):
        # Removes all files in dir that start with model_name and don't end with 'mod'
        # Therefore use different model names for different tests.
        logger.log_status("Deleting biogeme files for model ", model_name, " in ", dir)
        files_in_directory = os.listdir(dir)
        for file in files_in_directory:
            if (re.search('^'+model_name, file) is not None) and \
                (re.search('mod$', file) is None):
                os.remove(os.path.join(dir, file))

### TODO: These tests fail on the build machine because it does not have NumPtr,
###       causing problems with mnl_estimation. Re-enable when fixed.
#    def test_akiva_from_model_file(self):
#        try:
#            import biogeme.mnl_estimation
#        except:
#            # Module need by biogeme.mnl_estimation is not installed on this computer.
#            return
#        # expects a file of name akiva.mod in biogeme/working_directory
#        dir =  biogeme.working_directory.__path__[0]
#        model_name = "akiva" # use different model names (especially different prefix) for different tests!
#        model = os.path.join(dir, model_name)
#        estimation_config = Resources({"skip_generating_model_file": True,
#                                       "biogeme_model_name":model})
#        coefficients, other_results = self.choicemodel.estimate(self.specification,
#                             self.dataset, procedure="biogeme.mnl_estimation", estimate_config = estimation_config,
#                             debuglevel=1)
#        coefficients.summary()
#        self.cleanup(dir, model_name)

### TODO: These tests fail on the build machine because it does not have NumPtr,
###       causing problems with mnl_estimation. Re-enable when fixed.
#    def test_akiva_with_file_generation_in_tmp_dir(self):
#        try:
#            import biogeme.mnl_estimation
#        except:
#            # Module need by biogeme.mnl_estimation is not installed on this computer.
#            return
#        # Generates a model file for biogeme automatically. Operates on a temporary directory.
#        # Commented out because it doesn't cleanup
#        coefficients, other_results = self.choicemodel.estimate(self.specification,
#                             self.dataset, procedure="biogeme.mnl_estimation",
#                             debuglevel=1)
#        coefficients.summary()

### TODO: These tests fail on the build machine because it does not have NumPtr,
###       causing problems with mnl_estimation. Re-enable when fixed.
#    def test_akiva_with_file_generation_with_fixed_model_name(self):
#        try:
#            import biogeme.mnl_estimation
#        except:
#            # Module need by biogeme.mnl_estimation is not installed on this computer.
#            return
#        # Generates a model file for biogeme automatically. Operates in biogeme/working_directory/auto.
#        # The model name is fixed: fg_akiva.
#        dir =  os.path.join(biogeme.working_directory.__path__[0], 'auto')
#        model_name = "fg_akiva"
#        model = os.path.join(dir, model_name)
#        estimation_config = Resources({"biogeme_model_name":model})
#        coefficients, other_results = self.choicemodel.estimate(self.specification,
#                             self.dataset, procedure="biogeme.mnl_estimation", estimate_config = estimation_config,
#                             debuglevel=1)
#        coefficients.summary()
#        coefficients_bhhh, other_results = self.choicemodel.estimate(self.specification,
#                             self.dataset, procedure="opus_core.bhhh_mnl_estimation", estimate_config = estimation_config,
#                             debuglevel=1)
#        coefficients_bhhh.summary()
#        self.cleanup(dir, model_name)

if __name__ == "__main__":
    opus_unittest.main()
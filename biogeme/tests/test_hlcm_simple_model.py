# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE


from opus_core.tests import opus_unittest
import os
import re
import biogeme.working_directory
import biogeme.tests
from opus_core.equation_specification import EquationSpecification
from opus_core.resources import Resources
from opus_core.logger import logger
from urbansim.datasets.household_dataset import HouseholdDataset
from urbansim.datasets.gridcell_dataset import GridcellDataset
from urbansim.models.household_location_choice_model_creator import \
                               HouseholdLocationChoiceModelCreator
from opus_core.coefficients import Coefficients

class HLCMSimpleModelTest(opus_unittest.OpusTestCase):

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
#    def test_hlcm_simple(self):
#        try:
#            import biogeme.mnl_estimation
#        except:
#            # Module need by biogeme.mnl_estimation is not installed on this computer.
#            return
#        # Generates a model file for biogeme automatically. Operates in biogeme/working_directory.
#        # The model name is simple_hlcm.
#
#        # create agents and locations
#        data_files_directory = biogeme.tests.__path__[0]
#        agents = HouseholdDataset(in_storage = StorageFactory().get_storage('tab_storage', storage_location = data_files_directory),
#                      in_table_name = "householdset.tab", id_name="agent_id")
#        locations= GridcellDataset(in_storage = StorageFactory().get_storage('tab_storage', storage_location = data_files_directory),
#                       in_table_name = "gridcellset.tab", id_name="location")
#
#        # create model
#        hlcm = HouseholdLocationChoiceModelCreator().get_model(
#                        location_set = locations,
#                        sampler=None,
#                        utilities="opus_core.linear_utilities",
#                        probabilities="opus_core.mnl_probabilities",
#                        choices="opus_core.random_choices",
#                        compute_capacity_flag=False)
#
#        specification = EquationSpecification(variables=("gridcell.cost", ),
#                                                 coefficients=("costcoef", ))
#
#        madeup_coefficients = Coefficients(names=("costcoef", ), values=(-0.01,))
#
#        # simulate to get reasonable locations for agents
#        seed(1)
#        results = hlcm.run(specification, madeup_coefficients, agents)
#
#        # estimate (costcoef should be around -0.01)
#        dir =  biogeme.working_directory.__path__[0]
#        model_name = "simple_hlcm"
#        model = os.path.join(dir, model_name)
#        estimation_config = Resources({"biogeme_model_name":model})
#        coefficients, other_results = hlcm.estimate(specification,
#                             agents, procedure="biogeme.mnl_estimation",
#                             estimate_config = estimation_config,
#                             debuglevel=1)
#        coefficients.summary()
#        self.cleanup(dir, model_name)

if __name__ == "__main__":
    opus_unittest.main()
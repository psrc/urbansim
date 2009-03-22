# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import sum
from opus_core.model_component import ModelComponent
from opus_core.logger import logger

class Probabilities(ModelComponent):
    """Parent class for user defined probabilities classes.
    """
    def run(self, *args, **kwargs):
        pass

    def check_sum(self, probability):
        logger.log_status("Checking probability sums:")
        if probability.ndim < 2:
            logger.log_status("Probability should have at least 2 dimensions.")
        else:
            sum_probabilities = sum(probability, axis=1)
            logger.log_status("minimum probability sum:" + str(sum_probabilities.min()))
            logger.log_status("maximum probability sum:" + str(sum_probabilities.max()))

    def get_dependent_datasets(self):
        return []
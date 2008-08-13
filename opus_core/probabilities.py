#
# Opus software. Copyright (C) 2005-2008 University of Washington
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
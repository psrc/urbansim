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

from opus_core.bayesian_melding import BayesianMeldingFromFile

class BmNoVarpf(BayesianMeldingFromFile):
    """ Like BayesianMeldingFromFile, but does not include propagation factor of the variance.
    """
    
    def get_posterior_component_variance(self):
        return self.get_variance_for_quantity()


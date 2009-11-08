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
 
from opus_core.upc_sequence import upc_sequence
from opus_core.model_component_creator import ModelComponentCreator

class UPCFactory(ModelComponentCreator):
    def get_model(self, utilities="opus_core.linear_utilities", 
                   probabilities="opus_core.mnl_probabilities",
                   choices="opus_core.random_choices", debuglevel=0):
            
        utilities_class = self.get_model_component(utilities, debuglevel=debuglevel)
        probabilities_class = self.get_model_component(probabilities, debuglevel=debuglevel)
        choices_class = self.get_model_component(choices, debuglevel=debuglevel)
        return upc_sequence(utility_class=utilities_class, probability_class=probabilities_class, 
            choice_class=choices_class, debuglevel=debuglevel)
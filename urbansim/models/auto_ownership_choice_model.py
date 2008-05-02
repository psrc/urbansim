#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from opus_core.choice_model import ChoiceModel

class AutoOwnershipChoiceModel(ChoiceModel):
    """
    """
    model_name = "Auto Ownership Choice Model"
    model_short_name = "AOCM"
    
    def prepare_for_estimate(self, 
                             specification_dict = None, 
                             specification_storage=None, 
                             specification_table=None):
        from opus_core.model import get_specification_for_estimation
        return get_specification_for_estimation(specification_dict, 
                                                specification_storage, 
                                                specification_table)

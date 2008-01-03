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

import os
from opus_emme2.models.abstract_emme2_travel_model import AbstractEmme2TravelModel

class RunMacrosAbstract(AbstractEmme2TravelModel):
    """Abstract class to run specified Emme2 macros. Its children should run before 
       opus_emme2.models.get_emme2_data_into_cache.
    """

    def run(self, macro_group_name, config, year):
        """This is the main entry point.  It gets the appropriate values from the 
        travel_model_configuration part of this config, and then runs the specified 
        emme/2 macros. The macro specification should also have a specification of the bank it should run in.
        'macro_group_name' is the group name of the macros, such as 'emmission_emme2_macros', 'traffic_volume_macros'.
        The macros are taken from a subdirectory macros/{macro_group_name}. 
        'config' must contain an entry ['travel_model_configuration'][year][macro_group_name].
        """
        from opus_emme2.travel_model_output import TravelModelOutput
        import opus_emme2
        tm_output = TravelModelOutput()
        macro_dir = os.path.join(opus_emme2.__path__[0], 'macros', macro_group_name)
        specified_macros = config['travel_model_configuration'][year][macro_group_name]
        for macro_name, macro_info in specified_macros.iteritems():
            bank = macro_info['bank']
            bank_path = self.get_emme2_dir(config, year, bank)
            macro_path = self.get_macro_path(macro_dir, macro_name, bank)
            tm_output.run_emme2_macro(macro_path, bank_path, macro_info['scenario'])

    def get_macro_path(self, macro_dir, macro_name, *args, **kwargs):
        return os.path.join(macro_dir, macro_name)


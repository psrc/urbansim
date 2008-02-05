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
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from opus_core.resources import Resources
from opus_emme2.models.abstract_emme2_travel_model import AbstractEmme2TravelModel

class RunMacrosAbstract(AbstractEmme2TravelModel):
    """Abstract class to run specified Emme2 macros. Its children should run before 
       opus_emme2.models.get_emme2_data_into_cache.
    """

    def run(self, macro_group_name, config, year):
        """This is the main entry point.  It gets the appropriate values from the 
        travel_model_configuration part of this config, and then runs the specified 
        emme/2 macros. The macro specification should also have a specification of the bank it should run in.
        'macro_group_name' is the group name of the macros, such as 'export_macros'.
        The macros should live in the base directory of travel model, subdirectory given by the entry 'path' in each macro.  
        'config' must contain an entry ['travel_model_configuration'][year][macro_group_name].
        """
        from opus_emme2.travel_model_output import TravelModelOutput
        import opus_emme2
        tm_output = TravelModelOutput()
        specified_macros = config['travel_model_configuration'][year][macro_group_name]
        for macro_name, macro_info in specified_macros.iteritems():
            bank = macro_info['bank']
            bank_path = self.get_emme2_dir(config, year, bank)
            macro_path = os.path.join(self.get_emme2_base_dir(config), macro_info.get('path',''), macro_name)
            tm_output.run_emme2_macro(macro_path, bank_path, macro_info['scenario'])


def prepare_for_running_macro(parser):
    from opus_core.file_utilities import get_resources_from_file
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    (options, args) = parser.parse_args()
   
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))
    
    SessionConfiguration(new_instance=True,
                         package_order=resources['dataset_pool_configuration'].package_order,
                         package_order_exceptions=resources['dataset_pool_configuration'].package_order_exceptions,                              
                         in_storage=AttributeCache())
    return (resources, options)
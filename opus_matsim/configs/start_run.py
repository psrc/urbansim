#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

#import sys, pickle

from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration
from opus_core.logger import logger
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.services.run_server.run_manager import RunManager, insert_auto_generated_cache_directory_if_needed




#class StartRunOptionGroup(GenericOptionGroup):
class StartRunOptionGroup(object):
    """ Helper class to start model from an xml config file. 
    """

    config = XMLConfiguration("opus_matsim/configs/seattle_parcel.xml").get_run_configuration("Seattle_baseline")
    
    insert_auto_generated_cache_directory_if_needed(config)
 
    run_manager = RunManager(ServicesDatabaseConfiguration())
    
    run_manager.setup_new_run(cache_directory = config['cache_directory'],configuration = config)

#    run_manager.create_baseyear_cache(config)
 
    run_manager.run_run(config, run_as_multiprocess = True )
    

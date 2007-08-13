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
      
from optparse import OptionParser

from opus_core.logger import logger
from opus_core.resources import Resources
from opus_core.file_utilities import get_resources_from_file
from opus_core.misc import create_import_for_class
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.attribute_cache import AttributeCache

try: import wingdbstub
except: pass

parser = OptionParser()
parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                  help="Name of file containing resources")
parser.add_option("-y", "--year", dest="year", action="store", type="int",
                  help="Year in which to 'run' the travel model")
(options, args) = parser.parse_args()

resources = Resources(get_resources_from_file(options.resources_file_name))

SessionConfiguration(new_instance=True,
                     package_order=resources['dataset_pool_configuration'].package_order,
                     package_order_exceptions=resources['dataset_pool_configuration'].package_order_exceptions,
                     in_storage=AttributeCache())

#logger.enable_memory_logging()
exec(create_import_for_class(resources['creating_baseyear_cache_configuration'].cache_mysql_data, 'CacheMysqlData'))
CacheMysqlData().run(resources)
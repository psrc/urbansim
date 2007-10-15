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

import sys
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.resources import Resources
from opus_core.file_utilities import get_resources_from_file
from opus_core.services.run_server.run_manager import RunManager

if __name__ == "__main__":
    """Written for creating the cache as a process"""
    option_group = GenericOptionGroup()
    parser = option_group.parser
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    (options, args) = parser.parse_args()
    resources = Resources(get_resources_from_file(options.resources_file_name))
    RunManager().create_baseyear_cache(resources)


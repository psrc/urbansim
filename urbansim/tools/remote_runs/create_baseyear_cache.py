# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

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
    RunManager(option_group.get_services_database_configuration(options)).create_baseyear_cache(resources)


# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.services.run_server.generic_option_group import GenericOptionGroup
import shutil, os

if __name__ == "__main__":                                                                 
    option_group = GenericOptionGroup()
    parser = option_group.parser
    parser.add_option("-d", "--directory", dest="communication_path", action="store", type="string",
                      help="Name of directory for communication between processes. It will be deleted and newly created.")
    (options, args) = parser.parse_args()
   #shutil.rmtree('%s' % options.communication_path)
    if not os.path.exists(options.communication_path):
        os.makedirs('%s' % options.communication_path)
    for x in [1,2,3]:
        if not os.path.exists("%s/bank%s" % (options.communication_path, x)):
            os.makedirs('%s/bank%s' % (options.communication_path, x))
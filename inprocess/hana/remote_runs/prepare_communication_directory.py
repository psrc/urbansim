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
        if not os.path.exists("bank%s" % x):
            os.makedirs('bank%s' % x)
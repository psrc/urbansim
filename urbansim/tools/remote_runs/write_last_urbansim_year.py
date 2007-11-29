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
import os
from numpy import array
from opus_core.misc import write_to_text_file

if __name__ == "__main__":                                                                 
    option_group = GenericOptionGroup()
    parser = option_group.parser
    parser.add_option("-d", "--cache-directory", dest="cache_directory", action="store", type="string",
                      help="Cache directory")
    parser.add_option("-o", "--output-file", dest="output_file", action="store", type="string",
                      help="Output file")
    (options, args) = parser.parse_args()

    files = os.listdir(options.cache_directory)
    years = []
    for file in files:
        try:
            year = int(file)
        except:
            continue
        years.append(year)
    result = array(years).max()
    write_to_text_file(options.output_file, array([result]))
    
    
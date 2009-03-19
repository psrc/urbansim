# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

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
    
    
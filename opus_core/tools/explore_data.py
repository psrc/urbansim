# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from optparse import OptionParser
from opus_core.simulation.data_explorer import DataExplorer

class DataExplorerOptionGroup:
    def __init__(self, usage="python %prog -i [options] ", 
                 description="Utility for exploring data stored in cache_directory. Run this script with the -i option to use its functionality interactively."):
            
        self.parser = OptionParser(usage=usage, description=description)
        self.parser.add_option("-d", "--directory", dest="cache_directory", default = None,
                               action="store", help="Cache directory to be used.")
        
def main():    
    import sys
    option_group = DataExplorerOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()
    
    if options.cache_directory is None:
        raise StandardError, "Cache directory (argument -d) must be given."
    
    explorer = DataExplorer(cache_directory=options.cache_directory)
    explorer.run()
    return explorer

if __name__ == '__main__':
    try: import wingdbstub
    except: pass
    ex = main()
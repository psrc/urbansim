# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import urllib.request, urllib.error, urllib.parse, optparse
from opus_core.logger import logger

class LoadXSD(object):
    '''
    classdocs
    '''

    def __init__(self, source, destination):
        '''
        Constructor
        '''
        self.xsd_source = source
        self.xsd_destination = destination
    
    def load_and_store(self):
        
        logger.log_status('Loading xsd file from: %s' %self.xsd_source)
        
        response = urllib.request.urlopen( self.xsd_source )
        xsd = response.read()
        
        logger.log_status('Store xsd file to: %s' %self.xsd_destination)
        outfile = open( self.xsd_destination, 'w')
        outfile.write( xsd )
        outfile.close()

if __name__ == "__main__":
    
    # default parameters are:
    # --source=http://matsim.org/files/dtd/MATSim4UrbanSimConfigSchema.xsd
    parser = optparse.OptionParser()
    parser.add_option("-s", "--source", dest="xsd_source", action="store", type="string",
                      help="URL of xsd file")
    parser.add_option("-d", "--destination", dest="xsd_destination", action="store", type="string",
                      help="Destination of xsd file")
    (options, args) = parser.parse_args()
        
    if options.xsd_source == None:
        logger.log_error("Missing source location (url) to xsd file")
    if options.xsd_destination == None:
        logger.log_error("Missing destination location for xsd file")
    
    load = LoadXSD( options.xsd_source, options.xsd_destination )
    load.load_and_store()
    
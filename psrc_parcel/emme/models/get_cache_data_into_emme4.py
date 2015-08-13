# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_emme2.models.get_cache_data_into_emme2 import GetCacheDataIntoEmme2
from psrc_parcel.emme.models.abstract_emme4_travel_model import AbstractEmme4TravelModel

class GetCacheDataIntoEmme4(GetCacheDataIntoEmme2, AbstractEmme4TravelModel):
    """Get needed emme/2 data from UrbanSim cache into inputs for travel model.
    """
    pass

if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file
    from shutil import copy
    from opus_core.resources import Resources
    
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    parser.add_option("-d", "--dest", dest="destination_directory", action="store", type="string", default=None,
                      help="Copy resulting files into this directory.")
    (options, args) = parser.parse_args()
    
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))

#    logger.enable_memory_logging()
    files = GetCacheDataIntoEmme4(resources).run(options.year)
    if options.destination_directory is not None:
        for file in files:
            copy(file, options.destination_directory)
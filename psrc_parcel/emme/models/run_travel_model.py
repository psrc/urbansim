# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_emme2.models.run_travel_model import RunTravelModel as Emme2RunTravelModel
from psrc_parcel.emme.models.abstract_emme4_travel_model import AbstractEmme4TravelModel

class RunTravelModel(Emme2RunTravelModel, AbstractEmme4TravelModel):
    """Run the travel model. Uses different paths than the parent.
    """
    pass


if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file
    from opus_core.resources import Resources
    from opus_core.session_configuration import SessionConfiguration
    from opus_core.store.attribute_cache import AttributeCache
    
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    parser.add_option("-o", "--output-file", dest="output_file", action="store", type="string",
                      help="Output log file. If not given, it is written into urbansim cache directory.")
    (options, args) = parser.parse_args()
   
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))
    
    SessionConfiguration(new_instance=True,
                         package_order=resources['dataset_pool_configuration'].package_order,                             
                         in_storage=AttributeCache())

#    logger.enable_memory_logging()
    RunTravelModel(resources).run(options.year, options.output_file)
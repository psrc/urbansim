# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.session_configuration import SessionConfiguration
from opus_core.resources import Resources
from opus_core.logger import logger
from travel_model.models.get_cache_data_into_travel_model import GetCacheDataIntoTravelModel
from visum_functions import load_version_file
from opus_core.variables.variable_name import VariableName
import VisumPy.helpers as h

class GetCacheDataIntoVisum(GetCacheDataIntoTravelModel):
    """Get needed VISUM data from UrbanSim cache into inputs for travel model.
    """

    def run(self, config, year):
	GetCacheDataIntoTravelModel.run(self, config, year) 
	# this will call self.create_travel_model_input_file and compute variables for data transfer
	zone_set = SessionConfiguration().get_dataset_from_pool('zone')
	
	tm_config = config['travel_model_configuration']
	attribute_names = [ VariableName(v).get_alias() for v in tm_config["urbansim_to_tm_variables"]]
	       
        # -- Start Visum Specific Code -- #
        
        #Get config params
	visum_dir, fileName = tm_config[year]['version']
	visum_version_number = tm_config['visum_version_number']
	
        #Startup Visum
        Visum = load_version_file(visum_dir, fileName, visum_version_number)
	
        #Set zone attributes in Visum
	try:
	    for attrName in attribute_names:
		tempData = zone_set.get_attribute(attrName).tolist()
		#attribute must be defined in the version file
		if self.__attributeExists(Visum, attrName):
		    #is h.SetMulti case-sensitive?
		    #can h.SetMulti accept a numpy array?
		    h.SetMulti(Visum.Net.Zones, attrName, tempData)
		else:
		    #2 = float, 4 = num decimal places
		    Visum.Net.Zones.AddUserDefinedAttribute(attrName, attrName, attrName, 2, 4) 	
		    h.SetMulti(Visum.Net.Zones, attrName, tempData)
	except Exception:
		error_msg = "Setting zone attribute " + attrName + " failed"
		raise StandardError(error_msg)

	#Save version file
	#This saves over the existing version file
	try:
		Visum.SaveVersion(fileName)
	except Exception:
		error_msg = "Saving version file failed"
		raise StandardError(error_msg)
	    
    def create_travel_model_input_file(self, config, year, zone_set, dataset_pool):
	zone_set.compute_variables(config['travel_model_configuration']['urbansim_to_tm_variables'], 
				   dataset_pool=dataset_pool)
    
    
    def __attributeExists(self, Visum, attributeName):
	"""Visum function to check if attributeName exists for Zones
	"""
	
        for attr in Visum.Net.Zones.Attributes.GetAll:
	    if str(attr.ID).upper() == attributeName.upper():
		return True
	return False

    
if __name__ == "__main__":
    try: import wingdbstub
    except: pass
    from optparse import OptionParser
    from opus_core.file_utilities import get_resources_from_file
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    (options, args) = parser.parse_args()
    resources = Resources(get_resources_from_file(options.resources_file_name))

    logger.enable_memory_logging()
    GetCacheDataIntoVisum().run(resources, options.year)

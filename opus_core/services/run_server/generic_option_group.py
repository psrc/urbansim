# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


from optparse import OptionParser

from opus_core.database_management.configurations.services_database_configuration import ServicesDatabaseConfiguration

class GenericOptionGroup(object):
    def __init__(self, usage="python %prog [options]", description=""):
            
        self.parser = OptionParser(usage=usage, description=description)                     
        self.parser.add_option("--services_database", dest="database_name", default='services', 
                       action="store", help="Name of services database")        
        self.parser.add_option("--database_configuration", dest="database_configuration", default = "services_database_server",
                               action="store", help="Name of the database server configuration in database_server_configurations.xml that is to be used to connect to the services database. Defaults to 'services_database_server'.")
                     
    def get_services_database_configuration(self, options):
        return ServicesDatabaseConfiguration(
                 database_name = options.database_name,                         
                 database_configuration = options.database_configuration                    
            )
        
        
    def parse(self):
        (options, args) = self.parser.parse_args()
        return (options,args)
        
# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from opus_core.resources import Resources
from opus_emme2.models.abstract_emme2_travel_model import AbstractEmme2TravelModel
from opus_core.store.sftp_flt_storage import redirect_sftp_url_to_local_tempdir

class RunMacrosAbstract(AbstractEmme2TravelModel):
    """Abstract class to run specified Emme2 macros. Its children should run before 
       opus_emme2.models.get_emme2_data_into_cache.
    """

    def run(self, macro_group_name, year, output_file=None):
        """This is the main entry point.  It is initialized with the appropriate values from the 
        travel_model_configuration part of this config, and then runs the specified 
        emme/2 macros. The macro specification should also have a specification of the bank it should run in.
        'macro_group_name' is the group name of the macros, such as 'export_macros'.
        The macros should live in the base directory of travel model, subdirectory given by the entry 'path' in each macro.  
        'config' must contain an entry ['travel_model_configuration'][year][macro_group_name].
        """
        from opus_emme2.travel_model_output import TravelModelOutput
        import opus_emme2
        tm_output = TravelModelOutput(self.emme_cmd)
        specified_macros = self.config['travel_model_configuration'][year][macro_group_name]
        if output_file is None:
            tmp_output_file = os.path.join(self.config['cache_directory'], "emme2_export_macros_%s_log.txt" % year)
        else:
            tmp_output_file = output_file
        ## if tmp_output_file is a remote sftp URL, redirect file to local tempdir
        tmp_output_file = redirect_sftp_url_to_local_tempdir(tmp_output_file)
        
        for macro_name, macro_info in specified_macros.iteritems():
            bank = macro_info['bank']
            bank_path = self.get_emme2_dir(year, bank)
            macro_path = os.path.join(self.get_emme2_base_dir(), macro_info.get('path',''), macro_name)
            tm_output.run_emme2_macro(macro_path, bank_path, macro_info['scenario'], output_file=tmp_output_file)


def prepare_for_running_macro(parser):
    from opus_core.file_utilities import get_resources_from_file
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    parser.add_option("-o", "--output-file", dest="output_file", action="store", type="string", default=None,
                      help="Output log file. If not given, it is written into urbansim cache directory.")
    (options, args) = parser.parse_args()
   
    r = get_resources_from_file(options.resources_file_name)
    resources = Resources(get_resources_from_file(options.resources_file_name))
    
    SessionConfiguration(new_instance=True,
                         package_order=resources['dataset_pool_configuration'].package_order,                           
                         in_storage=AttributeCache())
    return (resources, options)
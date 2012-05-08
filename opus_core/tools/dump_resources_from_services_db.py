# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.services.run_server.run_manager import RunManager
from opus_core.file_utilities import write_resources_to_file

class OptionGroup(GenericOptionGroup):
    def __init__(self):
        GenericOptionGroup.__init__(self, usage="python %prog [options] run_id [pickle_file]",
               description="dump resources.pickle from services db for the given run_id")
        self.parser.add_option("-p", "--project-name", dest="project_name", 
                                default='',help="The project name")
                                
if __name__ == "__main__":
    option_group = OptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()

    run_id = int(args[0])
    if len(args) == 2: 
        pickle_file = args[1]
    else:
        pickle_file = "resources.pickle"

    run_manager = RunManager(option_group.get_services_database_configuration(options))
    if options.project_name:
        run_manager.update_environment_variables(run_resources={'project_name':options.project_name}) 

    resources = run_manager.get_resources_for_run_id_from_history(run_id=run_id)
    write_resources_to_file(pickle_file, resources)
                                 

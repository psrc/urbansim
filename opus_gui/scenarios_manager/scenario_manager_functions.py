# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_gui.main.controllers.instance_handlers import get_manager_instance

def update_models_to_run_lists():
    sm = get_manager_instance('scenario_manager')
    if sm is not None:
        sm.validate_models_to_run()

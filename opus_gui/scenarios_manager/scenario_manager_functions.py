# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.main.controllers.instance_handlers import get_manager_instance

def update_models_to_run_lists():
    sm = get_manager_instance('scenario_manager')
    if sm is not None:
        sm.validate_models_to_run()

#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.

import os
from opus_core.services.run_server.generic_option_group import GenericOptionGroup
from opus_core.services.run_server.run_activity import RunActivity
from opus_core.misc import get_config_from_opus_path

from urbansim.tools.run_manager import RunManager

if __name__ == "__main__":
    """Written for running the prepare_for_run method as a process"""
    option_group = GenericOptionGroup()
    parser = option_group.parser
    self.parser.add_option("-c", "--configuration-path", dest="configuration_path", default=None, 
                               help="Opus path to Python module defining configuration.")
    (options, args) = parser.parse_args()
    config = get_config_from_opus_path(options.configuration_path)

    db = option_group.get_services_database(options)
    if db is None:
        run_manager = RunManager()
    else:
        run_activity = RunActivity(db)
        run_manager = RunManager(run_activity)

    history_id = run_manager.prepare_for_run(config)
    os._exit(history_id)
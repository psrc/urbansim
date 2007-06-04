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
#

from opus_core.cache.cache_mysql_data import CacheMysqlData
from opus_core.session_configuration import SessionConfiguration

"""
This script creates a new urbansim_cache and populates it with all 
the tables_to_cache, the lag data, and unrolled gridcells.
It only needs to be run when you need to create or update a cache.
Once the cache is there, you can keep reusing it, e.g. for estimation.
"""

from randstad.estimation.estimation_config import config
CacheMysqlData().run(config, unroll_gridcells=False)


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
from opus_core.logger import logger

class DatabaseServer(object):
    """Base class for OPUS database server.
    """
    def __init__(self, connection, show_output=False) :
        self.con = connection
        self.cursor = self.con.cursor()
        self.show_output = show_output

    def log_sql(self, sql_query, show_output=False):
        if show_output == True:
            logger.log_status("SQL: " + sql_query, tags=["database"], verbosity_level=3)


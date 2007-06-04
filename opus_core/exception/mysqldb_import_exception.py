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

class MySqlDbImportException(ImportError):
    """ Error thrown when the MySQLdb package cannot be imported, i.e. it wasn't installed (properly) on
    this machine.  The MySQLdb package is the connection between the MySql database and Python. 
    """
    
    def __init__ (self, underlying_exception):
        self.underlying_exception = underlying_exception

        
    def __str__(self):
        return ("Unable to import the MySQLdb package, which is the connection between the MySql database "
            "and Python.  The underlying exception "
            "was: %s" % self.underlying_exception.__str__())

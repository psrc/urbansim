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

    
class CantConnectToMySqlException(Exception):
    """ Exception thrown when some MySql instance that the code requires is unreachable.  
        
        A common reason for this is that your environment variables that pertain to MySql 
        (for example, MYSQLUSERNAME and MYSQLPASSWORD) are incorrectly set (for this 
        MySql instance).              
        
        In any of these cases, this exception should be thrown and caught at the appropriate 
        place at which point a warning should be issued explaining this situation."""

    def __init__ (self, underlying_exception):
        self.underlying_exception = underlying_exception        
    
    def __str__(self):
        return ("Unable to connect to some particular instance of MySql.  "
                "A common reason for this is that your environment variables "
                "that pertain to MySql (for example, MYSQLUSERNAME and MYSQLPASSWORD) "
                "are incorrectly set (for this MySql instance).  "
                "See documentation for information on these environment variables.  "
                "The underlying exception was: %s" % self.underlying_exception.__str__() )
            
            